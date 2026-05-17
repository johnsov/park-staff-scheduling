from ortools.sat.python import cp_model
import pandas as pd

# =========================
# COBERTURA
# =========================

def agregar_restriccion_cobertura(
    model,
    x,
    personal,
    turnos_df
):

    """
    Cada turno debe tener exactamente
    la cantidad requerida de personas.
    """

    for t in turnos_df.index:

        personas_requeridas = (
            turnos_df.loc[t, "personas"]
        )

        model.Add(

            sum(
                x[(p, t)]
                for p in personal.index
            )

            == personas_requeridas

        )


# =========================
# ELEGIBILIDAD
# =========================

def agregar_restriccion_elegibilidad(
    model,
    x,
    personal,
    turnos_df
):

    """
    Restringe asignaciones inválidas:
    - inactivos
    - sin Arbolito
    - sin noche
    - sin Pato
    """

    for p in personal.index:

        for t in turnos_df.index:

            puesto = turnos_df.loc[t, "puesto"]

            horario = turnos_df.loc[t, "horario"]

            # =====================
            # SOLO ACTIVOS
            # =====================

            if (
                personal.loc[p, "activo"]
                != "SI"
            ):

                model.Add(
                    x[(p, t)] == 0
                )

            # =====================
            # ARBOLITO
            # =====================

            if puesto == "Arbolito":

                if (

                    personal.loc[
                        p,
                        "puede_arbolito"
                    ] != "SI"

                ):

                    model.Add(
                        x[(p, t)] == 0
                    )

                # NOCHE

                if horario == "noche":

                    if (

                        personal.loc[
                            p,
                            "puede_noche_arbolito"
                        ] != "SI"

                    ):

                        model.Add(
                            x[(p, t)] == 0
                        )

            # =====================
            # PATO PANCE
            # =====================

            if puesto == "Pato Pance":

                if (

                    personal.loc[
                        p,
                        "puede_pato"
                    ] != "SI"

                ):

                    model.Add(
                        x[(p, t)] == 0
                    )


# =========================
# NO DOBLE TURNO
# =========================

def agregar_restriccion_no_doble_turno(
    model,
    x,
    personal,
    turnos_df
):

    """
    Una persona no puede trabajar
    más de un turno el mismo día.
    """

    for p in personal.index:

        for fecha in turnos_df[
            "fecha"
        ].unique():

            turnos_mismo_dia = []

            for t in turnos_df.index:

                if (
                    turnos_df.loc[t, "fecha"]
                    == fecha
                ):

                    turnos_mismo_dia.append(
                        x[(p, t)]
                    )

            model.Add(

                sum(turnos_mismo_dia)

                <= 1

            )


# =========================
# TRANSPORTE
# =========================

def agregar_restriccion_transporte(

    model,
    x,
    turnos_df,
    conductores_carro,
    conductores_moto

):

    """
    Restricciones logísticas de transporte:

    - Arbolito noche:
      obligatorio carro

    - Arbolito día:
      mínimo 1 conductor
      (carro o moto)

    - Pato Pance:
      mínimo:
        1 carro
        O
        2 motos
    """

    for t in turnos_df.index:

        puesto = turnos_df.loc[t, "puesto"]

        horario = turnos_df.loc[t, "horario"]

        # =====================
        # ARBOLITO NOCHE
        # =====================

        if (
            puesto == "Arbolito"
            and horario == "noche"
        ):

            model.Add(

                sum(

                    x[(p, t)]

                    for p in conductores_carro

                )

                >= 1

            )

        # =====================
        # ARBOLITO DÍA
        # =====================

        elif (
            puesto == "Arbolito"
            and horario == "dia"
        ):

            model.Add(

                sum(

                    x[(p, t)]

                    for p in (

                        conductores_carro
                        +
                        conductores_moto

                    )

                )

                >= 1

            )

        # =====================
        # PATO PANCE
        # =====================

        elif puesto == "Pato Pance":

            carro_expr = sum(

                x[(p, t)]

                for p in conductores_carro

            )

            moto_expr = sum(

                x[(p, t)]

                for p in conductores_moto

            )

            # =====================
            # VARIABLES AUXILIARES
            # =====================

            tiene_carro = model.NewBoolVar(
                f"carro_{t}"
            )

            dos_motos = model.NewBoolVar(
                f"motos_{t}"
            )

            # =====================
            # CONDICIONES
            # =====================

            model.Add(
                carro_expr >= 1
            ).OnlyEnforceIf(
                tiene_carro
            )

            model.Add(
                carro_expr == 0
            ).OnlyEnforceIf(
                tiene_carro.Not()
            )

            model.Add(
                moto_expr >= 2
            ).OnlyEnforceIf(
                dos_motos
            )

            model.Add(
                moto_expr < 2
            ).OnlyEnforceIf(
                dos_motos.Not()
            )

            # =====================
            # REGLA FINAL
            # =====================

            model.AddBoolOr([

                tiene_carro,
                dos_motos

            ])


# =========================
# ECOTURISMO EN PATO
# =========================

def agregar_restriccion_ecoturismo(

    model,
    x,
    turnos_df,
    ecoturismo

):

    """
    Cada turno de Pato Pance
    debe tener mínimo una persona
    de ecoturismo.
    """

    for t in turnos_df.index:

        puesto = turnos_df.loc[t, "puesto"]

        if puesto == "Pato Pance":

            model.Add(

                sum(

                    x[(p, t)]

                    for p in ecoturismo

                )

                >= 1

            )


# =========================
# NO MÁS DE 2 PATOS SEGUIDOS
# =========================

def agregar_restriccion_patitos(

    model,
    x,
    personal,
    turnos_pato

):

    """
    Evita que una persona haga
    3 turnos consecutivos
    de Pato Pance.
    """

    for p in personal.index:

        for i in range(
            len(turnos_pato) - 2
        ):

            t1 = turnos_pato[i]
            t2 = turnos_pato[i + 1]
            t3 = turnos_pato[i + 2]

            model.Add(

                x[(p, t1)]

                +

                x[(p, t2)]

                +

                x[(p, t3)]

                <= 2

            )


# =========================
# ANCHICAYÁ
# =========================

def agregar_restriccion_anchicaya(

    model,
    x,
    personal,
    turnos_df,
    anchicaya

):

    """
    Personas de Anchicayá:

    - solo Arbolito noche
    - máximo 1 vez por semana
    """

    # =====================
    # SOLO ARBOLITO NOCHE
    # =====================

    for p in anchicaya:

        for t in turnos_df.index:

            puesto = turnos_df.loc[t, "puesto"]

            horario = turnos_df.loc[t, "horario"]

            if not (

                puesto == "Arbolito"

                and

                horario == "noche"

            ):

                model.Add(
                    x[(p, t)] == 0
                )

    # =====================
    # SEMANAS
    # =====================

    turnos_df["semana"] = (

        pd.to_datetime(
            turnos_df["fecha"]
        )

        .dt.isocalendar()

        .week

    )

    # =====================
    # MÁXIMO 1 POR SEMANA
    # =====================

    for p in anchicaya:

        for semana in turnos_df[
            "semana"
        ].unique():

            turnos_semana = []

            for t in turnos_df.index:

                if (

                    turnos_df.loc[t, "semana"]

                    == semana

                    and

                    turnos_df.loc[t, "puesto"]

                    == "Arbolito"

                    and

                    turnos_df.loc[t, "horario"]

                    == "noche"

                ):

                    turnos_semana.append(
                        x[(p, t)]
                    )

            model.Add(

                sum(turnos_semana)

                <= 1

            )