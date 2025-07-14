# Pipeline ETL - Análisis de Ingresos Región de Los Ríos

Pipeline ETL (Extract, Transform, Load) para el análisis de datos de ingresos de la Región de Los Ríos, Chile. Construido con principios de Arquitectura Limpia, patrones de diseño SOLID y visualizaciones profesionales interactivas.

## 🏗️ Arquitectura

Este proyecto sigue los principios de **Arquitectura Limpia** con clara separación de responsabilidades:

```
src/
├── domain/           # Lógica de negocio y entidades
│   ├── entities.py   # Entidades del dominio (IncomeRecord, Gender, etc.)
│   ├── repositories.py # Interfaces de repositorios
│   └── services.py   # Servicios de lógica de negocio
├── infrastructure/   # Aspectos externos
│   ├── data_loaders.py    # Implementaciones de carga de datos
│   ├── repositories.py    # Implementaciones de repositorios
│   └── visualization.py   # Generación de gráficos
├── application/      # Casos de uso y orquestación
│   └── use_cases.py  # Casos de uso ETL
└── presentation/     # Puntos de entrada e inyección de dependencias
    ├── di_container.py # Inyección de dependencias
    └── main.py        # Punto de entrada CLI
```

## 🎯 Implementación de Principios SOLID

- **Responsabilidad Única**: Cada clase tiene una sola razón para cambiar
- **Abierto/Cerrado**: Extensible sin modificación (nuevos cargadores de datos, visualizaciones)
- **Sustitución de Liskov**: Las interfaces de repositorios son intercambiables
- **Segregación de Interfaces**: Interfaces pequeñas y enfocadas
- **Inversión de Dependencias**: Depende de abstracciones, no de implementaciones concretas

## 📊 Características

### Procesamiento de Datos
- **Análisis robusto de CSV** con validación
- **Verificaciones de calidad** y limpieza de datos
- **Análisis de brecha salarial** por género
- **Análisis de tendencias** con métricas estadísticas
- **Almacenamiento SQLite** para datos procesados

### Visualizaciones Profesionales
- **Gráficos de tendencias** con líneas elegantes
- **Análisis de brecha de género** con gráficos de barras profesionales
- **Gráficos de comparación** de ingresos
- **Estilo personalizado** con tipografía y paleta de colores profesional

### Formatos de Salida
- **Exportaciones CSV** con datos formateados
- **Archivos Excel** con columnas auto-formateadas
- **Gráficos PNG de alta resolución** (300 DPI)
- **Resultados de análisis en JSON**

## 🚀 Inicio Rápido

### Instalación

1. **Clonar y navegar al proyecto:**
```bash
cd IngresoPromedioLosRios
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar el pipeline ETL:**
```bash
python src/main.py IngresoPromedio.csv
```

### Opciones de Línea de Comandos

```bash
# Ejecución básica
python src/main.py IngresoPromedio.csv

# Especificar formatos de salida
python src/main.py IngresoPromedio.csv --output csv excel charts

# Logging detallado
python src/main.py IngresoPromedio.csv --verbose

# Ayuda
python src/main.py --help
```

## 📈 Ejemplos de Salida

El pipeline genera varias salidas en el directorio `outputs/`:

### Gráficos Profesionales
- `income_trend_chart.png` - Evolución de ingresos a lo largo del tiempo
- `gender_gap_chart.png` - Análisis de brecha salarial por género
- `income_comparison_chart.png` - Comparación del último año

### Exportaciones de Datos
- `income_data_processed.csv` - Datos limpios y procesados
- `income_data_processed.xlsx` - Formato Excel con formateo
- `analysis_results.json` - Resultados completos del análisis

### Características de los Gráficos
- **Tipografía elegante** con fuentes serif para títulos
- **Paleta de colores profesional**
- **Formato limpio de grillas y ejes**
- **Formato adecuado de moneda** (notación K, M)
- **Atribución de fuente**

## 🧪 Pruebas

Ejecutar la suite de pruebas:

```bash
pytest tests/ -v
```

### Cobertura de Pruebas
- **Pruebas unitarias** para entidades y servicios del dominio
- **Pruebas de integración** para el pipeline ETL completo
- **Pruebas de validación de datos**
- **Pruebas de manejo de errores**

## 📊 Capacidades de Análisis de Datos

### Análisis de Brecha de Género
- Diferencias de ingresos por género año tras año
- Cálculos de porcentaje de brecha
- Identificación de tendencias

### Tendencias de Ingresos
- Cálculos de tasa de crecimiento
- Análisis de volatilidad
- Tendencias direccionales
- Detección estadística de valores atípicos

### Calidad de Datos
- Detección de valores faltantes
- Identificación de registros duplicados
- Validación de consistencia de datos
- Limpieza automatizada

## 🔧 Configuración

### Variables de Entorno (.env)
```bash
DATABASE_PATH=data/processed/ingreso_promedio.db
OUTPUT_PATH=outputs/
LOG_LEVEL=INFO
FIGURE_WIDTH=12
FIGURE_HEIGHT=8
DPI=300
```

### Configuración YAML (config/config.yaml)
```yaml
visualization:
  style:
    name: "professional"
    colors:
      primary: "#1f77b4"
      secondary: "#ff7f0e"
    fonts:
      title: 
        family: "Arial"
        size: 16
