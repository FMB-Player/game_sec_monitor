def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    """Clifica incidentes de sesiones de juego según reglas predefinidas.

    Args:
        sesiones: Lista de diccionarios con datos de sesiones. Cada diccionario
        debe contener: id_sesion, jugador_id, servidor, ping_promedio,
        intentos_fallidos, reportes_trampa.

    Returns:
        Tupla con:
        - Diccionario contador con claves "Normal", "Sospechoso", "Crítico"
        - Lista de diccionarios con eventos críticos (id_sesion, jugador_id,
            servidor, motivo)
    """
    contador: dict[str, int] = {
        "Normal": 0,
        "Sospechoso": 0,
        "Crítico": 0
    }
    eventos_criticos: list[dict] = []

    for registro in sesiones:
        id_sesion: int = registro.get("id_sesion")
        jugador_id: str = registro.get("jugador_id")
        servidor: str = registro.get("servidor")
        ping: float = registro.get("ping_promedio")
        intentos: int = registro.get("intentos_fallidos")
        reportes: int = registro.get("reportes_trampa")

        categoria = _determinar_categoria(ping, intentos, reportes)
        contador[categoria] += 1

        if categoria == "Crítico":
            motivo = _get_motivo(reportes, intentos)
            eventos_criticos.append({
                "id_sesion": id_sesion,
                "jugador_id": jugador_id,
                "servidor": servidor,
                "motivo": motivo
            })

    return contador, eventos_criticos

def _determinar_categoria(ping: float, intentos: int, reportes: int) -> str:
    """Determina la categoría de un incidente
    según ping, intentos y reportes."""
    if reportes >= 3 or intentos >= 4:
        return "Crítico"
    elif (ping > 200 and intentos >= 2) or reportes == 2:
        return "Sospechoso"
    else:
        return "Normal"

def _get_motivo(reportes: int, intentos: int) -> str:
    """Genera el mensaje de motivo para un incidente crítico."""
    assert reportes >= 3 or intentos >= 4, \
        "Error: No se encontraron motivos para marcar como crítico " + \
        "(Esperados: reportes >= 3 o intentos >= 4, " + \
        f"Recibidos: {reportes = !r}, {intentos = !r})"

    msg: list[str] = []
    if reportes >= 3:
        msg.append(f"reportes por trampa ({reportes})")
    if intentos >= 4:
        msg.append(f"intentos fallidos ({intentos})")

    return "Exceso de " + " e ".join(msg)
