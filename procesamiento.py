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
    """
    _total = _calcular_total_sesiones(sesiones) #Necesario para DRY
    assert _total > 0, (
        f"Recibida una lista inválida. "
        f"[Recibido {_total} registros, esperados al menos 1]"
    )   #Considerar raise ValueError

    return {
        "total_sesiones": _total,

        "ping_promedio": _calcular_valor_avg(
            sesiones,
            "ping_promedio",
            _total),

        "duracion_promedio": _calcular_valor_avg(
            sesiones,
            "duracion_minutos",
            _total),

        "porcentaje_competitivas": _calcular_porcentaje_competitivas(
            sesiones,
            _total)
    }

def _calcular_total_sesiones(sesiones: list[dict]) -> int:
    """Calcula el total de sesiones en la lista."""
    return len(sesiones)

def _calcular_valor_avg(
        sesiones: list[dict],
        clave: str,
        total: int) -> float:
    """Calcula el valor promedio de una clave específica en las sesiones. Redondea a 2 decimales."""
    suma = sum(
        registro.get(clave, 0)
        for registro in sesiones
    )

    return round(suma / total, 2)

def _calcular_porcentaje_competitivas(
        sesiones: list[dict],
        total: int) -> float:
    """Calcula el porcentaje de partidas competitivas
    (o no-Casuales)."""
    competitivas = total - _calcular_partidas_casuales(sesiones)
    return (competitivas / total) * 100
    # Regla de 3: (x / p) = Relación x contra población. 
    # Relación * 100 = repr a porcentaje.

def _calcular_partidas_casuales(sesiones: list[dict]) -> int:
    """Cuenta el número de partidas casuales en las sesiones."""
    return sum(
        1
        for registro in sesiones
        if registro.get("tipo_partida") == "Casual"
    )


def analizar_por_servidor(
    sesiones: list[dict[str, int | float]]
) -> dict[str, dict[str, int | float]]:
    """Analiza sesiones de juego por servidor.

    Procesa una lista de registros de sesiones, agrupándolos por el servidor
    donde se jugaron. Para cada servidor calcula el promedio de ping y FPS,
    además de mantener el conteo de sesiones.

    Args:
        sesiones: Lista de diccionarios donde cada diccionario representa
        una sesión de juego.

    Returns:
        Diccionario donde las claves son nombres de servidores y los valores
        son diccionarios con:
        - "cantidad": Número de sesiones en ese servidor (int)
        - "ping_promedio": Promedio de ping de todas las sesiones (float)
        - "fps_promedio": Promedio de FPS de todas las sesiones (float)
    """
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
    """Calcula los promedios de ping y FPS por servidor."""
    resultado: dict[str, dict[str, float | int]] = {}
    for servidor, datos in acumulador.items():
        cantidad = datos["cantidad"]
        resultado[servidor] = {
            "cantidad": cantidad,
            "ping_promedio": _calcular_promedio(datos["suma_ping"], cantidad),
            "fps_promedio": _calcular_promedio(datos["suma_fps"], cantidad)
        }
    return resultado


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
