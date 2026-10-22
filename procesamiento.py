def analizar_por_servidor(sesiones: list[dict]) -> dict[str, dict[str, float | int]]:
    acumulador = {}
    
    for registro in sesiones:
        servidor = registro.get("servidor")
        ping = registro.get("ping_promedio")
        fps = registro.get("fps_promedio")

        if servidor not in acumulador:
            acumulador[servidor] = {
                "cantidad": 0,
                "suma_ping": 0,
                "suma_fps": 0
            }
        acumulador[servidor]["cantidad"] += 1
        acumulador[servidor]["suma_ping"] += ping
        acumulador[servidor]["suma_fps"] += fps    

    resultado = {}
    for servidor, datos in acumulador.items():
        cantidad = datos["cantidad"]
        resultado[servidor] = {
            "cantidad": cantidad,
            "ping_promedio": round(datos["suma_ping"] / cantidad, 2),
            "fps_promedio": round(datos["suma_fps"] / cantidad, 2)
        }

    return resultado
