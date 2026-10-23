def analizar_por_servidor(
    sesiones: list[dict[str, int | float]]
) -> dict[str, dict[str, int | float]]:
    acumulador: dict[str, dict[str, int | float]] = {}

    for registro in sesiones:
        servidor = registro["servidor"]
        # Servidor no puede ser ignorado porque es clave, que falle en paso 1
        ping = registro.get("ping_promedio")
        fps = registro.get("fps_promedio")
        # NOTE: Permitimos valores None para levantar errores
        # en caso de datos faltantes

        if servidor not in acumulador:
            acumulador[servidor] = {
                "cantidad": 0,
                "suma_ping": 0,
                "suma_fps": 0
            }
        datos_server = acumulador[servidor]
        datos_server["cantidad"] += 1
        datos_server["suma_ping"] += ping
        datos_server["suma_fps"] += fps

    return _calcular_promedios_por_servidor(acumulador)

def _calcular_promedio(sumatoria: float, cantidad: int) -> float:
    """ Calcula el promedio de una sumatoria.
    No es particularmente útil, pero DRY """
    return round(sumatoria / cantidad, 2)

def _calcular_promedios_por_servidor(
    acumulador: dict[str, dict[str, int | float]]
) -> dict[str, dict[str, float | int]]:
    resultado: dict[str, dict[str, float | int]] = {}
    for servidor, datos in acumulador.items():
        cantidad = datos["cantidad"]
        resultado[servidor] = {
            "cantidad": cantidad,
            "ping_promedio": _calcular_promedio(datos["suma_ping"], cantidad),
            "fps_promedio": _calcular_promedio(datos["suma_fps"], cantidad)
        }
    return resultado
