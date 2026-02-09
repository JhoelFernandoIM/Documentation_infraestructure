def validar_obra(nombre_obra, presupuesto):
    if not nombre_obra:
        return False, "El nombre de la obra es obligatorio"

    if presupuesto <= 0:
        return False, "El presupuesto debe ser mayor a cero"

    return True, ""
