import pandas as pd


# ============================================================
# CONFIGURACIÓN
# ============================================================

DURACION_BLOQUE = 4


# ============================================================
# FUNCIÓN AUXILIAR
# ============================================================

def crear_bloques(calendario, puesto, prefijo):
    """
    Crea bloques consecutivos de 4 días para un puesto.

    Cada bloque representa un grupo de personas que permanecerá
    durante los 4 días completos.
    """

    fechas = (
        calendario["fecha"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    bloques = []

    numero_bloque = 1
    i = 0

    while i + DURACION_BLOQUE <= len(fechas):

        bloque_fechas = fechas[
            i:i + DURACION_BLOQUE
        ]

        # ----------------------------------------------------
        # Verificar consecutividad
        # ----------------------------------------------------

        son_consecutivos = all(
            bloque_fechas[j] - bloque_fechas[j - 1]
            == pd.Timedelta(days=1)
            for j in range(1, DURACION_BLOQUE)
        )

        if not son_consecutivos:
            i += 1
            continue

        # ----------------------------------------------------
        # Información del primer día
        # ----------------------------------------------------

        primera_fecha = bloque_fechas[0]

        fila_inicio = calendario[
            calendario["fecha"] == primera_fecha
        ].iloc[0]

        # ----------------------------------------------------
        # Crear bloque
        # ----------------------------------------------------

        bloques.append({
            "id": f"{prefijo}-{numero_bloque:02d}",
            "puesto": puesto,
            "tipo": "bloque",
            "fecha": primera_fecha,
            "fecha_inicio": primera_fecha,
            "fecha_fin": bloque_fechas[-1],
            "duracion_dias": DURACION_BLOQUE,
            "horario": "24h",
            "personas": 4,

            # Información temporal
            "tipo_dia": fila_inicio["tipo_dia"],
            "festivo": fila_inicio["festivo"]
        })

        numero_bloque += 1
        i += DURACION_BLOQUE

    return bloques


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def crear_turnos(calendario):
    """
    Crea las necesidades de puestos de control.

    Puestos:

    1. Amor y Paz
       - 24 horas
       - bloques de 4 días
       - 4 personas

    2. Pato-Leonera
       - 24 horas
       - bloques de 4 días
       - 4 personas

    3. Pato-Pance
       - sábados, domingos y festivos
       - 5 personas
       - turno de un día

    4. Topacio
       - sábados, domingos y festivos
       - 1 persona
       - turno de un día

    Las fechas son controladas exclusivamente desde la hoja
    Calendario del Excel.
    """

    # ========================================================
    # COPIA Y LIMPIEZA DEL CALENDARIO
    # ========================================================

    calendario = calendario.copy()

    calendario["fecha"] = pd.to_datetime(
        calendario["fecha"]
    )

    calendario["tipo_dia"] = (
        calendario["tipo_dia"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    calendario["festivo"] = (
        calendario["festivo"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    calendario = calendario.sort_values(
        "fecha"
    ).reset_index(drop=True)

    # ========================================================
    # LISTA GENERAL DE TURNOS
    # ========================================================

    turnos = []

    # ========================================================
    # 1. AMOR Y PAZ
    # ========================================================

    bloques_amor_paz = crear_bloques(
        calendario=calendario,
        puesto="Amor y Paz",
        prefijo="AP"
    )

    turnos.extend(
        bloques_amor_paz
    )

    # ========================================================
    # 2. PATO-LEONERA
    # ========================================================

    bloques_pato_leonera = crear_bloques(
        calendario=calendario,
        puesto="Pato-Leonera",
        prefijo="PL"
    )

    turnos.extend(
        bloques_pato_leonera
    )

    # ========================================================
    # 3. PATO-PANCE
    # ========================================================

    contador_pato_pance = 1

    for _, fila in calendario.iterrows():

        tipo_dia = fila["tipo_dia"]
        festivo = fila["festivo"]

        es_fin_semana_o_festivo = (
            tipo_dia in ["sabado", "domingo"]
            or festivo == "SI"
        )

        if es_fin_semana_o_festivo:

            turnos.append({
                "id": f"PP-{contador_pato_pance:02d}",
                "puesto": "Pato-Pance",
                "tipo": "turno",
                "fecha": fila["fecha"],
                "fecha_inicio": fila["fecha"],
                "fecha_fin": fila["fecha"],
                "duracion_dias": 1,
                "horario": "dia",
                "personas": 5,
                "tipo_dia": tipo_dia,
                "festivo": festivo
            })

            contador_pato_pance += 1

    # ========================================================
    # 4. TOPACIO
    # ========================================================

    contador_topacio = 1

    for _, fila in calendario.iterrows():

        tipo_dia = fila["tipo_dia"]
        festivo = fila["festivo"]

        es_fin_semana_o_festivo = (
            tipo_dia in ["sabado", "domingo"]
            or festivo == "SI"
        )

        if es_fin_semana_o_festivo:

            turnos.append({
                "id": f"TO-{contador_topacio:02d}",
                "puesto": "Topacio",
                "tipo": "turno",
                "fecha": fila["fecha"],
                "fecha_inicio": fila["fecha"],
                "fecha_fin": fila["fecha"],
                "duracion_dias": 1,
                "horario": "dia",
                "personas": 1,
                "tipo_dia": tipo_dia,
                "festivo": festivo
            })

            contador_topacio += 1

    # ========================================================
    # DATAFRAME FINAL
    # ========================================================

    turnos_df = pd.DataFrame(turnos)

    # Ordenar cronológicamente y luego por puesto
    turnos_df = turnos_df.sort_values(
        by=["fecha_inicio", "puesto"]
    ).reset_index(drop=True)

    return turnos_df