import pandas as pd
from ortools.sat.python import cp_model


# ============================================================
# CREAR MODELO
# ============================================================

def crear_modelo():
    """
    Crea y retorna un modelo vacío de CP-SAT.
    """

    model = cp_model.CpModel()

    return model


# ============================================================
# CREAR VARIABLES
# ============================================================

def crear_variables(model, personal, turnos_df):
    """
    Crea las variables de decisión del modelo.

    x[(p, t)] = 1
        si la persona p es asignada al turno/bloque t.

    x[(p, t)] = 0
        si no es asignada.

    Retorna:
        x
    """

    x = {}

    for p in personal.index:

        for t in turnos_df.index:

            x[(p, t)] = model.NewBoolVar(
                f"x_{p}_{t}"
            )

    return x


# ============================================================
# COBERTURA DE TURNOS
# ============================================================

def agregar_restriccion_cobertura(
    model,
    x,
    personal,
    turnos_df
):
    """
    Garantiza que cada turno/bloque tenga exactamente
    la cantidad de personas requerida.

    Ejemplo:

        Amor y Paz → 4 personas
        Pato-Leonera → 4 personas
        Pato-Pance → 5 personas
        Topacio → 1 persona
    """

    for t in turnos_df.index:

        personas_requeridas = int(
            turnos_df.loc[t, "personas"]
        )

        model.Add(
            sum(
                x[(p, t)]
                for p in personal.index
            )
            == personas_requeridas
        )


# ============================================================
# ELEGIBILIDAD
# ============================================================

def agregar_restriccion_elegibilidad(
    model,
    x,
    personal,
    turnos_df
):
    """
    Impide asignar personas que no pueden realizar
    determinados puestos.

    Se utilizan las columnas del Excel:

        activo
        puede_arbolito
        puede_pato

    Y las restricciones específicas conocidas:
        - Marianne Hoyos no puede Pato-Pance
        - Felipe Garcia no puede Pato-Pance
        - Marianne Hoyos no puede Topacio
        - Personas de Anchicaya no hacen Pato-Pance
        - Personas de Anchicaya no hacen Topacio
    """

    for p in personal.index:

        # ----------------------------------------------------
        # Persona inactiva
        # ----------------------------------------------------

        if personal.loc[p, "activo"] != "SI":

            for t in turnos_df.index:

                model.Add(
                    x[(p, t)] == 0
                )

        # ----------------------------------------------------
        # Restricciones por puesto
        # ----------------------------------------------------

        for t in turnos_df.index:

            puesto = turnos_df.loc[t, "puesto"]

        # =================================================
        # AMOR Y PAZ
        # =================================================

        if puesto == "Amor y Paz":

            estrategia = (
                str(
                    personal.loc[p, "estrategia"]
                )
                .strip()
                .upper()
            )

            if "MINER" in estrategia:

                model.Add(
                    x[(p, t)] == 0
                )

            # =================================================
            # PATO-PANCE
            # =================================================

            if puesto == "Pato-Pance":

                # Puede realizar Pato-Pance
                if personal.loc[p, "puede_pato"] != "SI":

                    model.Add(
                        x[(p, t)] == 0
                    )

                # Personas de Anchicaya no hacen Pato-Pance
                if personal.loc[p, "estrategia"] == "ANCHICAYA":

                    model.Add(
                        x[(p, t)] == 0
                    )

                # Marianne Hoyos
                if personal.loc[p, "nombre"] == "Marianne Hoyos":

                    model.Add(
                        x[(p, t)] == 0
                    )

                # Felipe Garcia
                if personal.loc[p, "nombre"] == "Felipe Garcia":

                    model.Add(
                        x[(p, t)] == 0
                    )

            # =================================================
            # TOPACIO
            # =================================================

            elif puesto == "Topacio":

                # No ecoturismo
                if personal.loc[p, "ecoturismo"] == "SI":

                    model.Add(
                        x[(p, t)] == 0
                    )

                # Anchicaya no hace Topacio
                if personal.loc[p, "estrategia"] == "ANCHICAYA":

                    model.Add(
                        x[(p, t)] == 0
                    )

                # Marianne Hoyos
                if personal.loc[p, "nombre"] == "Marianne Hoyos":

                    model.Add(
                        x[(p, t)] == 0
                    )


