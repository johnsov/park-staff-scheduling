import pandas as pd


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def normalizar_texto(valor):
    """
    Normaliza textos para evitar problemas de mayúsculas,
    espacios o valores nulos.
    """

    return (
        str(valor)
        .strip()
        .upper()
    )


# ============================================================
# CREAR BLOQUES CONTINUOS
# ============================================================

def crear_bloques(
    calendario,
    puesto,
    prefijo,
    fecha_inicio_puesto,
    duracion_dias,
    personas
):
    """
    Crea bloques continuos.

    Los bloques comparten el día de relevo.

    Ejemplo con duración 4:

    Equipo A:
    lunes -> jueves

    Equipo B:
    jueves -> domingo

    Equipo C:
    domingo -> miércoles
    """

    fechas = (
        calendario["fecha"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    fecha_inicio_puesto = pd.to_datetime(
        fecha_inicio_puesto
    )

    # Solo fechas desde la apertura del puesto
    fechas = [
        fecha
        for fecha in fechas
        if fecha >= fecha_inicio_puesto
    ]

    bloques = []

    numero_bloque = 1

    i = 0

    while i + duracion_dias <= len(fechas):

        bloque_fechas = fechas[
            i:i + duracion_dias
        ]

        # Verificar consecutividad
        son_consecutivos = all(
            bloque_fechas[j]
            -
            bloque_fechas[j - 1]
            ==
            pd.Timedelta(days=1)

            for j in range(
                1,
                duracion_dias
            )
        )

        if not son_consecutivos:

            i += 1
            continue

        bloques.append({

            "id": (
                f"{prefijo}-"
                f"{numero_bloque:02d}"
            ),

            "puesto": puesto,

            "tipo": "bloque",

            "fecha": bloque_fechas[0],

            "fecha_inicio": bloque_fechas[0],

            "fecha_fin": bloque_fechas[-1],

            "duracion_dias": duracion_dias,

            "horario": "24h",

            "personas": personas

        })

        numero_bloque += 1

        # ================================================
        # IMPORTANTE
        # ================================================
        # El siguiente equipo entra el mismo día
        # que sale el anterior.
        #
        # Ejemplo:
        #
        # L M X J
        #       J V S D
        #
        # Avanzamos duración - 1
        # ================================================

        i += duracion_dias - 1

    return bloques


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def crear_turnos(
    calendario,
    configuracion_puestos
):
    """
    Crea todos los turnos de acuerdo con:

    - Calendario
    - Configuracion_Puestos

    Configuracion_Puestos debe tener:

        puesto
        fecha_inicio
        personas
        duracion_dias

    Puestos actuales:

        Amor y Paz
        Pato-Leonera
        Pato-Pance
        Topacio
    """

    # ========================================================
    # COPIAS
    # ========================================================

    calendario = calendario.copy()

    configuracion_puestos = (
        configuracion_puestos.copy()
    )

    # ========================================================
    # NORMALIZAR FECHAS
    # ========================================================

    calendario["fecha"] = pd.to_datetime(
        calendario["fecha"]
    )

    configuracion_puestos[
        "fecha_inicio"
    ] = pd.to_datetime(

        configuracion_puestos[
            "fecha_inicio"
        ]

    )

    # ========================================================
    # NORMALIZAR CALENDARIO
    # ========================================================

    if "tipo_dia" in calendario.columns:

        calendario["tipo_dia"] = (

            calendario["tipo_dia"]
            .astype(str)
            .str.strip()
            .str.lower()

        )

    else:

        # Crear automáticamente el día si no existe
        dias = {

            0: "lunes",
            1: "martes",
            2: "miercoles",
            3: "jueves",
            4: "viernes",
            5: "sabado",
            6: "domingo"

        }

        calendario["tipo_dia"] = (

            calendario["fecha"]
            .dt.weekday
            .map(dias)

        )

    # ========================================================
    # FESTIVOS
    # ========================================================

    if "festivo" in calendario.columns:

        calendario["festivo"] = (

            calendario["festivo"]
            .astype(str)
            .str.strip()
            .str.upper()

        )

    else:

        calendario["festivo"] = "NO"

    # ========================================================
    # ORDENAR
    # ========================================================

    calendario = (

        calendario
        .sort_values("fecha")
        .reset_index(drop=True)

    )

    configuracion_puestos = (

        configuracion_puestos
        .sort_values("fecha_inicio")
        .reset_index(drop=True)

    )

    # ========================================================
    # LISTA DE TURNOS
    # ========================================================

    turnos = []

    # ========================================================
    # RECORRER CONFIGURACIÓN
    # ========================================================

    for _, config in configuracion_puestos.iterrows():

        puesto = str(
            config["puesto"]
        ).strip()

        fecha_inicio = config[
            "fecha_inicio"
        ]

        personas = int(
            config["personas"]
        )

        duracion_dias = int(
            config["duracion_dias"]
        )

        # ====================================================
        # AMOR Y PAZ
        # ====================================================

        if puesto == "Amor y Paz":

            bloques = crear_bloques(

                calendario=calendario,

                puesto=puesto,

                prefijo="AP",

                fecha_inicio_puesto=fecha_inicio,

                personas=personas,

                duracion_dias=duracion_dias

            )

            turnos.extend(
                bloques
            )

        # ====================================================
        # PATO-LEONERA
        # ====================================================

        elif puesto == "Pato-Leonera":

            bloques = crear_bloques(

                calendario=calendario,

                puesto=puesto,

                prefijo="PL",

                fecha_inicio_puesto=fecha_inicio,

                personas=personas,

                duracion_dias=duracion_dias

            )

            turnos.extend(
                bloques
            )

        # ====================================================
        # PATO-PANCE
        # ====================================================

        elif puesto == "Pato-Pance":

            contador = 1

            calendario_puesto = calendario[

                calendario["fecha"]
                >=
                fecha_inicio

            ]

            for _, fila in (
                calendario_puesto.iterrows()
            ):

                tipo_dia = normalizar_texto(
                    fila["tipo_dia"]
                )

                festivo = normalizar_texto(
                    fila["festivo"]
                )

                es_dia_puesto = (

                    tipo_dia in [
                        "SABADO",
                        "DOMINGO"
                    ]

                    or

                    festivo == "SI"

                )

                if es_dia_puesto:

                    turnos.append({

                        "id": (
                            f"PP-"
                            f"{contador:02d}"
                        ),

                        "puesto": puesto,

                        "tipo": "turno",

                        "fecha": fila["fecha"],

                        "fecha_inicio": (
                            fila["fecha"]
                        ),

                        "fecha_fin": (
                            fila["fecha"]
                        ),

                        "duracion_dias": (
                            duracion_dias
                        ),

                        "horario": "dia",

                        "personas": personas,

                        "tipo_dia": (
                            fila["tipo_dia"]
                        ),

                        "festivo": (
                            fila["festivo"]
                        )

                    })

                    contador += 1

        # ====================================================
        # TOPACIO
        # ====================================================

        elif puesto == "Topacio":

            contador = 1

            calendario_puesto = calendario[

                calendario["fecha"]
                >=
                fecha_inicio

            ]

            for _, fila in (
                calendario_puesto.iterrows()
            ):

                tipo_dia = normalizar_texto(
                    fila["tipo_dia"]
                )

                festivo = normalizar_texto(
                    fila["festivo"]
                )

                es_dia_puesto = (

                    tipo_dia in [
                        "SABADO",
                        "DOMINGO"
                    ]

                    or

                    festivo == "SI"

                )

                if es_dia_puesto:

                    turnos.append({

                        "id": (
                            f"TO-"
                            f"{contador:02d}"
                        ),

                        "puesto": puesto,

                        "tipo": "turno",

                        "fecha": fila["fecha"],

                        "fecha_inicio": (
                            fila["fecha"]
                        ),

                        "fecha_fin": (
                            fila["fecha"]
                        ),

                        "duracion_dias": (
                            duracion_dias
                        ),

                        "horario": "dia",

                        "personas": personas,

                        "tipo_dia": (
                            fila["tipo_dia"]
                        ),

                        "festivo": (
                            fila["festivo"]
                        )

                    })

                    contador += 1

        else:

            print(
                f"⚠ Puesto no reconocido: "
                f"{puesto}"
            )

    # ========================================================
    # DATAFRAME FINAL
    # ========================================================

    turnos_df = pd.DataFrame(
        turnos
    )

    if turnos_df.empty:

        return turnos_df

    # ========================================================
    # NORMALIZAR FECHAS
    # ========================================================

    turnos_df["fecha"] = pd.to_datetime(
        turnos_df["fecha"]
    )

    turnos_df["fecha_inicio"] = pd.to_datetime(
        turnos_df["fecha_inicio"]
    )

    turnos_df["fecha_fin"] = pd.to_datetime(
        turnos_df["fecha_fin"]
    )

    # ========================================================
    # ORDENAR
    # ========================================================

    turnos_df = (

        turnos_df
        .sort_values(

            by=[
                "fecha_inicio",
                "puesto"
            ]

        )
        .reset_index(drop=True)

    )

    return turnos_df