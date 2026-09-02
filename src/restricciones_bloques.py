from ortools.sat.python import cp_model


# ============================================================
# RESTRICCIONES DE AMOR Y PAZ
# ============================================================

def agregar_restricciones_amor_paz(
    model,
    x,
    personal,
    turnos_df
):
    """
    Restricciones específicas del puesto Amor y Paz.

    Cada bloque requiere:

        - 4 personas
        - 2 hombres
        - 2 mujeres

    Las mismas 4 personas permanecen durante los
    cuatro días del bloque.
    """

    bloques_ap = turnos_df[
        turnos_df["puesto"] == "Amor y Paz"
    ].index.tolist()

    hombres = personal[
        personal["sexo"] == "M"
    ].index.tolist()

    mujeres = personal[
        personal["sexo"] == "F"
    ].index.tolist()

    for t in bloques_ap:

        # ----------------------------------------------------
        # Exactamente 2 hombres
        # ----------------------------------------------------

        model.Add(
            sum(
                x[(p, t)]
                for p in hombres
            )
            == 2
        )

        # ----------------------------------------------------
        # Exactamente 2 mujeres
        # ----------------------------------------------------

        model.Add(
            sum(
                x[(p, t)]
                for p in mujeres
            )
            == 2
        )


# ============================================================
# RESTRICCIONES DE PATO-LEONERA
# ============================================================

def agregar_restricciones_pato_leonera(
    model,
    x,
    personal,
    turnos_df
):
    """
    Restricciones específicas del puesto Pato-Leonera.

    Cada bloque requiere:

        - 4 personas
        - 2 hombres
        - 2 mujeres
        - mínimo 1 persona de PVC
        - mínimo 1 conductor de carro
    """

    bloques_pl = turnos_df[
        turnos_df["puesto"] == "Pato-Leonera"
    ].index.tolist()

    hombres = personal[
        personal["sexo"] == "M"
    ].index.tolist()

    mujeres = personal[
        personal["sexo"] == "F"
    ].index.tolist()

    pvc = personal[
        personal["estrategia"] == "PVC"
    ].index.tolist()

    conductores_carro = personal[
        personal["conductor_carro"] == "SI"
    ].index.tolist()

    for t in bloques_pl:

        # ----------------------------------------------------
        # 2 hombres
        # ----------------------------------------------------

        model.Add(
            sum(
                x[(p, t)]
                for p in hombres
            )
            == 2
        )

        # ----------------------------------------------------
        # 2 mujeres
        # ----------------------------------------------------

        model.Add(
            sum(
                x[(p, t)]
                for p in mujeres
            )
            == 2
        )

        # ----------------------------------------------------
        # Mínimo 1 persona PVC
        # ----------------------------------------------------

        model.Add(
            sum(
                x[(p, t)]
                for p in pvc
            )
            >= 1
        )

        # ----------------------------------------------------
        # Mínimo 1 conductor de carro
        # ----------------------------------------------------

        model.Add(
            sum(
                x[(p, t)]
                for p in conductores_carro
            )
            >= 1
        )


# ============================================================
# TODAS LAS RESTRICCIONES DE BLOQUES
# ============================================================

def agregar_restricciones_bloques(
    model,
    x,
    personal,
    turnos_df
):
    """
    Agrega todas las restricciones relacionadas
    con los bloques de 4 días.
    """

    agregar_restricciones_amor_paz(
        model,
        x,
        personal,
        turnos_df
    )

    agregar_restricciones_pato_leonera(
        model,
        x,
        personal,
        turnos_df
    )