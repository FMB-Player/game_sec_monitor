def calcular_estadisticas_globales(sesiones: list[dict]) -> dict[str, int | float]:
    # Retorna un diccionario con las métricas consolidadas
    return {
        "total_sesiones": _calculcar_total_sesiones(sesiones),
        "ping_promedio": _calcular_valor_avg(sesiones, "ping_promedio"),
        "duracion_promedio": _calcular_valor_avg(sesiones, "duracion_minutos"),
        "porcentaje_competitivas": _calcular_procentaje_competitivas(sesiones)
    }

def _calculcar_total_sesiones(sesiones: list[dict]) -> int:
    return len(sesiones)

def _calcular_valor_avg(sesiones:list[dict], clave:str) -> float:
    total = _calculcar_total_sesiones(sesiones)
    suma = 0
    for registro in sesiones:
        suma += registro.get(clave)
    return round(suma / total, 2)

def _calcular_procentaje_competitivas(sesiones):
    total = _calculcar_total_sesiones(sesiones)
    competitivas = total - _calcular_partidas_casuales(sesiones)
    return (competitivas / total) * 100

def _calcular_partidas_casuales(sesiones:list[dict]) -> int:
    casuales = 0
    for registro in sesiones:
        if registro.get("tipo_partida") == "Casual":
            casuales +=1
    return casuales