# ============================================================
# NO DOBLE ASIGNACIÓN EL MISMO DÍA
# ============================================================

def agregar_restriccion_no_solapamiento(
    model,
    x,
    personal,
    turnos_df
):
    """
    Impide que una persona tenga dos asignaciones
    que se crucen temporalmente.

    Para turnos de un día:
        solo puede tener una asignación ese día.

    Para bloques:
        si pertenece a un bloque de 4 días,
        queda ocupada durante los cuatro días.

    Ejemplo:

        Juan → AP-01 (05/09 - 08/09)

    Entonces Juan NO puede:

        Pato-Pance 05/09
        Pato-Pance 06/09
        Pato-Pance 07/09
        Pato-Pance 08/09
        Topacio 05/09
        etc.
    """

# ============================================================
# NO TURNOS AP / PL CONSECUTIVOS
# ============================================================

def agregar_restriccion_no_bloques_consecutivos(
    model,
    x,
    personal,
    turnos_df
):

    """
    Impide que una persona haga dos bloques consecutivos entre:

    - Amor y Paz
    - Pato-Leonera

    Ejemplo NO permitido:

    AP-01 → 05/09 al 08/09
    PL-02 → 09/09 al 12/09

    Tampoco:

    PL-01 → 05/09 al 08/09
    AP-02 → 09/09 al 12/09
    """

    bloques = turnos_df[
        turnos_df["puesto"].isin(
            ["Amor y Paz", "Pato-Leonera"]
        )
    ].index.tolist()

    for p in personal.index:

        for t1 in bloques:

            fin_1 = turnos_df.loc[
                t1,
                "fecha_fin"
            ]

            for t2 in bloques:

                if t1 == t2:
                    continue

                inicio_2 = turnos_df.loc[
                    t2,
                    "fecha_inicio"
                ]

                # El segundo bloque empieza
                # exactamente al día siguiente

                if inicio_2 == fin_1 + pd.Timedelta(days=1):

                    model.Add(

                        x[(p, t1)]
                        +
                        x[(p, t2)]

                        <= 1

                    )




    # --------------------------------------------------------
    # Comparar cada par de turnos
    # --------------------------------------------------------

    turnos = list(turnos_df.index)

    for p in personal.index:

        for i in range(len(turnos)):

            t1 = turnos[i]

            inicio_1 = turnos_df.loc[
                t1,
                "fecha_inicio"
            ]

            fin_1 = turnos_df.loc[
                t1,
                "fecha_fin"
            ]

            for j in range(i + 1, len(turnos)):

                t2 = turnos[j]

                inicio_2 = turnos_df.loc[
                    t2,
                    "fecha_inicio"
                ]

                fin_2 = turnos_df.loc[
                    t2,
                    "fecha_fin"
                ]

                # ------------------------------------------------
                # Determinar si los períodos se solapan
                # ------------------------------------------------

                hay_solapamiento = (
                    inicio_1 <= fin_2
                    and
                    inicio_2 <= fin_1
                )

                if hay_solapamiento:

                    model.Add(
                        x[(p, t1)]
                        +
                        x[(p, t2)]
                        <= 1
                    )


# ============================================================
# CONSTRUIR MODELO BASE
# ============================================================

def construir_modelo_base(
    personal,
    turnos_df
):
    """
    Construye el modelo base completo.

    Incluye:

        1. Variables
        2. Cobertura
        3. Elegibilidad
        4. No solapamiento

    Todavía NO incluye:

        - Sexo
        - Conductores
        - Transporte
        - PVC
        - Anchicaya semanal
        - Balance de carga
        - Función objetivo
    """

    model = crear_modelo()

    x = crear_variables(
        model,
        personal,
        turnos_df
    )

    agregar_restriccion_cobertura(
        model,
        x,
        personal,
        turnos_df
    )

    agregar_restriccion_elegibilidad(
        model,
        x,
        personal,
        turnos_df
    )

    agregar_restriccion_no_solapamiento(
        model,
        x,
        personal,
        turnos_df
    )

    agregar_restriccion_no_bloques_consecutivos(
        model,
        x,
        personal,
        turnos_df

    )

    return model, x