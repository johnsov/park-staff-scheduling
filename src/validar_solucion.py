import pandas as pd


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def normalizar_texto(valor):

    return (
        str(valor)
        .strip()
        .upper()
    )


def obtener_personas_asignadas(
    solver,
    x,
    personal,
    turno
):

    return [

        p

        for p in personal.index

        if solver.Value(
            x[(p, turno)]
        ) == 1

    ]


def nombre_persona(
    personal,
    p
):

    return str(
        personal.loc[
            p,
            "nombre"
        ]
    )


# ============================================================
# VALIDAR COBERTURA
# ============================================================

def validar_cobertura(
    solver,
    x,
    personal,
    turnos_df
):

    errores = []

    for t in turnos_df.index:

        requeridas = int(
            turnos_df.loc[
                t,
                "personas"
            ]
        )

        asignadas = sum(

            solver.Value(
                x[(p, t)]
            )

            for p in personal.index

        )

        if asignadas != requeridas:

            errores.append(

                f"{turnos_df.loc[t, 'id']}: "

                f"requiere {requeridas}, "

                f"tiene {asignadas}"

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

    errores = []

    turnos = turnos_df[

        turnos_df["puesto"]
        ==
        "Amor y Paz"

    ].index.tolist()

    for t in turnos:

        asignados = (
            obtener_personas_asignadas(

                solver,
                x,
                personal,
                t

            )
        )

        hombres = sum(

            normalizar_texto(
                personal.loc[
                    p,
                    "sexo"
                ]
            )
            ==
            "M"

            for p in asignados

        )

        mujeres = sum(

            normalizar_texto(
                personal.loc[
                    p,
                    "sexo"
                ]
            )
            ==
            "F"

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

    errores = []

    turnos = turnos_df[

        turnos_df["puesto"]
        ==
        "Pato-Leonera"

    ].index.tolist()

    for t in turnos:

        asignados = (
            obtener_personas_asignadas(

                solver,
                x,
                personal,
                t

            )
        )

        hombres = sum(

            normalizar_texto(
                personal.loc[
                    p,
                    "sexo"
                ]
            )
            ==
            "M"

            for p in asignados

        )

        mujeres = sum(

            normalizar_texto(
                personal.loc[
                    p,
                    "sexo"
                ]
            )
            ==
            "F"

            for p in asignados

        )

        pvc = sum(

            normalizar_texto(
                personal.loc[
                    p,
                    "estrategia"
                ]
            )
            ==
            "PVC"

            for p in asignados

        )

        conductores = sum(

            normalizar_texto(
                personal.loc[
                    p,
                    "conductor_carro"
                ]
            )
            ==
            "SI"

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

    errores = []

    turnos = turnos_df[

        turnos_df["puesto"]
        ==
        "Pato-Pance"

    ].index.tolist()

    for t in turnos:

        asignados = (
            obtener_personas_asignadas(

                solver,
                x,
                personal,
                t

            )
        )

        ecoturismo = sum(

            normalizar_texto(
                personal.loc[
                    p,
                    "ecoturismo"
                ]
            )
            ==
            "SI"

            for p in asignados

        )

        conductores = sum(

            normalizar_texto(
                personal.loc[
                    p,
                    "conductor_carro"
                ]
            )
            ==
            "SI"

            for p in asignados

        )

        if ecoturismo != 1:

            errores.append(

                f"{turnos_df.loc[t, 'id']}: "

                f"debe tener exactamente "

                f"1 persona de Ecoturismo, "

                f"tiene {ecoturismo}"

            )

        if conductores != 1:

            errores.append(

                f"{turnos_df.loc[t, 'id']}: "

                f"debe tener exactamente "

                f"1 conductor de carro, "

                f"tiene {conductores}"

            )

        # ----------------------------------------------------
        # VALIDAR PERSONAS
        # ----------------------------------------------------

        tipo_dia = normalizar_texto(

            turnos_df.loc[
                t,
                "tipo_dia"
            ]

        )

        for p in asignados:

            estrategia = normalizar_texto(

                personal.loc[
                    p,
                    "estrategia"
                ]

            )

            nombre = normalizar_texto(

                personal.loc[
                    p,
                    "nombre"
                ]

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

                    f"Marianne Hoyos no puede "

                    f"hacer Pato-Pance"

                )

            # Felipe

            if nombre == "FELIPE GARCIA":

                errores.append(

                    f"{turnos_df.loc[t, 'id']}: "

                    f"Felipe Garcia no puede "

                    f"hacer Pato-Pance"

                )

            # Esmeralda sábado

            if (

                nombre
                ==
                "ESMERALDA ACOSTA"

                and

                tipo_dia
                ==
                "SABADO"

            ):

                errores.append(

                    f"{turnos_df.loc[t, 'id']}: "

                    f"Esmeralda Acosta no puede "

                    f"trabajar los sábados"

                )

            # Cristian sábado

            if (

                nombre
                ==
                "CRISTIAN LIBREROS"

                and

                tipo_dia
                ==
                "SABADO"

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

    errores = []

    turnos = turnos_df[

        turnos_df["puesto"]
        ==
        "Topacio"

    ].index.tolist()

    for t in turnos:

        asignados = (
            obtener_personas_asignadas(

                solver,
                x,
                personal,
                t

            )
        )

        for p in asignados:

            nombre = normalizar_texto(

                personal.loc[
                    p,
                    "nombre"
                ]

            )

            estrategia = normalizar_texto(

                personal.loc[
                    p,
                    "estrategia"
                ]

            )

            ecoturismo = (

                normalizar_texto(

                    personal.loc[
                        p,
                        "ecoturismo"
                    ]

                )
                ==
                "SI"

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

                    f"Marianne Hoyos no puede "

                    f"hacer Topacio"

                )

            if estrategia == "ANCHICAYA":

                errores.append(

                    f"{turnos_df.loc[t, 'id']}: "

                    f"{nombre} pertenece a Anchicaya "

                    f"y no puede hacer Topacio"

                )

    return errores


# ============================================================
# VALIDAR SOLAPAMIENTO
# ============================================================

def validar_no_doble_turno(
    solver,
    x,
    personal,
    turnos_df
):
    """
    Verifica que ninguna persona tenga dos puestos
    activos el mismo día.

    Funciona correctamente tanto para:

        - turnos de 1 día
        - bloques de 4 días
        - futuros bloques de cualquier duración
    """

    errores = []

    # --------------------------------------------------------
    # Rango completo de fechas
    # --------------------------------------------------------

    fecha_min = (
        turnos_df["fecha_inicio"]
        .min()
    )

    fecha_max = (
        turnos_df["fecha_fin"]
        .max()
    )

    fechas = pd.date_range(

        start=fecha_min,

        end=fecha_max,

        freq="D"

    )

    # --------------------------------------------------------
    # REVISAR CADA PERSONA
    # --------------------------------------------------------

    for p in personal.index:

        nombre = nombre_persona(
            personal,
            p
        )

        for fecha in fechas:

            turnos_activos = []

            for t in turnos_df.index:

                inicio = turnos_df.loc[
                    t,
                    "fecha_inicio"
                ]

                fin = turnos_df.loc[
                    t,
                    "fecha_fin"
                ]

                # ¿Este turno cubre la fecha?

                if (

                    inicio
                    <=
                    fecha
                    <=
                    fin

                ):

                    if (

                        solver.Value(
                            x[(p, t)]
                        )
                        ==
                        1

                    ):

                        turnos_activos.append(
                            t
                        )

            # ------------------------------------------------
            # ERROR
            # ------------------------------------------------

            if len(turnos_activos) > 1:

                ids_turnos = [

                    turnos_df.loc[
                        t,
                        "id"
                    ]

                    for t in turnos_activos

                ]

                errores.append(

                    f"{nombre} tiene "

                    f"{len(turnos_activos)} "

                    f"turnos simultáneos "

                    f"el "

                    f"{fecha.strftime('%Y-%m-%d')}: "

                    f"{', '.join(ids_turnos)}"

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

    errores = []

    # --------------------------------------------------------
    # COBERTURA
    # --------------------------------------------------------

    errores.extend(

        validar_cobertura(

            solver,
            x,
            personal,
            turnos_df

        )

    )

    # --------------------------------------------------------
    # AMOR Y PAZ
    # --------------------------------------------------------

    errores.extend(

        validar_amor_y_paz(

            solver,
            x,
            personal,
            turnos_df

        )

    )

    # --------------------------------------------------------
    # PATO-LEONERA
    # --------------------------------------------------------

    errores.extend(

        validar_pato_leonera(

            solver,
            x,
            personal,
            turnos_df

        )

    )

    # --------------------------------------------------------
    # PATO-PANCE
    # --------------------------------------------------------

    errores.extend(

        validar_pato_pance(

            solver,
            x,
            personal,
            turnos_df

        )

    )

    # --------------------------------------------------------
    # TOPACIO
    # --------------------------------------------------------

    errores.extend(

        validar_topacio(

            solver,
            x,
            personal,
            turnos_df

        )

    )

    # --------------------------------------------------------
    # SOLAPAMIENTOS
    # --------------------------------------------------------

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

    print(
        "VALIDACIÓN DE LA SOLUCIÓN"
    )

    print("=" * 60)

    if len(errores) == 0:

        print(
            "\n✓ SOLUCIÓN VÁLIDA"
        )

        print(
            "Todas las reglas verificadas "
            "se cumplen."
        )

    else:

        print(

            f"\n✗ SOLUCIÓN CON "

            f"{len(errores)} ERRORES\n"

        )

        for error in errores:

            print(
                " -",
                error
            )

    return errores