def crear_grupos_cargo(personal):

    grupos = {
        "operario": [],
        "tecnico": [],
        "tecnologo": [],
        "profesional": []
    }

    for p in personal.index:

        cargo = (
            str(personal.loc[p, "cargo"])
            .strip()
            .lower()
        )

        if cargo in grupos:
            grupos[cargo].append(p)

    return grupos