```

## 🏛️ Prácticas de Código Limpio

### Convenciones de Nomenclatura
- **Nombres descriptivos**: `IncomeAnalysisService`, `gender_gap_percentage`
- **Reveladores de intención**: `is_total_population()`, `calculate_gender_gap_by_year()`
- **Lenguaje del dominio**: Usa terminología de negocio consistentemente

### Diseño de Funciones
- **Funciones pequeñas** con responsabilidades únicas
- **Funciones puras** cuando es posible (sin efectos secundarios)
- **Parámetros descriptivos** con type hints
- **Manejo integral de errores**

### Organización del Código
- **Indentación y formato** consistentes
- **Agrupación lógica** de funcionalidad relacionada
- **Imports claros** y dependencias
- **Documentación integral**

## 📁 Estructura del Proyecto

```
IngresoPromedioLosRios/
├── IngresoPromedio.csv          # Datos originales
├── requirements.txt             # Dependencias de Python
├── .env                        # Configuración de entorno
├── README.md                   # Este archivo
├── config/
│   └── config.yaml            # Configuración de la aplicación
├── src/                       # Código fuente
│   ├── domain/               # Lógica de negocio
│   ├── infrastructure/       # Integraciones externas
│   ├── application/          # Casos de uso
│   └── presentation/         # Puntos de entrada
├── data/                     # Directorios de datos
│   ├── raw/                 # Datos originales
│   └── processed/           # Datos procesados
├── outputs/                  # Salidas generadas
├── tests/                   # Suite de pruebas
├── notebooks/               # Notebooks de análisis interactivo
└── logs/                    # Logs de la aplicación
```

## 🔍 Insights Clave del Análisis

El pipeline genera automáticamente insights como:

- **Tendencias de brecha salarial** a lo largo del tiempo
- **Tasas de crecimiento de ingresos** por demografía
- **Valores atípicos estadísticos** y problemas de calidad de datos
- **Análisis de volatilidad** de cambios en ingresos
- **Análisis comparativo** entre géneros

## 🎨 Diseño de Visualización

### Elementos de Estilo Profesional
- **Tipografía**: Fuentes serif para títulos, sans-serif para datos
- **Paleta de Colores**: Azules y rojos profesionales
- **Layout**: Márgenes limpios con contenido alineado a la izquierda
- **Estilo de Grilla**: Solo líneas de grilla horizontales sutiles
- **Atribución de Fuente**: Notas de fuente consistentes

### Tipos de Gráficos
1. **Gráficos de Líneas**: Para análisis de tendencias a lo largo del tiempo
2. **Gráficos de Barras**: Para comparaciones categóricas
3. **Gráficos de Barras Horizontales**: Para comparaciones directas de valores

## 🚦 Manejo de Errores

El pipeline incluye manejo integral de errores:

- **Validación de datos** con mensajes de error claros
- **Fallas elegantes** con capacidades de rollback
- **Logging detallado** para depuración
- **Reportes de error** amigables para el usuario

## 📝 Logging

Logging estructurado con múltiples niveles:
- **INFO**: Progreso general del pipeline
- **WARNING**: Problemas de calidad de datos
- **ERROR**: Fallas críticas
- **DEBUG**: Información detallada de ejecución

## 🔄 Extensibilidad

La arquitectura soporta extensión fácil:

- **Nuevas fuentes de datos**: Implementar interfaz `DataLoader`
- **Visualizaciones adicionales**: Extender `VisualizationService`
- **Almacenamiento diferente**: Implementar interfaz `Repository`
- **Nuevo análisis**: Agregar a servicios del dominio

## 📋 Requerimientos

- Python 3.8+
- pandas, numpy para procesamiento de datos
- matplotlib, seaborn para visualización
- sqlite3 para almacenamiento de datos
- loguru para logging
- pytest para testing
- plotly para visualizaciones interactivas

## � Análisis Interactivo

### Notebook Jupyter Incluido
- **Análisis completo** con visualizaciones interactivas
- **Exploración de datos** paso a paso
- **Gráficos dinámicos** con Plotly
- **Insights automáticos** y estadísticas clave
- **Estilo profesional** consistente

### Características del Notebook
- **Carga automática de datos** desde múltiples fuentes
- **Visualizaciones elegantes** con tipografía profesional
- **Análisis de brecha salarial** detallado
- **Comparaciones temporales** interactivas
- **Resumen ejecutivo** automático

## 👥 Contribuciones

Este proyecto sigue prácticas de desarrollo profesional:

1. **Revisión de código** para todos los cambios
2. **Requerimientos de cobertura** de pruebas
3. **Actualizaciones de documentación**
4. **Adherencia a principios SOLID**
5. **Estándares de código limpio**

## 📊 Rendimiento

- **Eficiencia de memoria**: Procesa datos en chunks
- **Ejecución rápida**: Operaciones optimizadas de pandas
- **Diseño escalable**: Puede manejar datasets más grandes
- **Gestión de recursos**: Limpieza adecuada y manejo de conexiones

## 🎯 Casos de Uso

### Análisis Empresarial
- **Auditorías de equidad salarial**
- **Planificación de recursos humanos**
- **Reportes ejecutivos** automatizados

### Investigación Académica
- **Estudios de género** en el mercado laboral
- **Análisis económico regional**
- **Investigación de tendencias** salariales

### Políticas Públicas
- **Evaluación de brechas salariales**
- **Monitoreo de indicadores** económicos
- **Desarrollo de políticas** basadas en evidencia
