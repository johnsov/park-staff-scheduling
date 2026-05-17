import pandas as pd


def crear_turnos(calendario):

    """
    Genera automáticamente los turnos
    de control a partir del calendario.
    """

    turnos = []

    for _, fila in calendario.iterrows():

        fecha = fila["fecha"]

        tipo_dia = (
            str(fila["tipo_dia"])
            .strip()
            .lower()
        )

        festivo = (
            str(fila["festivo"])
            .strip()
            .upper()
        )

        # =========================
        # ARBOLITO DÍA
        # =========================

        turnos.append({

            "fecha": fecha,
            "puesto": "Arbolito",
            "horario": "dia",
            "personas": 2

        })

        # =========================
        # ARBOLITO NOCHE
        # =========================

        turnos.append({

            "fecha": fecha,
            "puesto": "Arbolito",
            "horario": "noche",
            "personas": 3

        })

        # =========================
        # PATO PANCE
        # =========================

        if (
            tipo_dia in ["sabado", "domingo"]
            or festivo == "SI"
        ):

            turnos.append({

                "fecha": fecha,
                "puesto": "Pato Pance",
                "horario": "dia",
                "personas": 4

            })

    # =========================
    # DATAFRAME FINAL
    # =========================

    turnos_df = pd.DataFrame(turnos)

    return turnos_df