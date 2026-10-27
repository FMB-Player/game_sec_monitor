# GAMESEC MONITOR

**Sistema de monitoreo y auditoría de telemetría para servidores de juegos.**

## Descripción

***GAMESEC MONITOR*** es una herramienta de línea de comandos desarrollada en Python que procesa datos de telemetría de sesiones de juego multi-regional. El sistema analiza métricas de rendimiento (ping, FPS), clasifica incidentes de seguridad según reglas predefinidas, y genera reportes detallados con conclusiones técnicas.

## Arquitectura

El proyecto sigue una arquitectura modular con tres componentes principales:

```
GAMESEC MONITOR
├── main.py
│   ├── Interfaz de Usuario
│   ├── Generación de Reportes
│   └── Menú Interactivo
├── carga.py
│   ├── Carga desde CSV
│   ├── Validación de Datos
│   └── Conversión de Tipos
└── procesamiento.py
    ├── Estadísticas Globales
    ├── Análisis por Servidor
    └── Clasificación de Incidentes
```

### Flujo de Datos

1. **Entrada**: El usuario inicia el programa y selecciona cargar datos desde `gamesec_logs.csv`
2. **Carga**: `carga.py` lee el CSV, valida y convierte los tipos de datos
3. **Procesamiento**: `procesamiento.py` analiza los datos (estadísticas, por servidor, clasificación)
4. **Presentación**: `main.py` muestra resultados por consola o genera reporte en `reporte_gamesec.txt`

### Componentes

- **`main.py`**: Módulo principal que implementa la interfaz de usuario por consola y la generación de reportes. Maneja el menú interactivo y coordina las operaciones de carga, procesamiento y exportación.

- **`carga.py`**: Módulo responsable de la carga y validación de datos desde archivos CSV. Realiza conversión de tipos automática de los campos de telemetría.

- **`procesamiento.py`**: Módulo de análisis de datos que contiene funciones para:
  - Cálculo de estadísticas globales (total de sesiones, ping promedio, duración, porcentaje de partidas competitivas)
  - Análisis de rendimiento por servidor/región
  - Clasificación de incidentes de seguridad (Normal, Sospechoso, Crítico)

## Requisitos

- Python 3.10+
- Archivo de datos `gamesec_logs.csv` con el formato especificado

## Instalación

No requiere instalación de dependencias externas. Solo asegúrese de tener Python 3.10 o superior instalado.

## Uso

Ejecute el programa desde la terminal:

```bash
python main.py
```

El sistema mostrará un menú interactivo con las siguientes opciones:

1. **Cargar y validar dataset**: Carga los datos de telemetría desde `gamesec_logs.csv`
2. **Ver estadísticas globales de servidores**: Muestra métricas agregadas de todas las sesiones
3. **Ver rendimiento por región de servidor**: Desglose de ping y FPS por cada servidor regional
4. **Auditar incidentes de seguridad**: Muestra distribución de estados de seguridad y detalle de sesiones críticas
5. **Exportar reporte consolidado**: Genera `reporte_gamesec.txt` con análisis completo
6. **Salir**: Termina la ejecución del programa

## Formato de Datos

El archivo CSV de entrada debe contener las siguientes columnas:

- `id_sesion`: Identificador único de la sesión (int)
- `servidor`: Nombre del servidor/región (str)
- `jugador_id`: Identificador del jugador (str)
- `tipo_partida`: Tipo de partida (str, ej: "Casual", "Competitivo", "Torneo")
- `ping_promedio`: Ping promedio de la sesión (int, ms)
- `fps_promedio`: FPS promedio de la sesión (int)
- `duracion_minutos`: Duración de la partida (float, minutos)
- `intentos_fallidos`: Cantidad de intentos fallidos de login (int)
- `reportes_trampa`: Cantidad de reportes por trampa (int)

## Reglas de Clasificación de Seguridad

El sistema clasifica cada sesión en una de tres categorías:

- **Normal**: Sesiones sin patrones sospechosos
- **Sospechoso**: Sesiones con alguna combinación de factores anómalos (ping > 200 + intentos ≥ 2, o reportes = 2)
- **Crítico**: Sesiones con evidencia clara de comprometimiento (reportes ≥ 3 o intentos ≥ 4)

## Reporte de Salida

El reporte generado (`reporte_gamesec.txt`) incluye:

1. **Resumen Global Operativo**: Estadísticas agregadas de todas las sesiones
2. **Rendimiento Regional por Servidor**: Tabla con métricas por servidor/región
3. **Auditoría de Seguridad e Incidentes**: Distribución de estados y detalle de incidentes críticos
4. **Conclusiones Técnicas del Equipo**: Análisis de datos y observaciones arquitectónicas

## Desarrollo

### Estructura del Código

- Funciones privadas prefijadas con `_` siguen la convención de Python
- Docstrings en todas las funciones públicas
- Type hints en parámetros y retornos

<!-- ### Equipo de desarrollo

- Balella, Franco Matías 

- Maidana, Federico

- Vera, Elias

No me sé sus nombre completos - FMB -->
