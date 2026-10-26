def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    contador = {"Normal": 0, "Sospechoso": 0, "Crítico": 0}
    eventos_criticos = []

    for registro in sesiones:
        id_sesion = registro.get("id_sesion")
        jugador_id = registro.get("jugador_id")
        servidor = registro.get("servidor")
        ping = registro.get("ping_promedio", 0)
        intentos = registro.get("intentos_fallidos", 0)
        reportes = registro.get("reportes_trampa", 0)

        if reportes >= 3 or intentos >= 4:
            contador["Crítico"] += 1

            if reportes >= 3 and intentos >= 4:
                motivo = f"Exceso de reportes por trampa ({reportes}) e intentos fallidos ({intentos})"
            elif reportes >= 3:
                motivo = f"Exceso de reportes por trampa ({reportes})"
            else:
                motivo = f"Exceso de intentos fallidos ({intentos})"

            eventos_criticos.append({
                "id_sesion": id_sesion,
                "jugador_id": jugador_id,
                "servidor": servidor,
                "motivo": motivo
            })

        elif ping > 200 and intentos >= 2 or reportes == 2:
            contador["Sospechoso"] += 1

        else:
            contador["Normal"] += 1  
              
    return contador, eventos_criticos