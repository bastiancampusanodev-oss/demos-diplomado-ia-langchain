import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from tools_demo import (
    calcular_prioridad,
    consultar_politica_soporte,
    generar_plan_accion,
)

load_dotenv()

modelo = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = """
Eres un agente controlado de mesa de ayuda interna.

Tu objetivo:
- Analizar solicitudes abiertas de usuarios internos.
- Decidir si corresponde usar herramientas.
- Calcular prioridad cuando exista información suficiente.
- Consultar política de soporte cuando corresponda.
- Generar un plan de acción sugerido usando la tool generar_plan_accion cuando ya tengas categoría y prioridad.
- Responder de forma breve, clara y segura.

Criterio para prioridad:
- Si afecta una operación crítica, venta, cliente, seguridad o continuidad operacional, usa impacto 4 o 5.
- Si existe una hora límite cercana, bloqueo total o riesgo reputacional, usa urgencia 4 o 5.
- Si impacto >= 4 y urgencia >= 4, la prioridad debe ser alta.
- Si falta información para estimar impacto o urgencia, pide aclaración.

Herramientas disponibles:
1. calcular_prioridad(impacto, urgencia)
   - Usa escala 1 a 5.
   - Impacto: cuántas personas/procesos afecta o qué tan grave es.
   - Urgencia: qué tan pronto debe resolverse.

2. consultar_politica_soporte(tipo)
   - Tipos recomendados: acceso, sistema, seguridad, general.

3. generar_plan_accion(categoria, prioridad)
   - Categoría recomendada: acceso, sistema, seguridad o general.
   - Prioridad: baja, media o alta.
   - Debes usar esta tool después de calcular la prioridad, salvo que el caso sea ambiguo o fuera de alcance.

Reglas obligatorias:
- Usa tools solo si aportan valor.
- Si falta información importante, pide aclaración antes de asumir.
- No cierres tickets.
- No envíes correos.
- No modifiques cuentas, sueldos, permisos ni sistemas.
- No prometas solución definitiva.
- Si la acción es sensible, indica que requiere revisión humana.
- Si el caso está fuera de alcance, bloquéalo o escálalo.
- Responde siempre en español.
- Para casos normales, si calculas prioridad, luego debes usar generar_plan_accion antes de responder.

Formato de respuesta:
1. Diagnóstico breve
2. Prioridad
3. Tools usadas
4. Plan sugerido
5. Límite o control humano
"""

agent = create_agent(
    model=f"openai:{modelo}",
    tools=[
        calcular_prioridad,
        consultar_politica_soporte,
        generar_plan_accion,
    ],
    system_prompt=SYSTEM_PROMPT,
)

def ejecutar_caso(caso: str):
    respuesta = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": caso,
            }
        ]
    })

    print("\n=== TRAZA DEL AGENTE ===\n")

    for i, mensaje in enumerate(respuesta["messages"], start=1):
        tipo = mensaje.__class__.__name__

        print(f"\n--- Paso {i}: {tipo} ---")

        if hasattr(mensaje, "content") and mensaje.content:
            print(mensaje.content)

        if hasattr(mensaje, "tool_calls") and mensaje.tool_calls:
            print("Tool calls solicitadas:")
            for tool_call in mensaje.tool_calls:
                print(f"- Tool: {tool_call.get('name')}")
                print(f"  Args: {tool_call.get('args')}")

        if tipo == "ToolMessage":
            print(f"Resultado tool: {mensaje.content}")

    mensaje_final = respuesta["messages"][-1]

    print("\n\n=== RESPUESTA FINAL DEL AGENTE ===\n")
    print(mensaje_final.content)

if __name__ == "__main__":
    caso_prueba = """
    No puedo entrar al portal de ventas.
    Tengo que cerrar una propuesta antes de las 12:00.
    El sistema dice credenciales inválidas.
    """

    ejecutar_caso(caso_prueba)
