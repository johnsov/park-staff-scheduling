import pandas as pd
from .restricciones_puestos import normalizar_texto

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_personas_asignadas(
    solver,
    x,
    personal,
    turno
):
    """
    Devuelve los índices de las personas asignadas a un turno.
    """

    personas = []

    for p in personal.index:

        if solver.Value(x[(p, turno)]) == 1:
            personas.append(p)

    return personas


def nombre_persona(personal, p):
    """
    Devuelve el nombre de una persona.
    """

    return personal.loc[p, "nombre"]


# ============================================================
# VALIDAR COBERTURA
# ============================================================

def validar_cobertura(
    solver,
    x,
    personal,
    turnos_df
):
    """
    Comprueba que cada turno tenga exactamente
    la cantidad de personas requerida.
    """

    errores = []

    for t in turnos_df.index:

        requeridas = turnos_df.loc[t, "personas"]

        asignadas = sum(
            solver.Value(x[(p, t)])
            for p in personal.index
        )

        if asignadas != requeridas:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"requiere {requeridas}, "
                f"pero tiene {asignadas}"
            )

    return errores


# ============================================================
# VALIDAR AMOR Y PAZ
# ============================================================

def validar_amor_y_paz(
    solver,
    x,
    personal,
    turnos_df
):
    """
    Valida Amor y Paz.

    Reglas:

    - 4 personas
    - 2 hombres
    - 2 mujeres
    """

    errores = []

    turnos = turnos_df[
        turnos_df["puesto"] == "Amor y Paz"
    ].index.tolist()

    for t in turnos:

        asignados = obtener_personas_asignadas(
            solver,
            x,
            personal,
            t
        )

        hombres = sum(
            personal.loc[p, "sexo"] == "M"
            for p in asignados
        )

        mujeres = sum(
            personal.loc[p, "sexo"] == "F"
            for p in asignados
        )

        if hombres != 2:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"debe tener 2 hombres, "
                f"tiene {hombres}"
            )

        if mujeres != 2:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"debe tener 2 mujeres, "
                f"tiene {mujeres}"
            )

    return errores


# ============================================================
# VALIDAR PATO-LEONERA
# ============================================================

def validar_pato_leonera(
    solver,
    x,
    personal,
    turnos_df
):
    """
    Valida Pato-Leonera.

    Reglas:

    - 4 personas
    - 2 hombres
    - 2 mujeres
    - mínimo 1 PVC
    - mínimo 1 conductor de carro
    """

    errores = []

    turnos = turnos_df[
        turnos_df["puesto"] == "Pato-Leonera"
    ].index.tolist()

    for t in turnos:

        asignados = obtener_personas_asignadas(
            solver,
            x,
            personal,
            t
        )

        hombres = sum(
            personal.loc[p, "sexo"] == "M"
            for p in asignados
        )

        mujeres = sum(
            personal.loc[p, "sexo"] == "F"
            for p in asignados
        )

        pvc = sum(
            personal.loc[p, "estrategia"] == "PVC"
            for p in asignados
        )

        conductores = sum(
            personal.loc[p, "conductor_carro"] == "SI"
            for p in asignados
        )

        if hombres != 2:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"debe tener 2 hombres, "
                f"tiene {hombres}"
            )

        if mujeres != 2:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"debe tener 2 mujeres, "
                f"tiene {mujeres}"
            )

        if pvc < 1:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"debe tener mínimo 1 PVC"
            )

        if conductores < 1:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"debe tener mínimo 1 conductor de carro"
            )

    return errores


# ============================================================
# VALIDAR PATO-PANCE
# ============================================================

def validar_pato_pance(
    solver,
    x,
    personal,
    turnos_df
):
    """
    Valida Pato-Pance.

    Reglas:

    - 5 personas
    - exactamente 1 Ecoturismo
    - exactamente 1 conductor de carro
    - nadie de Anchicaya
    - Marianne Hoyos no puede estar
    - Felipe Garcia no puede estar
    - Esmeralda Acosta no puede estar los sábados
    - Cristian Libreros no puede estar los sábados
    """

    errores = []

    turnos = turnos_df[
        turnos_df["puesto"] == "Pato-Pance"
    ].index.tolist()

    for t in turnos:

        asignados = obtener_personas_asignadas(
            solver,
            x,
            personal,
            t
        )

        ecoturismo = sum(
            personal.loc[p, "ecoturismo"] == "SI"
            for p in asignados
        )

        conductores = sum(
            personal.loc[p, "conductor_carro"] == "SI"
            for p in asignados
        )

        if ecoturismo != 1:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"debe tener exactamente 1 persona "
                f"de Ecoturismo, tiene {ecoturismo}"
            )

        if conductores != 1:

            errores.append(
                f"{turnos_df.loc[t, 'id']}: "
                f"debe tener exactamente 1 conductor "
                f"de carro, tiene {conductores}"
            )

        for p in asignados:

            estrategia = str(
                personal.loc[p, "estrategia"]
            ).strip().upper()

            nombre = str(
                personal.loc[p, "nombre"]
            ).strip().upper()

            tipo_dia = normalizar_texto(
                turnos_df.loc[t, "tipo_dia"]
            )

            # Anchicaya

            if estrategia == "ANCHICAYA":

                errores.append(
                    f"{turnos_df.loc[t, 'id']}: "
                    f"{nombre} pertenece a Anchicaya "
                    f"y no puede hacer Pato-Pance"
                )

            # Marianne

            if nombre == "MARIANNE HOYOS":

                errores.append(
                    f"{turnos_df.loc[t, 'id']}: "
                    f"Marianne Hoyos no puede hacer "
                    f"Pato-Pance"
                )

            # Felipe

            if nombre == "FELIPE GARCIA":

                errores.append(
                    f"{turnos_df.loc[t, 'id']}: "
                    f"Felipe Garcia no puede hacer "
                    f"Pato-Pance"
                )

            # Esmeralda sábado

            if (
                nombre == "ESMERALDA ACOSTA"
                and tipo_dia == "sabado"
            ):

                errores.append(
                    f"{turnos_df.loc[t, 'id']}: "
                    f"Esmeralda Acosta no puede "
                    f"trabajar los sábados"
                )

            # Cristian sábado

            if (
                nombre == "CRISTIAN LIBREROS"
                and tipo_dia == "sabado"
            ):

                errores.append(
                    f"{turnos_df.loc[t, 'id']}: "
                    f"Cristian Libreros no puede "
                    f"trabajar los sábados"
                )

    return errores


