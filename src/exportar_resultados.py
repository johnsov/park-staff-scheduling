import pandas as pd


def crear_tabla_asignaciones(
    solver,
    x,
    personal,
    turnos_df
):
    filas = []

    for t in turnos_df.index:

        turno = turnos_df.loc[t]

        for p in personal.index:

            if solver.Value(x[(p, t)]) == 1:

                filas.append({
                    "id_turno": turno["id"],
                    "puesto": turno["puesto"],
                    "fecha_inicio": turno["fecha_inicio"],
                    "fecha_fin": turno["fecha_fin"],
                    "duracion_dias": turno["duracion_dias"],
                    "nombre": personal.loc[p, "nombre"],
                    "cargo": personal.loc[p, "cargo"],
                    "estrategia": personal.loc[p, "estrategia"],
                    "sexo": personal.loc[p, "sexo"],
                    "conductor_carro": personal.loc[
                        p, "conductor_carro"
                    ]
                })

    return pd.DataFrame(filas)


def exportar_excel(
    solver,
    x,
    personal,
    turnos_df,
    archivo_salida
):

    asignaciones = crear_tabla_asignaciones(
        solver,
        x,
        personal,
        turnos_df
    )

    resumen_carga = crear_resumen_carga(
    solver,
    x,
    personal,
    turnos_df
    )

    with pd.ExcelWriter(
        archivo_salida,
        engine="openpyxl"
    ) as writer:

        # Asignaciones detalladas
        asignaciones.to_excel(
            writer,
            sheet_name="Asignaciones",
            index=False
        )

        # Información de los turnos
        turnos_df.to_excel(
            writer,
            sheet_name="Turnos",
            index=False
        )

        resumen_carga.to_excel(
            writer,
            sheet_name="Resumen_Carga",
            index=False
        )

    print(f"\n✓ Excel exportado:")
    print(archivo_salida)

    return asignaciones





def crear_resumen_carga(
    solver,
    x,
    personal,
    turnos_df
):
    filas = []

    for p in personal.index:

        # ---------------------------------------------
        # CARGA POR PUESTO (DÍAS TRABAJADOS)
        # ---------------------------------------------

        amor_paz = sum(
            solver.Value(x[(p, t)])
            * int(turnos_df.loc[t, "duracion_dias"])
            for t in turnos_df.index
            if turnos_df.loc[t, "puesto"] == "Amor y Paz"
        )

        pato_leonera = sum(
            solver.Value(x[(p, t)])
            * int(turnos_df.loc[t, "duracion_dias"])
            for t in turnos_df.index
            if turnos_df.loc[t, "puesto"] == "Pato-Leonera"
        )

        pato_pance = sum(
            solver.Value(x[(p, t)])
            * int(turnos_df.loc[t, "duracion_dias"])
            for t in turnos_df.index
            if turnos_df.loc[t, "puesto"] == "Pato-Pance"
        )

        topacio = sum(
            solver.Value(x[(p, t)])
            * int(turnos_df.loc[t, "duracion_dias"])
            for t in turnos_df.index
            if turnos_df.loc[t, "puesto"] == "Topacio"
        )

        # ---------------------------------------------
        # TOTAL DE DÍAS TRABAJADOS
        # ---------------------------------------------

        total_dias = (
            amor_paz
            + pato_leonera
            + pato_pance
            + topacio
        )

        filas.append({

            "nombre": personal.loc[p, "nombre"],

            "cargo": personal.loc[p, "cargo"],

            "estrategia": personal.loc[p, "estrategia"],

            "conductor_carro": personal.loc[
                p,
                "conductor_carro"
            ],

            "Amor y Paz (días)": amor_paz,

            "Pato-Leonera (días)": pato_leonera,

            "Pato-Pance (días)": pato_pance,

            "Topacio (días)": topacio,

            "TOTAL DÍAS": total_dias
        })

    resumen = pd.DataFrame(filas)

    return resumen.sort_values(
        by=["TOTAL DÍAS", "cargo"],
        ascending=[False, True]
    ).reset_index(drop=True)