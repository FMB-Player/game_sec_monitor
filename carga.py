from csv import DictReader

Telemetria = dict[str, int | str | float]

# Tecnicamente se podria usar TypedDict,
# pero el ejercicio prohibe específicamente usar imports que faciliten.
_format: dict[str, type[int | str | float]] = {
    "id_sesion": int,
    "servidor": str,
    "jugador_id": str,
    "tipo_partida": str,
    "ping_promedio": int,
    "fps_promedio": int,
    "duracion_minutos": float,
    "intentos_fallidos": int,
    "reportes_trampa": int,
}


def cargar_telemetria(ruta_archivo: str) -> list[Telemetria]:
    """
    Carga los datos de telemetría desde un archivo CSV.

    Args:
        ruta_archivo (str): Ruta al archivo CSV con los datos de telemetría.

    Returns:
        list[Telemetria]: Lista de diccionarios con los datos de telemetría.
    """
    datos_telemetria: list[Telemetria] = []

    with open(ruta_archivo, encoding="utf-8", newline="") as _csv:
        lector = DictReader(_csv, delimiter=",")
        for registro in lector:
            _castear_valores(registro)
            datos_telemetria.append(registro)
        return datos_telemetria


def _castear_valores(registro: dict[str, str]) -> None:
    """
    Convierte los valores de cada registro a su tipo correspondiente
    usando el diccionario de formateo para DRY.

    Args:
        registro (dict[str, str]): Diccionario con los datos de telemetría.
    """
    for key, _type in _format.items():
        registro[key] = _type(registro[key])
