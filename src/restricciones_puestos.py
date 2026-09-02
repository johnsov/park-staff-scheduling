from ortools.sat.python import cp_model
import unicodedata


# ============================================================
# NORMALIZAR TEXTO
# ============================================================

def normalizar_texto(valor):
    """
    Convierte un texto a una forma estándar:

        "Sábado"  → "sabado"
        " SÁBADO " → "sabado"
        "Domingo" → "domingo"

    Esto evita problemas con tildes, mayúsculas
    y espacios provenientes del Excel.
    """

    texto = str(valor).strip().lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto


# ============================================================
# PATO-PANCE
# ============================================================

def agregar_restricciones_pato_pance(
    model,
    x,
    personal,
    turnos_df
):
    """
    Restricciones específicas de Pato-Pance.

    Reglas:

    - 5 personas por turno
    - Exactamente 1 persona de Ecoturismo
    - Exactamente 1 conductor de carro
    - Las personas de Anchicaya no pueden asistir
    - Marianne Hoyos no puede asistir
    - Felipe Garcia no puede asistir
    - Esmeralda Acosta no puede asistir los sábados
    - Cristian Libreros no puede asistir los sábados
    """

    turnos_pp = turnos_df[
        turnos_df["puesto"] == "Pato-Pance"
    ].index.tolist()

    # --------------------------------------------------------
    # PERSONAS DE ECOTURISMO
    # --------------------------------------------------------

    ecoturismo = personal[
        personal["ecoturismo"] == "SI"
    ].index.tolist()

    # --------------------------------------------------------
    # CONDUCTORES DE CARRO
    # --------------------------------------------------------

    conductores_carro = personal[
        personal["conductor_carro"] == "SI"
    ].index.tolist()

    # --------------------------------------------------------
    # RECORRER TURNOS
    # --------------------------------------------------------

    for t in turnos_pp:

        tipo_dia = normalizar_texto(
            turnos_df.loc[t, "tipo_dia"]
        )

        # ====================================================
        # EXACTAMENTE 1 PERSONA DE ECOTURISMO
        # ====================================================

        model.Add(
            sum(
                x[(p, t)]
                for p in ecoturismo
            )
            == 1
        )

        # ====================================================
        # EXACTAMENTE 1 CONDUCTOR DE CARRO
        # ====================================================

        model.Add(
            sum(
                x[(p, t)]
                for p in conductores_carro
            )
            == 1
        )

        # ====================================================
        # RESTRICCIONES INDIVIDUALES
        # ====================================================

        for p in personal.index:

            nombre = normalizar_texto(
                personal.loc[p, "nombre"]
            )

            estrategia = normalizar_texto(
                personal.loc[p, "estrategia"]
            )

            # ------------------------------------------------
            # Marianne Hoyos
            # ------------------------------------------------

            if nombre == "marianne hoyos":

                model.Add(
                    x[(p, t)] == 0
                )

            # ------------------------------------------------
            # Felipe Garcia
            # ------------------------------------------------

            if nombre == "felipe garcia":

                model.Add(
                    x[(p, t)] == 0
                )

            # ------------------------------------------------
            # Esmeralda Acosta
            # No puede trabajar sábados
            # ------------------------------------------------

            if (
                nombre == "esmeralda acosta"
                and tipo_dia == "sabado"
            ):

                model.Add(
                    x[(p, t)] == 0
                )

            # ------------------------------------------------
            # Cristian Libreros
            # No puede trabajar sábados
            # ------------------------------------------------

            if (
                nombre == "cristian libreros"
                and tipo_dia == "sabado"
            ):

                model.Add(
                    x[(p, t)] == 0
                )

            # ------------------------------------------------
            # Anchicaya
            # No hace Pato-Pance
            # ------------------------------------------------

            if estrategia == "anchicaya":

                model.Add(
                    x[(p, t)] == 0
                )


# ============================================================
# TOPACIO
# ============================================================

def agregar_restricciones_topacio(
    model,
    x,
    personal,
    turnos_df
):
    """
    Restricciones específicas de Topacio.

    Reglas:

    - 1 persona por turno
    - No puede pertenecer a Ecoturismo
    - Marianne Hoyos no puede asistir
    - Personas de Anchicaya no pueden asistir
    """

    turnos_topacio = turnos_df[
        turnos_df["puesto"] == "Topacio"
    ].index.tolist()

    for t in turnos_topacio:

        for p in personal.index:

            # =================================================
            # ECOTURISMO
            # =================================================

            if personal.loc[p, "ecoturismo"] == "SI":

                model.Add(
                    x[(p, t)] == 0
                )

            # =================================================
            # MARIANNE HOYOS
            # =================================================

            if normalizar_texto(
                personal.loc[p, "nombre"]
            ) == "marianne hoyos":

                model.Add(
                    x[(p, t)] == 0
                )

            # =================================================
            # ANCHICAYA
            # =================================================

            if normalizar_texto(
                personal.loc[p, "estrategia"]
            ) == "anchicaya":

                model.Add(
                    x[(p, t)] == 0
                )


# ============================================================
# TODAS LAS RESTRICCIONES DE PUESTOS
# ============================================================

def agregar_restricciones_puestos(
    model,
    x,
    personal,
    turnos_df
):
    """
    Agrega las restricciones de:

        - Pato-Pance
        - Topacio
    """

    agregar_restricciones_pato_pance(
        model,
        x,
        personal,
        turnos_df
    )

    agregar_restricciones_topacio(
        model,
        x,
        personal,
        turnos_df
    )