# ============================================================
# VALIDAR TOPACIO
# ============================================================

def validar_topacio(
    solver,
    x,
    personal,
    turnos_df
):
    """
    Valida Topacio.

    Reglas:

    - 1 persona
    - no Ecoturismo
    - no Marianne Hoyos
    - no Anchicaya
    """

    errores = []

    turnos = turnos_df[
        turnos_df["puesto"] == "Topacio"
    ].index.tolist()

    for t in turnos:

        asignados = obtener_personas_asignadas(
            solver,
            x,
            personal,
            t
        )

        for p in asignados:

            nombre = str(
                personal.loc[p, "nombre"]
            ).strip().upper()

            estrategia = str(
                personal.loc[p, "estrategia"]
            ).strip().upper()

            ecoturismo = (
                personal.loc[p, "ecoturismo"]
                == "SI"
            )

            if ecoturismo:

                errores.append(
                    f"{turnos_df.loc[t, 'id']}: "
                    f"{nombre} pertenece a Ecoturismo "
                    f"y no puede hacer Topacio"
                )

            if nombre == "MARIANNE HOYOS":

                errores.append(
                    f"{turnos_df.loc[t, 'id']}: "
                    f"Marianne Hoyos no puede hacer Topacio"
                )

            if estrategia == "ANCHICAYA":

                errores.append(
                    f"{turnos_df.loc[t, 'id']}: "
                    f"{nombre} pertenece a Anchicaya "
                    f"y no puede hacer Topacio"
                )

    return errores


# ============================================================
# VALIDAR DOBLE TURNO
# ============================================================

def validar_no_doble_turno(
    solver,
    x,
    personal,
    turnos_df
):
    """
    Comprueba que una persona no tenga dos turnos
    el mismo día.
    """

    errores = []

    fechas = turnos_df["fecha"].unique()

    for p in personal.index:

        for fecha in fechas:

            turnos_dia = turnos_df[
                turnos_df["fecha"] == fecha
            ].index.tolist()

            cantidad = sum(
                solver.Value(x[(p, t)])
                for t in turnos_dia
            )

            if cantidad > 1:

                errores.append(
                    f"{nombre_persona(personal, p)} "
                    f"tiene {cantidad} turnos el "
                    f"{fecha}"
                )

    return errores


# ============================================================
# VALIDACIÓN GENERAL
# ============================================================

def validar_solucion(
    solver,
    x,
    personal,
    turnos_df
):
    """
    Ejecuta todas las validaciones.
    """

    errores = []

    errores.extend(
        validar_cobertura(
            solver,
            x,
            personal,
            turnos_df
        )
    )

    errores.extend(
        validar_amor_y_paz(
            solver,
            x,
            personal,
            turnos_df
        )
    )

    errores.extend(
        validar_pato_leonera(
            solver,
            x,
            personal,
            turnos_df
        )
    )

    errores.extend(
        validar_pato_pance(
            solver,
            x,
            personal,
            turnos_df
        )
    )

    errores.extend(
        validar_topacio(
            solver,
            x,
            personal,
            turnos_df
        )
    )

    errores.extend(
        validar_no_doble_turno(
            solver,
            x,
            personal,
            turnos_df
        )
    )

    # ========================================================
    # RESULTADO
    # ========================================================

    print("\n" + "=" * 60)
    print("VALIDACIÓN DE LA SOLUCIÓN")
    print("=" * 60)

    if len(errores) == 0:

        print("\n✓ SOLUCIÓN VÁLIDA")
        print("Todas las reglas verificadas se cumplen.")

    else:

        print(
            f"\n✗ SOLUCIÓN CON {len(errores)} ERRORES\n"
        )

        for error in errores:

            print(" -", error)

    return errores