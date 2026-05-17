import pandas as pd


# =========================
# IMPRIMIR ASIGNACIONES
# =========================

def imprimir_asignaciones(

    solver,
    x,
    personal,
    turnos_df

):

    """
    Imprime todas las asignaciones
    generadas por el solver.
    """

    print("\n=== ASIGNACIONES ===")

    for t in turnos_df.index:

        turno = turnos_df.loc[t]

        print(

            f"\n{turno['fecha']} | "
            f"{turno['puesto']} | "
            f"{turno['horario']}"

        )

        for p in personal.index:

            if solver.Value(x[(p, t)]) == 1:

                print(

                    "-",
                    personal.loc[p, "nombre"]

                )


# =========================
# RESUMEN DE CARGA
# =========================

def crear_resumen_carga(

    solver,
    x,
    personal,
    turnos_df

):

    """
    Genera tabla resumen
    de carga operativa.
    """

    resumen = []

    for p in personal.index:

        nombre = personal.loc[p, "nombre"]

        estrategia = personal.loc[
            p,
            "estrategia"
        ]

        # =====================
        # CONDUCTOR
        # =====================

        carro = (

            personal.loc[
                p,
                "conductor_carro"
            ] == "SI"

        )

        moto = (

            personal.loc[
                p,
                "conductor_moto"
            ] == "SI"

        )

        if carro and moto:

            conductor = "CARRO y MOTO"

        elif carro:

            conductor = "CARRO"

        elif moto:

            conductor = "MOTO"

        else:

            conductor = "NO"

        # =====================
        # CONTADORES
        # =====================

        arbolito_dia = 0
        arbolito_noche = 0
        pato_pance = 0

        for t in turnos_df.index:

            if solver.Value(x[(p, t)]) == 1:

                puesto = turnos_df.loc[
                    t,
                    "puesto"
                ]

                horario = turnos_df.loc[
                    t,
                    "horario"
                ]

                # Arbolito día

                if (

                    puesto == "Arbolito"

                    and

                    horario == "dia"

                ):

                    arbolito_dia += 1

                # Arbolito noche

                elif (

                    puesto == "Arbolito"

                    and

                    horario == "noche"

                ):

                    arbolito_noche += 1

                # Pato

                elif puesto == "Pato Pance":

                    pato_pance += 1

        total = (

            arbolito_dia
            +
            arbolito_noche
            +
            pato_pance

        )

        resumen.append({

            "nombre": nombre,
            "estrategia": estrategia,
            "conductor": conductor,
            "arbolito_dia": arbolito_dia,
            "arbolito_noche": arbolito_noche,
            "pato_pance": pato_pance,
            "total": total

        })

    resumen_df = pd.DataFrame(
        resumen
    )

    resumen_df = resumen_df.sort_values(

        by="total",
        ascending=False

    )

    return resumen_df