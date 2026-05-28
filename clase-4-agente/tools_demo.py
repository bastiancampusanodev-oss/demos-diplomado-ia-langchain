from langchain_core.tools import tool


@tool
def calcular_prioridad(impacto: int, urgencia: int) -> str:
    """
    Calcula la prioridad de un caso usando impacto y urgencia en escala 1 a 5.
    Devuelve baja, media o alta.
    """
    if impacto < 1 or impacto > 5:
        return "Error: impacto debe estar entre 1 y 5."

    if urgencia < 1 or urgencia > 5:
        return "Error: urgencia debe estar entre 1 y 5."

    score = impacto * urgencia

    if score >= 16:
        return "alta"
    elif score >= 8:
        return "media"
    else:
        return "baja"


@tool
def consultar_politica_soporte(tipo: str) -> str:
    """
    Consulta una política ficticia de soporte interno según el tipo de incidente.
    Tipos disponibles: acceso, sistema, seguridad, general.
    """
    politicas = {
        "acceso": (
            "Para problemas de acceso, validar identidad del usuario, revisar bloqueo de cuenta "
            "y escalar a soporte TI si afecta una operación crítica."
        ),
        "sistema": (
            "Para fallas de sistema, revisar si existe incidente masivo, registrar evidencia "
            "y priorizar según impacto operativo."
        ),
        "seguridad": (
            "Para eventos de seguridad, no entregar credenciales, no modificar permisos sin autorización "
            "y escalar inmediatamente al equipo responsable."
        ),
        "general": (
            "Para solicitudes generales, recopilar antecedentes mínimos, clasificar el caso "
            "y derivar al equipo correspondiente."
        ),
    }

    tipo_normalizado = tipo.lower().strip()

    return politicas.get(
        tipo_normalizado,
        "No hay una política específica para ese tipo. Se recomienda pedir más información y derivar a soporte."
    )


@tool
def generar_plan_accion(categoria: str, prioridad: str) -> str:
    """
    Genera un plan de acción sugerido según categoría y prioridad.
    No ejecuta acciones reales.
    """
    categoria = categoria.lower().strip()
    prioridad = prioridad.lower().strip()

    pasos = [
        "1. Confirmar datos mínimos del usuario y del incidente.",
        "2. Registrar evidencia del problema reportado.",
    ]

    if categoria == "acceso":
        pasos.append("3. Revisar estado de cuenta, bloqueo o credenciales.")
    elif categoria == "sistema":
        pasos.append("3. Verificar si existe caída, error masivo o degradación del servicio.")
    elif categoria == "seguridad":
        pasos.append("3. Escalar inmediatamente al equipo de seguridad.")
    else:
        pasos.append("3. Clasificar el caso y derivar al equipo correspondiente.")

    if prioridad == "alta":
        pasos.append("4. Escalar a revisión humana prioritaria antes de ejecutar cambios.")
    elif prioridad == "media":
        pasos.append("4. Atender dentro del flujo normal de soporte con seguimiento.")
    else:
        pasos.append("4. Registrar y resolver según disponibilidad del equipo.")

    pasos.append("5. No cerrar el caso sin confirmar resolución con el usuario.")

    return "\n".join(pasos)
