def crear_grupos(personal):

    """
    Crea todos los grupos operativos
    necesarios para el modelo.
    """

    grupos = {}

    # =========================
    # PVC
    # =========================

    grupos["pvc"] = personal[

        personal["estrategia"] == "PVC"

    ].index.tolist()

    # =========================
    # NO PVC
    # =========================

    grupos["no_pvc"] = personal[

        personal["estrategia"] != "PVC"

    ].index.tolist()

    # =========================
    # CONDUCTORES CARRO
    # =========================

    grupos["conductores_carro"] = personal[

        personal["conductor_carro"] == "SI"

    ].index.tolist()

    # =========================
    # CONDUCTORES MOTO
    # =========================

    grupos["conductores_moto"] = personal[

        personal["conductor_moto"] == "SI"

    ].index.tolist()

    # =========================
    # ECOTURISMO
    # =========================

    grupos["ecoturismo"] = personal[

        personal["ecoturismo"] == "SI"

    ].index.tolist()

    # =========================
    # ANCHICAYÁ
    # =========================

    grupos["anchicaya"] = personal[

        personal["estrategia"] == "ANCHICAYA"

    ].index.tolist()

    # =========================
    # SIN ARBOLITO
    # =========================

    grupos["sin_arbolito"] = personal[

        personal["puede_arbolito"] != "SI"

    ].index.tolist()

    # =========================
    # NO PVC RESTRINGIDOS
    # =========================

    no_pvc_restringidos = []

    for p in grupos["no_pvc"]:

        es_ecoturismo = (

            personal.loc[p, "ecoturismo"] == "SI"

        )

        es_conductor = (

            personal.loc[p, "conductor_carro"] == "SI"

            or

            personal.loc[p, "conductor_moto"] == "SI"

        )

        if (
            not es_ecoturismo
            and not es_conductor
        ):

            no_pvc_restringidos.append(p)

    grupos["no_pvc_restringidos"] = (
        no_pvc_restringidos
    )

    return grupos