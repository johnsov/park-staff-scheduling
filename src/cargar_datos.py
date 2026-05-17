import pandas as pd


def cargar_datos(ruta_excel):

    # =========================
    # CARGAR
    # =========================

    personal = pd.read_excel(
        ruta_excel,
        sheet_name="Personal"
    )

    calendario = pd.read_excel(
        ruta_excel,
        sheet_name="Calendario"
    )

    # =========================
    # LIMPIAR COLUMNAS
    # =========================

    personal.columns = (
        personal.columns
        .str.strip()
        .str.lower()
    )

    # =========================
    # NORMALIZAR SI/NO
    # =========================

    columnas_si_no = [

        "activo",
        "puede_arbolito",
        "puede_noche_arbolito",
        "puede_pato",
        "conductor_carro",
        "conductor_moto",
        "ecoturismo"

    ]

    for col in columnas_si_no:

        personal[col] = (

            personal[col]
            .astype(str)
            .str.strip()
            .str.upper()

        )

    return personal, calendario