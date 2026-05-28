from tools_demo import calcular_prioridad, consultar_politica_soporte, generar_plan_accion


print("=== Prueba 1: calcular prioridad ===")
resultado_prioridad = calcular_prioridad.invoke({
    "impacto": 5,
    "urgencia": 4
})
print(resultado_prioridad)


print("\n=== Prueba 2: consultar política ===")
resultado_politica = consultar_politica_soporte.invoke({
    "tipo": "acceso"
})
print(resultado_politica)


print("\n=== Prueba 3: generar plan ===")
resultado_plan = generar_plan_accion.invoke({
    "categoria": "acceso",
    "prioridad": "alta"
})
print(resultado_plan)
