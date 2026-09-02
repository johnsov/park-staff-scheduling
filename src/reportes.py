import pandas as pd


# ============================================================
# IMPRIMIR ASIGNACIONES
# ============================================================

def imprimir_asignaciones(
    solver,
    x,
    personal,
    turnos_df
):

    print("\n=== ASIGNACIONES ===")

    for t in turnos_df.index:

        turno = turnos_df.loc[t]

        print(
            f"\n{turno['id']} | "
            f"{turno['fecha_inicio'].date()} - "
            f"{turno['fecha_fin'].date()} | "
            f"{turno['puesto']} | "
            f"{turno['horario']}"
        )

        for p in personal.index:

            if solver.Value(x[(p, t)]) == 1:

                print(
                    "-",
                    personal.loc[p, "nombre"]
                )


# ============================================================
# RESUMEN DE CARGA
# ============================================================

def crear_resumen_carga(
    solver,
    x,
    personal,
    turnos_df
):

    resumen = []

    for p in personal.index:

        nombre = personal.loc[p, "nombre"]
        cargo = personal.loc[p, "cargo"]
        estrategia = personal.loc[p, "estrategia"]
        activo = personal.loc[p, "activo"]

        # ----------------------------------------------------
        # CONDUCTOR
        # ----------------------------------------------------

        carro = (
            personal.loc[p, "conductor_carro"] == "SI"
        )

        moto = (
            personal.loc[p, "conductor_moto"] == "SI"
        )

        if carro and moto:
            conductor = "CARRO y MOTO"

        elif carro:
            conductor = "CARRO"

        elif moto:
            conductor = "MOTO"

        else:
            conductor = "NO"

        # ----------------------------------------------------
        # CONTADORES
        # ----------------------------------------------------

        amor_paz = 0
        pato_leonera = 0
        pato_pance = 0
        topacio = 0

        # ----------------------------------------------------
        # RECORRER ASIGNACIONES
        # ----------------------------------------------------

        for t in turnos_df.index:

            if solver.Value(x[(p, t)]) != 1:
                continue

            puesto = turnos_df.loc[t, "puesto"]

            if puesto == "Amor y Paz":
                amor_paz += int(
                    turnos_df.loc[
                        t,
                        "duracion_dias"
                    ]
                )

            elif puesto == "Pato-Leonera":
                pato_leonera += int(
                    turnos_df.loc[
                        t,
                        "duracion_dias"
                    ]
                )

            elif puesto == "Pato-Pance":
                pato_pance += 1

            elif puesto == "Topacio":
                topacio += 1

        # ----------------------------------------------------
        # TOTAL
        # ----------------------------------------------------

        total = (
            amor_paz
            + pato_leonera
            + pato_pance
            + topacio
        )

        resumen.append({

            "nombre": nombre,
            "cargo": cargo,
            "estrategia": estrategia,
            "activo": activo,
            "conductor": conductor,

            "amor_y_paz": amor_paz,
            "pato_leonera": pato_leonera,
            "pato_pance": pato_pance,
            "topacio": topacio,

            "total_puestos": total

        })

    resumen_df = pd.DataFrame(resumen)

    resumen_df = resumen_df.sort_values(
        by="total_puestos",
        ascending=False
    ).reset_index(drop=True)

    return resumen_df


# ============================================================
# RESUMEN POR CARGO
# ============================================================

def crear_resumen_por_cargo(resumen_df):

    resumen_cargo = (

        resumen_df

        .groupby("cargo")

        .agg(

            personas=("nombre", "count"),

            puestos_totales=(
                "total_puestos",
                "sum"
            ),

            promedio_puestos=(
                "total_puestos",
                "mean"
            ),

            minimo_puestos=(
                "total_puestos",
                "min"
            ),

            maximo_puestos=(
                "total_puestos",
                "max"
            )

        )

        .round(2)

        .reset_index()

    )

    return resumen_cargo