import random


# ============================================================
# FUNCIÓN OBJETIVO
# ============================================================

def agregar_funcion_objetivo(
    model,
    x,
    personal,
    turnos_df,
    semilla=None
):
    """
    Optimiza la asignación considerando:

    1. La carga medida en días trabajados.
    2. Una distribución proporcional según cargo:

        OPERARIO     -> 100%
        TECNICO      -> 80%
        TECNOLOGO    -> 70%
        PROFESIONAL  -> 60%

    3. Evitar personas activas sin carga.
    4. Evitar sobrecargas individuales.
    5. Evitar asignaciones consecutivas en
       Pato-Pance y Topacio.
    6. Introducir variación entre soluciones similares.
    """

    # ========================================================
    # PESOS POR CARGO
    # ========================================================
    #
    # Usamos enteros para evitar trabajar con decimales
    # dentro del modelo CP-SAT.
    #
    # OPERARIO     = 10
    # TECNICO      = 8
    # TECNOLOGO    = 7
    # PROFESIONAL  = 6
    #
    # Ejemplo:
    #
    # Operario con 10 días:
    # 10 / 1.0 = 10
    #
    # Profesional con 6 días:
    # 6 / 0.6 = 10
    #
    # Ambos tienen aproximadamente la misma carga relativa.
    # ========================================================

    pesos_cargo = {

        "OPERARIO": 10,
        "TECNICO": 8,
        "TECNÓLOGO": 7,
        "TECNOLOGO": 7,
        "PROFESIONAL": 6

    }


    # ========================================================
    # VARIABLES DE CARGA EN DÍAS
    # ========================================================

    carga = {}

    max_dias_posibles = int(
        turnos_df["duracion_dias"].sum()
    )

    for p in personal.index:

        carga[p] = model.NewIntVar(

            0,
            max_dias_posibles,
            f"carga_{p}"

        )

        model.Add(

            carga[p]

            ==

            sum(

                x[(p, t)]
                *
                int(
                    turnos_df.loc[
                        t,
                        "duracion_dias"
                    ]
                )

                for t in turnos_df.index

            )

        )


    # ========================================================
    # PENALIZAR PERSONAS ACTIVAS SIN CARGA
    # ========================================================

    penalizacion_sin_puesto = []

    for p in personal.index:

        activo = str(
            personal.loc[p, "activo"]
        ).strip().upper()

        if activo == "SI":

            sin_puesto = model.NewBoolVar(
                f"sin_puesto_{p}"
            )

            model.Add(
                carga[p] == 0
            ).OnlyEnforceIf(
                sin_puesto
            )

            model.Add(
                carga[p] >= 1
            ).OnlyEnforceIf(
                sin_puesto.Not()
            )

            penalizacion_sin_puesto.append(
                sin_puesto
            )


    # ========================================================
    # CARGA RELATIVA POR CARGO
    # ========================================================
    #
    # Queremos que:
    #
    # carga_operario / 1.0
    #
    # sea aproximadamente igual a:
    #
    # carga_tecnico / 0.8
    #
    # carga_tecnologo / 0.7
    #
    # carga_profesional / 0.6
    #
    # Como CP-SAT trabaja mejor con enteros,
    # escalamos:
    #
    # carga_relativa = carga * 10 / peso
    #
    # En vez de dividir, usamos variables enteras
    # que representan la carga relativa escalada.
    # ========================================================

    carga_relativa = {}

    for p in personal.index:

        cargo = str(
            personal.loc[p, "cargo"]
        ).strip().upper()

        peso = pesos_cargo.get(
            cargo,
            6
        )

        # Variable proporcional:
        #
        # carga_relativa * peso
        # aproximadamente =
        # carga_real * 10

        carga_relativa[p] = model.NewIntVar(

            0,
            max_dias_posibles * 10,
            f"carga_relativa_{p}"

        )

        # Igualdad escalada:
        #
        # carga_relativa * peso
        # =
        # carga * 10
        #
        # Esto funciona exactamente cuando la división
        # es entera. Para permitir todos los valores de carga,
        # usamos una aproximación mediante desigualdades.

        model.Add(

            carga_relativa[p]
            * peso

            >=

            carga[p]
            * 10

        )

        model.Add(

            carga_relativa[p]
            * peso

            <=

            (
                carga[p]
                * 10
            )
            +
            (
                peso - 1
            )

        )


    # ========================================================
    # MÁXIMA CARGA RELATIVA
    # ========================================================
    #
    # En lugar de minimizar directamente la mayor
    # cantidad de días, minimizamos la mayor carga
    # proporcional.
    #
    # Esto permite que:
    #
    # Operarios hagan más días.
    # Técnicos un poco menos.
    # Tecnólogos menos.
    # Profesionales menos.
    # ========================================================

    max_carga_relativa = model.NewIntVar(

        0,
        max_dias_posibles * 10,
        "max_carga_relativa"

    )

    for p in personal.index:

        model.Add(

            carga_relativa[p]
            <=
            max_carga_relativa

        )


    # ========================================================
    # PENALIZAR PP / TOPACIO CONSECUTIVOS
    # ========================================================

    turnos_ecoturismo = (

        turnos_df[

            turnos_df["puesto"].isin(

                [
                    "Pato-Pance",
                    "Topacio"
                ]

            )

        ]

        .sort_values(
            "fecha_inicio"
        )

        .index.tolist()

    )


    penalizacion_consecutivos = []


    for p in personal.index:

        for i in range(
            len(turnos_ecoturismo) - 1
        ):

            t1 = turnos_ecoturismo[i]

            fecha_1 = turnos_df.loc[
                t1,
                "fecha_inicio"
            ]


            for j in range(
                i + 1,
                len(turnos_ecoturismo)
            ):

                t2 = turnos_ecoturismo[j]

                fecha_2 = turnos_df.loc[
                    t2,
                    "fecha_inicio"
                ]


                diferencia_dias = (

                    fecha_2
                    -
                    fecha_1

                ).days


                # Solo fechas consecutivas

                if diferencia_dias == 1:

                    consecutivo = model.NewBoolVar(

                        f"consecutivo_{p}_{t1}_{t2}"

                    )


                    # consecutivo = 1
                    # si trabaja ambos días

                    model.Add(

                        consecutivo
                        <=
                        x[(p, t1)]

                    )

                    model.Add(

                        consecutivo
                        <=
                        x[(p, t2)]

                    )

                    model.Add(

                        consecutivo
                        >=

                        x[(p, t1)]
                        +
                        x[(p, t2)]
                        -
                        1

                    )


                    penalizacion_consecutivos.append(
                        consecutivo
                    )

                elif diferencia_dias > 1:

                    # Los turnos están ordenados.
                    # Ya no habrá más fechas consecutivas.

                    break


    # ========================================================
    # ALEATORIEDAD CONTROLADA
    # ========================================================

    rng = random.Random(
        semilla
    )

    aleatoriedad = []

    for p in personal.index:

        for t in turnos_df.index:

            coeficiente = rng.randint(
                0,
                3
            )

            aleatoriedad.append(

                coeficiente
                *
                x[(p, t)]

            )


    # ========================================================
    # FUNCIÓN OBJETIVO
    # ========================================================
    #
    # PRIORIDADES:
    #
    # 1. Evitar personas activas sin carga.
    #
    # 2. Evitar PP / Topacio consecutivos.
    #
    # 3. Balancear proporcionalmente según cargo.
    #
    # 4. Aleatoriedad controlada.
    # ========================================================

    model.Minimize(

        # ====================================================
        # 1. EVITAR ACTIVOS SIN CARGA
        # ====================================================

        10000

        *

        sum(
            penalizacion_sin_puesto
        )


        # ====================================================
        # 2. EVITAR ECOTURISMO CONSECUTIVO
        # ====================================================

        +

        500

        *

        sum(
            penalizacion_consecutivos
        )


        # ====================================================
        # 3. BALANCE PROPORCIONAL POR CARGO
        # ====================================================

        +

        100

        *

        max_carga_relativa


        # ====================================================
        # 4. ALEATORIEDAD
        # ====================================================

        +

        sum(
            aleatoriedad
        )

    )


    return carga