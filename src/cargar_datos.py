import pandas as pd


def cargar_datos(ruta_excel):

    # ========================================================
    # PERSONAL
    # ========================================================

    personal = pd.read_excel(
        ruta_excel,
        sheet_name="Personal"
    )

    personal.columns = (
        personal.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # ========================================================
    # CALENDARIO
    # ========================================================

    calendario = pd.read_excel(
        ruta_excel,
        sheet_name="Calendario"
    )

    calendario.columns = (
        calendario.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    calendario["fecha"] = pd.to_datetime(
        calendario["fecha"]
    )

    calendario["tipo_dia"] = (
        calendario["tipo_dia"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    calendario["festivo"] = (
        calendario["festivo"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # ========================================================
    # CONFIGURACIÓN DE PUESTOS
    # ========================================================

    configuracion_puestos = pd.read_excel(
        ruta_excel,
        sheet_name="Configuracion_Puestos"
    )

    configuracion_puestos.columns = (
        configuracion_puestos.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Convertir fechas

    if "fecha_inicio" in configuracion_puestos.columns:

        configuracion_puestos["fecha_inicio"] = (
            pd.to_datetime(
                configuracion_puestos["fecha_inicio"],
                errors="coerce"
            )
        )

    return (
        personal,
        calendario,
        configuracion_puestos
    )