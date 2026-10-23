from time import sleep

def _menu_prompt() -> int:
    MENU, PROMPT = _generar_menu()
    print(MENU)

    try:
        output = int(input(PROMPT).strip())
    except ValueError:
        output = 0
    return output

def _generar_menu() -> tuple[str, str]:
    divisor: str = ("=" * 41)
    title: str = "GAMESEC MONITOR - PANEL DE CONTROL"
    options: list[str] = [
        "1. Cargar y validar dataset",
        "2. Ver estadísticas globales de servidores",
        "3. Ver rendimiento por región de servidor",
        "4. Auditar incidentes de seguridad (Críticos y Sospechosos)",
        "5. Exportar reporte consolidado (reporte_gamesec.txt)",
        "6. Salir"
    ]
    input_text: str = "Seleccione una opción:"

    LINE_LEN: int = max(len(x) for x in (options, divisor, title, input_text))

    divisor = divisor.center(LINE_LEN)
    title = title.center(LINE_LEN)
    options = [option.center(LINE_LEN) for option in options]

    input_text = input_text.center(LINE_LEN).rstrip() + " "

    return "\n".join([divisor, title, divisor, *options, divisor]), input_text

if __name__ == "__main__":
    while True:
        select = _menu_prompt()
        match select:
            case 1:
                # cargar y validar dataset
                pass
            case 2:
                # ver estadísticas globales de servidores
                pass
            case 3:
                # ver rendimiento por región de servidor
                pass
            case 4:
                # auditar incidentes de seguridad (Críticos y Sospechosos)
                pass
            case 5:
                # exportar reporte consolidado (reporte_gamesec.txt)
                pass
            case 6:
                # salir
                print("Bye bye!")
                sleep(1)
                break
            case _:
                print("Opción no válida")
        sleep(1)