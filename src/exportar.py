import pandas as pd


# =========================
# EXPORTAR SISTEMA COMPLETO
# =========================

def exportar_resultados(

    solver,
    x,
    personal,
    turnos_df,
    resumen_df,
    ruta_salida

):

    """
    Exporta:

    - asignaciones
    - resumen de carga
    - estadísticas

    a un solo archivo Excel.
    """

    # ==================================
    # ASIGNACIONES
    # ==================================

    filas = []

    for t in turnos_df.index:

        turno = turnos_df.loc[t]

        for p in personal.index:

            if solver.Value(x[(p, t)]) == 1:

                filas.append({

                    "fecha": turno["fecha"],
                    "puesto": turno["puesto"],
                    "horario": turno["horario"],
                    "nombre": personal.loc[p, "nombre"],
                    "estrategia": personal.loc[
                        p,
                        "estrategia"
                    ]

                })

    asignaciones_df = pd.DataFrame(
        filas
    )

    # ==================================
    # ESTADÍSTICAS
    # ==================================

    estadisticas = []

    # Total asignaciones

    total_turnos = resumen_df[
        "total"
    ].sum()

    estadisticas.append({

        "indicador": "Total asignaciones",
        "valor": total_turnos

    })

    # Promedio carga

    promedio = resumen_df[
        "total"
    ].mean()

    estadisticas.append({

        "indicador": "Promedio carga",
        "valor": round(promedio, 2)

    })

    # Máxima carga

    maxima = resumen_df[
        "total"
    ].max()

    estadisticas.append({

        "indicador": "Máxima carga",
        "valor": maxima

    })

    # Personas sin carga

    sin_carga = len(

        resumen_df[
            resumen_df["total"] == 0
        ]

    )

    estadisticas.append({

        "indicador": "Personas sin carga",
        "valor": sin_carga

    })

    # Total PVC

    total_pvc = len(

        resumen_df[
            resumen_df["estrategia"] == "PVC"
        ]

    )

    estadisticas.append({

        "indicador": "Total personas PVC",
        "valor": total_pvc

    })

    estadisticas_df = pd.DataFrame(
        estadisticas
    )

    # ==================================
    # EXPORTAR EXCEL
    # ==================================

    with pd.ExcelWriter(
        ruta_salida,
        engine="openpyxl"
    ) as writer:

        asignaciones_df.to_excel(

            writer,

            sheet_name="Asignaciones",

            index=False

        )

        resumen_df.to_excel(

            writer,

            sheet_name="Resumen_Carga",

            index=False

        )

        estadisticas_df.to_excel(

            writer,

            sheet_name="Estadisticas",

            index=False

        )

    print(
        f"\nArchivo exportado:\n{ruta_salida}"
    )