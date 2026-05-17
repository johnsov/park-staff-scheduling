from ortools.sat.python import cp_model


# =========================
# BALANCE DE CARGA
# =========================

def agregar_balance_carga(

    model,
    x,
    personal,
    turnos_df,
    turnos_arbolito,
    turnos_pato,
    pvc,
    no_pvc,
    no_pvc_restringidos,
    sin_arbolito

):

    """
    Agrega restricciones de carga:

    - límites PVC
    - límites NO PVC
    - compensación sin Arbolito
    """

    # =====================
    # LÍMITES
    # =====================

    MAX_ARBOLITO_PVC = 5
    MAX_PATO_PVC = 10

    MAX_ARBOLITO_NO_PVC = 2
    MAX_PATO_NO_PVC = 1

    # =====================
    # RESTRICCIONES
    # =====================

    for p in personal.index:

        # =================
        # SIN ARBOLITO
        # =================

        if p in sin_arbolito:

            model.Add(

                sum(

                    x[(p, t)]

                    for t in turnos_pato

                )

                >= 2

            )

            model.Add(

                sum(

                    x[(p, t)]

                    for t in turnos_pato

                )

                >= 3

            )

        # =================
        # PVC
        # =================

        elif p in pvc:

            model.Add(

                sum(

                    x[(p, t)]

                    for t in turnos_arbolito

                )

                <= MAX_ARBOLITO_PVC

            )

            model.Add(

                sum(

                    x[(p, t)]

                    for t in turnos_pato

                )

                <= MAX_PATO_PVC

            )

        # =================
        # NO PVC
        # =================

        elif p in no_pvc_restringidos:

            model.Add(

                sum(

                    x[(p, t)]

                    for t in turnos_arbolito

                )

                <= MAX_ARBOLITO_NO_PVC

            )

            model.Add(

                sum(

                    x[(p, t)]

                    for t in turnos_pato

                )

                <= MAX_PATO_NO_PVC

            )


# =========================
# FUNCIÓN OBJETIVO
# =========================

def agregar_funcion_objetivo(

    model,
    x,
    personal,
    turnos_df,
    no_pvc

):

    """
    Minimiza:

    - uso de NO PVC en Arbolito
    - máxima sobrecarga individual
    """

    # =====================
    # PENALIZACIONES
    # =====================

    penalizaciones = []

    for p in no_pvc:

        for t in turnos_df.index:

            puesto = turnos_df.loc[t, "puesto"]

            if puesto == "Arbolito":

                penalizaciones.append(
                    x[(p, t)]
                )

    # =====================
    # VARIABLES DE CARGA
    # =====================

    carga = {}

    for p in personal.index:

        carga[p] = model.NewIntVar(

            0,
            len(turnos_df),
            f"carga_{p}"

        )

        model.Add(

            carga[p]

            ==

            sum(

                x[(p, t)]

                for t in turnos_df.index

            )

        )

    # =====================
    # MÁXIMA CARGA
    # =====================

    max_carga = model.NewIntVar(

        0,
        len(turnos_df),
        "max_carga"

    )

    for p in personal.index:

        model.Add(
            carga[p] <= max_carga
        )

    # =====================
    # OBJETIVO FINAL
    # =====================

    model.Minimize(

        (
            10 * sum(penalizaciones)
        )

        +

        (
            30 * max_carga
        )

    )