from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agente_demo import agent


app = FastAPI(title="Demo Agente Clase 4")

app.mount("/static", StaticFiles(directory="static"), name="static")


class CasoRequest(BaseModel):
    caso: str


def construir_traza(messages) -> str:
    lineas = []

    for i, mensaje in enumerate(messages, start=1):
        tipo = mensaje.__class__.__name__
        lineas.append(f"--- Paso {i}: {tipo} ---")

        if hasattr(mensaje, "content") and mensaje.content:
            lineas.append(str(mensaje.content))

        if hasattr(mensaje, "tool_calls") and mensaje.tool_calls:
            lineas.append("Tool calls solicitadas:")
            for tool_call in mensaje.tool_calls:
                lineas.append(f"- Tool: {tool_call.get('name')}")
                lineas.append(f"  Args: {tool_call.get('args')}")

        if tipo == "ToolMessage":
            lineas.append(f"Resultado tool: {mensaje.content}")

        lineas.append("")

    return "\n".join(lineas)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/agente")
def ejecutar_agente(request: CasoRequest):
    if not request.caso.strip():
        raise HTTPException(status_code=400, detail="El caso no puede estar vacío.")

    try:
        respuesta = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": request.caso,
                }
            ]
        })

        messages = respuesta["messages"]
        mensaje_final = messages[-1]

        return {
            "respuesta_final": mensaje_final.content,
            "traza": construir_traza(messages),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))