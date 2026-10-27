from os.path import exists
from time import sleep, strftime  # No se puede evitar.
# No se puede obtener la fecha desde os.
# Y si vamos a usar esto, ¿Por qué no también sleep?
from typing import TextIO

from carga import cargar_telemetria
from procesamiento import (
    analizar_por_servidor,
    calcular_estadisticas_globales,
    clasificar_incidentes,
)


def _menu_prompt() -> str:
    """Muestra el menú y solicita una opción al usuario."""
    MENU, PROMPT = _generar_menu()
    print(MENU)
    return input(PROMPT).strip()


def _generar_menu() -> tuple[str, str]:
    """Genera el menú de opciones y el texto de prompt."""
    divisor: str = "=" * 41
    title: str = "GAMESEC MONITOR - PANEL DE CONTROL"
    options: list[str] = [
        "1. Cargar y validar dataset",
        "2. Ver estadísticas globales de servidores",
        "3. Ver rendimiento por región de servidor",
        "4. Auditar incidentes de seguridad (Críticos y Sospechosos)",
        "5. Exportar reporte consolidado (reporte_gamesec.txt)",
        "6. Salir",
    ]
    input_text: str = "Seleccione una opción:"

    LINE_LEN: int = max(len(x) for x in options + [divisor, title, input_text])

    divisor = divisor.center(LINE_LEN)
    title = title.center(LINE_LEN)
    options = [option.center(LINE_LEN) for option in options]

    input_text = input_text.center(LINE_LEN).rstrip() + " "

    return "\n".join([divisor, title, divisor, *options, divisor]), input_text


DIVIDER = "=" * 70 + "\n"
SUBDIVIDER = "-" * 70 + "\n"


def exportar_reporte(
    sesiones: list[dict], ruta_salida: str = "reporte_gamesec.txt"
) -> None:
    """Exporta un reporte consolidado de telemetría a un archivo."""
    stats = calcular_estadisticas_globales(sesiones)
    servidores = analizar_por_servidor(sesiones)
    frecuencias, criticos = clasificar_incidentes(sesiones)

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        _escribir_encabezado(archivo)

        # [1] RESUMEN GLOBAL OPERATIVO
        _escribir_resumen_operativo(archivo, stats)

        # [2] RENDIMIENTO REGIONAL POR SERVIDOR
        _escribir_rendimiento_regional(archivo, servidores)

        # [3] AUDITORÍA DE SEGURIDAD E INCIDENTES
        _escribir_auditoria_seguridad(
            archivo, frecuencias, criticos, stats.get("total_sesiones")
        )

        # [4] CONCLUSIONES TÉCNICAS DEL EQUIPO
        _escribir_conclusiones(archivo)


def _escribir_encabezado(archivo: TextIO) -> None:
    """Escribe el encabezado del reporte."""
    archivo.write(DIVIDER)
    archivo.write("REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC\n")
    archivo.write(DIVIDER)
    archivo.write(f"Fecha de generación: {strftime('%d/%m/%Y')}\n\n")

def _escribir_resumen_operativo(archivo: TextIO, stats: dict) -> None:
    """Escribe el resumen global operativo del reporte."""
    archivo.write("[1] RESUMEN GLOBAL OPERATIVO\n")
    archivo.write(SUBDIVIDER)

    total_sesiones = stats.get("total_sesiones")
    ping_promedio = stats.get("ping_promedio")
    duracion_promedio = stats.get("duracion_promedio")
    porcentaje_competitivas = stats.get("porcentaje_competitivas")

    archivo.write(f"Total de sesiones procesadas: {total_sesiones}\n")
    archivo.write(f"Ping promedio global: {ping_promedio}ms\n")
    archivo.write(f"Duración media de partida: {duracion_promedio}min\n")
    archivo.write(
        f"Partidas de alta competencia (Ranked/Torneo): "
        f"{porcentaje_competitivas}%\n\n"
    )


def _escribir_rendimiento_regional(archivo: TextIO, servidores: dict) -> None:
    """Escribe el rendimiento regional por servidor."""
    archivo.write("[2] RENDIMIENTO REGIONAL POR SERVIDOR\n")
    archivo.write(SUBDIVIDER)
    archivo.write(
        "Servidor           | Sesiones | Ping Promedio | FPS Promedio\n"
    )
    archivo.write(SUBDIVIDER)
    for servidor, datos in servidores.items():
        cantidad = datos.get("cantidad")
        ping_srv = datos.get("ping_promedio")
        fps_srv = datos.get("fps_promedio")
        archivo.write(
            f"{servidor:<18} | {cantidad:<8} | "
            f"{ping_srv:>10.2f} ms | {fps_srv:>6.2f} fps\n"
        )
    archivo.write("\n")


def _escribir_auditoria_seguridad(
    archivo: TextIO, frecuencias: dict, criticos: list, total_sesiones: int
) -> None:
    """Escribe la auditoría de seguridad e incidentes."""
    archivo.write("[3] AUDITORÍA DE SEGURIDAD E INCIDENTES\n")
    archivo.write(SUBDIVIDER)
    archivo.write("Distribución de estados de seguridad:\n")

    normal = frecuencias.get("Normal")
    sospechoso = frecuencias.get("Sospechoso")
    critico = frecuencias.get("Crítico")

    porc_normal = round(normal * 100 / total_sesiones, 2)
    porc_sospechoso = round(sospechoso * 100 / total_sesiones, 2)
    porc_critico = round(critico * 100 / total_sesiones, 2)

    archivo.write(f"  • Normales:    {normal} sesiones ({porc_normal}%)\n")
    archivo.write(
        f"  • Sospechosos: {sospechoso} sesiones ({porc_sospechoso}%)\n"
    )
    archivo.write(f"  • Críticos:    {critico} sesiones ({porc_critico}%)\n\n")

    archivo.write("Detalle de Sesiones Críticas Detectadas:\n")
    for evento in criticos:
        id_sesion = evento.get("id_sesion")
        jugador_id = evento.get("jugador_id")
        servidor = evento.get("servidor")
        motivo = evento.get("motivo")
        archivo.write(
            f"  [!] Sesión #{id_sesion:<3} | "
            f"Jugador: {jugador_id} | Servidor: {servidor}\n"
        )
        archivo.write(f"      Motivo: {motivo}\n")
    archivo.write("\n")


