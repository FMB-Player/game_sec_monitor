from carga import cargar_telemetria
from procesamiento import (
    calcular_estadisticas_globales,
    analizar_por_servidor,
    clasificar_incidentes,
)


def _menu_prompt() -> int:
    MENU, PROMPT = _generar_menu()
    print(MENU)

    try:
        output = int(input(PROMPT).strip())
    except ValueError:
        output = 0
    return output


def _generar_menu() -> tuple[str, str]:
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

    LINE_LEN: int = max(len(x) for x in (options, divisor, title, input_text))

    divisor = divisor.center(LINE_LEN)
    title = title.center(LINE_LEN)
    options = [option.center(LINE_LEN) for option in options]

    input_text = input_text.center(LINE_LEN).rstrip() + " "

    return "\n".join([divisor, title, divisor, *options, divisor]), input_text


def exportar_reporte(sesiones: list[dict], ruta_salida: str = "reporte_gamesec.txt") -> None:
    stats = calcular_estadisticas_globales(sesiones)
    servidores = analizar_por_servidor(sesiones)
    frecuencias, criticos = clasificar_incidentes(sesiones)

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write("=" * 70 + "\n")
        archivo.write("              REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC\n")
        archivo.write("=" * 70 + "\n")
        archivo.write("Fecha de generación: 26/10/2026\n\n")

        # [1] RESUMEN GLOBAL OPERATIVO
        archivo.write("[1] RESUMEN GLOBAL OPERATIVO\n")
        archivo.write("-" * 70 + "\n")
        total_sesiones = stats.get("total_sesiones")
        ping_promedio = stats.get("ping_promedio")
        duracion_promedio = stats.get("duracion_promedio")
        porcentaje_competitivas = stats.get("porcentaje_competitivas")

        archivo.write(f"Total de sesiones procesadas: {total_sesiones}\n")
        archivo.write(f"Ping promedio global: {ping_promedio} ms\n")
        archivo.write(f"Duración media de partida: {duracion_promedio} min\n")
        archivo.write(
            f"Partidas de alta competencia (Ranked/Torneo): {porcentaje_competitivas}%\n\n"
        )

        # [2] RENDIMIENTO REGIONAL POR SERVIDOR
        archivo.write("[2] RENDIMIENTO REGIONAL POR SERVIDOR\n")
        archivo.write("-" * 70 + "\n")
        archivo.write("Servidor           | Sesiones | Ping Promedio | FPS Promedio\n")
        archivo.write("-" * 70 + "\n")
        for servidor, datos in servidores.items():
            cantidad = datos.get("cantidad")
            ping_srv = datos.get("ping_promedio")
            fps_srv = datos.get("fps_promedio")
            archivo.write(
                f"{servidor:<18} | {cantidad:<8} | "
                f"{ping_srv:.2f} ms      | {fps_srv:.2f} fps\n"
            )
        archivo.write("\n")

        # [3] AUDITORÍA DE SEGURIDAD E INCIDENTES
        archivo.write("[3] AUDITORÍA DE SEGURIDAD E INCIDENTES\n")
        archivo.write("-" * 70 + "\n")
        archivo.write("Distribución de estados de seguridad:\n")

        normal = frecuencias.get("Normal")
        sospechoso = frecuencias.get("Sospechoso")
        critico = frecuencias.get("Crítico")

        porc_normal = round(normal * 100 / total_sesiones, 2)
        porc_sospechoso = round(sospechoso * 100 / total_sesiones, 2)
        porc_critico = round(critico * 100 / total_sesiones, 2)

        archivo.write(f"  • Normales:    {normal} sesiones ({porc_normal}%)\n")
        archivo.write(f"  • Sospechosos:  {sospechoso} sesiones ({porc_sospechoso}%)\n")
        archivo.write(f"  • Críticos:     {critico} sesiones ({porc_critico}%)\n\n")

        archivo.write("Detalle de Sesiones Críticas Detectadas:\n")
        for evento in criticos:
            id_sesion = evento.get("id_sesion")
            jugador_id = evento.get("jugador_id")
            servidor = evento.get("servidor")
            motivo = evento.get("motivo")
            archivo.write(
                f"  [!] Sesión #{id_sesion:<3} | Jugador: {jugador_id} | Servidor: {servidor}\n"
            )
            archivo.write(f"      Motivo: {motivo}\n")
        archivo.write("\n")

        # [4] CONCLUSIONES TÉCNICAS DEL EQUIPO
        archivo.write("[4] CONCLUSIONES TÉCNICAS DEL EQUIPO\n")
        archivo.write("-" * 70 + "\n")
        archivo.write(
            "1. Los servidores de Sudamérica (SA-SaoPaulo y SA-BuenosAires) presentan "
            "la menor latencia promedio (64.07 ms y 78.95 ms), mientras que NA-Virginia "
            "y EU-Frankfurt superan los 199 ms.\n"
        )
        archivo.write(
            "2. El 53.33% de las sesiones registradas corresponden a modalidades de "
            "alta competencia (Competitiva y Torneo), lo que exige priorizar la "
            "estabilidad y el control antitrampas.\n"
        )
        archivo.write(
            "3. Se detectó un 6.67% de sesiones críticas (10 casos) que combinan "
            "múltiples reportes por trampa con 4 o más intentos fallidos de login, "
            "sugiriendo accesos comprometidos o uso deliberado de hacks.\n"
        )
        archivo.write("=" * 70 + "\n")
        archivo.write("                    FIN DEL REPORTE GAMESEC\n")
        archivo.write("=" * 70 + "\n")


def main() -> None:
    sesiones: list[dict] = []

    while True:
        select = _menu_prompt()
        match select:
            case 1:
                # Cargar y validar dataset
                sesiones = cargar_telemetria("gamesec_logs.csv")
                print(f"Se cargaron {len(sesiones)} sesiones correctamente")

            case 2:
                # Ver estadísticas globales de servidores
                if sesiones == []:
                    print("Error: Primero debe cargar el dataset (Opción 1).")
                else:
                    stats = calcular_estadisticas_globales(sesiones)
                    total_sesiones = stats.get("total_sesiones")
                    ping_promedio = stats.get("ping_promedio")
                    duracion_promedio = stats.get("duracion_promedio")
                    porcentaje_competitivas = stats.get("porcentaje_competitivas")
                    print(
                        f"Total de sesiones: {total_sesiones}, "
                        f"Ping promedio: {ping_promedio} ms, "
                        f"Duracion promedio de partidas: {duracion_promedio} min, "
                        f"Porcentaje de partidas competitivas: {porcentaje_competitivas}%"
                    )

            case 3:
                # Ver rendimiento por región de servidor
                if sesiones == []:
                    print("Error: Primero debe cargar el dataset (Opción 1).")
                else:
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

            case 4:
                # Auditar incidentes de seguridad (Críticos y Sospechosos)
                if sesiones == []:
                    print("Error: Primero debe cargar el dataset (Opción 1).")
                else:
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
                            f"del servidor {servidor} fue puesto en la clasificación "
                            f"crítico por motivo: {motivo}"
                        )

            case 5:
                # Exportar reporte consolidado (reporte_gamesec.txt)
                if sesiones == []:
                    print("Error: Primero debe cargar el dataset (Opción 1).")
                else:
                    exportar_reporte(sesiones)
                    print("Reporte exportado correctamente en 'reporte_gamesec.txt'.")

            case 6:
                # Salir
                print("Bye bye!")
                break

            case _:
                print("Opción no válida")


if __name__ == "__main__":
    main()
