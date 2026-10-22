# Considerar importar los detalles de Sesiones para tipar los parámetros

def calcular_estadisticas_globales(
        sesiones: list[dict]) -> dict[str, int | float]:
    """Calcula estadísticas globales de las sesiones de juego.

    Args:
        sesiones: Lista de diccionarios con datos de sesiones de juego.

    Returns:
        Diccionario con estadísticas globales incluyendo:
            - total_sesiones: número total de sesiones
            - ping_promedio: promedio de ping
            - duracion_promedio: duración promedio en minutos
            - porcentaje_competitivas: porcentaje de partidas competitivas

    Raises:
        AssertionError: Si la lista de sesiones está vacía.
    """
    _total = _calcular_total_sesiones(sesiones) #Necesario para DRY
    assert _total > 0, (
        f"Recibida una lista inválida. "
        f"[Recibido {_total} registros, esperados al menos 1]"
    )   #Considerar raise ValueError

    return {
        "total_sesiones": _calculcar_total_sesiones(sesiones),
        "ping_promedio": _calcular_valor_avg(sesiones, "ping_promedio"),
        "duracion_promedio": _calcular_valor_avg(sesiones, "duracion_minutos"),
        "porcentaje_competitivas": _calcular_procentaje_competitivas(sesiones)
    }

def _calcular_total_sesiones(sesiones: list[dict]) -> int:
    """Calcula el total de sesiones en la lista."""
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