def _escribir_conclusiones(archivo: TextIO) -> None:
    """Escribe las conclusiones técnicas del equipo."""
    archivo.write("[4] CONCLUSIONES TÉCNICAS DEL EQUIPO\n")
    archivo.write(SUBDIVIDER)
    archivo.write(
        "1. El análisis de latencia muestra que los servidores "
        "sudamericanos (SaoPaulo: 64.07ms, BuenosAires: 78.95ms) "
        "tienen el mejor rendimiento, lo que sugiere que la "
        "infraestructura está centrada en Sudamérica. Las "
        "comunicaciones hacia Europa y Norteamérica presentan "
        "latencias significativamente mayores (Frankfurt: 199.07ms, "
        "Virginia: 228.31ms), lo cual es consistente con la distancia "
        "física entre regiones.\n"
    )
    archivo.write(
        "2. El diseño modular del sistema separa la lógica de carga, "
        "procesamiento y presentación, facilitando el mantenimiento "
        "y la escalabilidad del código.\n"
    )
    archivo.write(
        "3. El programa procesa los registros de la base de manera eficaz, "
        "pero podría contar con try catch y excepciones, "
        "importar otros módulos como TypedDict y usar más archivos para "
        "partir main de UI.\n"
    )
    archivo.write(DIVIDER)
    archivo.write("FIN DEL REPORTE GAMESEC\n")
    archivo.write(DIVIDER)


def _has_sesiones(sesiones: list[dict]) -> bool:
    """Verifica si hay sesiones cargadas."""
    if sesiones:
        return True
    print("Error: Primero debe cargar el dataset (Opción 1).")
    return False


def main() -> None:
    sesiones: list[dict] = []

    while True:
        select = _menu_prompt()
        match select:
            case "1":
                # Cargar y validar dataset
                if not exists("gamesec_logs.csv"):
                    print("Error: El archivo 'gamesec_logs.csv' no existe.")
                else:
                    sesiones = cargar_telemetria("gamesec_logs.csv")
                    print(
                        f"Se cargaron {len(sesiones)} sesiones correctamente\n"
                        "Ahora se pueden procesar los datos."
                    )

            case "2":
                # Ver estadísticas globales de servidores
                if _has_sesiones(sesiones):
                    stats = calcular_estadisticas_globales(sesiones)
                    total_sesiones = stats.get("total_sesiones")
                    ping_promedio = stats.get("ping_promedio")
                    duracion_promedio = stats.get("duracion_promedio")
                    porcentaje_competitivas = stats.get(
                        "porcentaje_competitivas"
                    )
                    print(
                        f"Total de sesiones: {total_sesiones}, "
                        f"Ping promedio: {ping_promedio} ms, "
                        f"Duracion promedio de partidas: "
                        f"{duracion_promedio} min, "
                        f"Porcentaje de partidas competitivas: "
                        f"{porcentaje_competitivas:.2f}%"
                    )
                    input() # Pausa para leer

            case "3":
                # Ver rendimiento por región de servidor
                if _has_sesiones(sesiones):
                    servidores = analizar_por_servidor(sesiones)
                    for servidor, datos in servidores.items():
                        cantidad = datos.get("cantidad")
                        ping_promedio = datos.get("ping_promedio")
                        fps_promedio = datos.get("fps_promedio")
                        print(
                            f"Región: {servidor} | "
                            f"Cantidad: {cantidad} | "
                            f"Ping promedio: {ping_promedio} ms | "
                            f"FPS Promedio: {fps_promedio} fps"
                        )
                    input() # Pausa para leer

            case "4":
                # Auditar incidentes de seguridad (Críticos y Sospechosos)
                if _has_sesiones(sesiones):
                    frecuencias, criticos = clasificar_incidentes(sesiones)
                    normal = frecuencias.get("Normal")
                    sospechoso = frecuencias.get("Sospechoso")
                    critico = frecuencias.get("Crítico")
                    print(
                        f"Cantidad de sesiones normales: {normal}, "
                        f"Cantidad de sesiones sospechosas: {sospechoso}, "
                        f"Cantidad de sesiones críticas: {critico}"
                    )
                    for evento in criticos:
                        id_sesion = evento.get("id_sesion")
                        jugador_id = evento.get("jugador_id")
                        servidor = evento.get("servidor")
                        motivo = evento.get("motivo")
                        print(
                            f"En la sesión {id_sesion} el jugador {jugador_id} "
                            f"del servidor {servidor} fue puesto en la "
                            f"clasificación crítico por motivo: {motivo}"
                        )
                    input() # Pausa para leer

            case "5":
                # Exportar reporte consolidado (reporte_gamesec.txt)
                if _has_sesiones(sesiones):
                    exportar_reporte(sesiones)
                    print(
                        "Reporte exportado correctamente en "
                        "'reporte_gamesec.txt'."
                    )

            case "6":
                # Salir
                print("Bye bye!")
                sleep(1)
                break

            case _:
                print("Opción no válida")
        sleep(1)


if __name__ == "__main__":
    main()
