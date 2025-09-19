# 📊 Análisis de Ingresos - Región de Los Ríos

<div align="center">

![Chile](https://img.shields.io/badge/Chile-Los%20Ríos-red?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjRkZGRkZGIi8+Cjwvc3ZnPg==)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production-green?style=for-the-badge)

</div>

<div align="center">
  <h3>🎯 Pipeline ETL y Dashboard Interactivo para Análisis de Equidad Salarial</h3>
  <p><em>Análisis longitudinal de la evolución salarial y brechas de género en la Región de Los Ríos, Chile (2010-2022)</em></p>
</div>

---

## ✨ Características Principales

<table>
<tr>
<td width="50%">

### 🔍 **Análisis Avanzado**
- **Pipeline ETL robusto** con arquitectura limpia
- **Análisis de brecha salarial** por género y tiempo
- **Detección estadística** de tendencias y valores atípicos
- **Validación automática** de calidad de datos

</td>
<td width="50%">

### 📱 **Visualización Moderna**
- **Dashboard responsivo** optimizado para móviles
- **4 visualizaciones interactivas** con Plotly
- **Estilo The Economist** profesional
- **Renderizado instantáneo** sin delays

</td>
</tr>
</table>

## � Inicio Rápido

### 📋 Prerrequisitos
- **Python 3.8+**
- **Git** para clonar el repositorio

### ⚡ Instalación en 3 pasos

```bash
# 1️⃣ Clonar el repositorio
git clone https://github.com/ObservaLosRios/IngresoPromedioLosRios.git
cd IngresoPromedioLosRios

# 2️⃣ Instalar dependencias
pip install -r requirements.txt

# 3️⃣ Ejecutar análisis
python src/main.py data/raw/IngresoPromedio.csv
```

### 🌐 Ver Dashboard
```bash
# Opción 1: Abrir directamente
open docs/index.html

# Opción 2: Servidor local
python -m http.server 8000 -d docs/
# Visita: http://localhost:8000
```

---

## 📊 Dashboard Interactivo

<div align="center">
  <img src="https://via.placeholder.com/800x400/f8f9fa/2c3e50?text=Dashboard+Preview" alt="Dashboard Preview" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
</div>

### 🎨 Visualizaciones Disponibles

| Sección | Descripción | Insights Clave |
|---------|-------------|----------------|
| **📈 Evolución** | Tendencias salariales temporales | Crecimiento promedio anual, volatilidad |
| **⚖️ Brecha Salarial** | Diferencias de género por año | Patrones de inequidad, cambios temporales |
| **👥 Comparación** | Análisis comparativo hombres vs mujeres | Convergencia/divergencia salarial |
| **🎯 Años Clave** | Períodos específicos (2010, 2015, 2022) | Hitos y cambios estructurales |

### ✨ Características Técnicas

<table>
<tr>
<td align="center">
<strong>📱 Responsivo</strong><br>
<small>Optimizado para móviles<br>y tablets</small>
</td>
<td align="center">
<strong>⚡ Instantáneo</strong><br>
<small>Sin delays de<br>renderizado</small>
</td>
<td align="center">
<strong>🎯 Interactivo</strong><br>
<small>Hover, zoom, pan<br>y descarga</small>
</td>
<td align="center">
<strong>🎨 Elegante</strong><br>
<small>Estilo The Economist<br>profesional</small>
</td>
</tr>
</table>

---

## 🏗️ Arquitectura del Sistema

### 📐 Principios de Diseño

<table>
<tr>
<td width="33%">

#### 🎯 **Clean Architecture**
- Separación clara de responsabilidades
- Independencia de frameworks
- Testabilidad completa

</td>
<td width="33%">

#### 🔧 **Principios SOLID**
- Single Responsibility
- Open/Closed
- Dependency Inversion

</td>
<td width="33%">

#### 📊 **ETL Robusto**
- Validación de datos
- Manejo de errores
- Logging estructurado

</td>
</tr>
</table>

### 🗂️ Estructura de Capas

```
🏛️ src/
├── 🧠 domain/              # Lógica de negocio core
│   ├── entities.py         # Modelos de datos
│   ├── repositories.py     # Contratos de persistencia
│   └── services.py         # Reglas de negocio
├── 🔧 infrastructure/      # Implementaciones técnicas
│   ├── data_loaders.py     # Carga de datos
│   ├── repositories.py     # Persistencia concreta
│   └── visualization.py    # Generación de gráficos
├── 📋 application/         # Casos de uso
│   └── use_cases.py        # Orquestación del flujo
└── 🎭 presentation/        # Interfaz externa
    ├── di_container.py     # Inyección de dependencias
    └── main.py             # Punto de entrada CLI
```

---

## ⚙️ Uso Avanzado

### 📊 Pipeline ETL

```bash
# Análisis básico
python src/main.py data/raw/IngresoPromedio.csv

# Múltiples formatos de salida
python src/main.py data/raw/IngresoPromedio.csv --output csv excel charts

# Modo verbose para debugging
python src/main.py data/raw/IngresoPromedio.csv --verbose

# Ver ayuda completa
python src/main.py --help
```

### 🎯 Outputs Generados

<details>
<summary><strong>📁 Archivos de Datos</strong></summary>

| Archivo | Descripción | Formato |
|---------|-------------|---------|
| `income_data_processed.csv` | Datos limpios y validados | CSV |
| `income_data_processed.xlsx` | Datos con formato profesional | Excel |
| `analysis_results.json` | Métricas y estadísticas completas | JSON |

</details>

<details>
<summary><strong>📈 Gráficos Estáticos (Opcionales)</strong></summary>

| Archivo | Descripción | Resolución |
|---------|-------------|------------|
| `income_trend_chart.png` | Evolución temporal | 300 DPI |
| `gender_gap_chart.png` | Análisis de brecha salarial | 300 DPI |
| `income_comparison_chart.png` | Comparaciones demográficas | 300 DPI |

</details>

---

## 🔬 Capacidades de Análisis

### 📊 Análisis Estadístico Avanzado

<table>
<tr>
<td width="33%">

#### ⚖️ **Brecha de Género**
- Cálculo porcentual año por año
- Identificación de tendencias
- Análisis de convergencia
- Proyecciones estadísticas

</td>
<td width="33%">

#### 📈 **Tendencias Temporales**
- Tasas de crecimiento anuales
- Análisis de volatilidad
- Detección de valores atípicos
- Patrones estacionales

</td>
<td width="33%">

#### 🔍 **Calidad de Datos**
- Validación automática
- Detección de inconsistencias
- Limpieza inteligente
- Reportes de calidad

</td>
</tr>
</table>

### 🎯 Insights Automáticos

El sistema genera automáticamente:

- 📊 **Resumen ejecutivo** con métricas clave
- 📈 **Tendencias de crecimiento** por demografía  
- ⚖️ **Evolución de brechas** salariales
- 🚨 **Alertas de anomalías** en los datos
- 📋 **Recomendaciones** basadas en patrones

---

## 🧪 Testing y Calidad

### 🔬 Suite de Pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Cobertura de código
pytest tests/ --cov=src --cov-report=html

# Pruebas específicas
pytest tests/test_entities.py -v
```

### 📊 Cobertura de Testing

| Componente | Tipo de Prueba | Cobertura |
|------------|----------------|-----------|
| **Entidades** | Unitarias | Modelos de datos y validaciones |
| **Servicios** | Unitarias | Lógica de negocio |
| **Pipeline** | Integración | Flujo ETL completo |
| **Datos** | Validación | Calidad y consistencia |

---

## �️ Configuración Avanzada

### 🌍 Variables de Entorno

```bash
# .env (ejemplo)
DATABASE_PATH=data/processed/ingreso_promedio.db
OUTPUT_PATH=data/processed/
LOG_LEVEL=INFO
FIGURE_WIDTH=12
FIGURE_HEIGHT=8
DPI=300
```

### ⚙️ Configuración YAML

```yaml
# config/config.yaml
visualization:
  style:
    name: "economist"
    colors:
      primary: "#003B5C"
      secondary: "#E3120B"
      accent: "#FFD700"
  fonts:
    title: 
      family: "Georgia, serif"
      size: 22
    axis:
      family: "Arial, sans-serif"
      size: 12
```

---

## 📁 Estructura del Proyecto

```
IngresoPromedioLosRios/
│
├── 📊 compile_visualizations.py    # Script principal de visualizaciones
├── 🚀 demo.sh                      # Demo de inicio rápido  
├── ⚙️ pyproject.toml               # Configuración moderna de Python
├── 📋 requirements.txt             # Dependencias del proyecto
├── 📖 README.md                    # Esta documentación
├── 📈 RESULTADOS.md                # Análisis y conclusiones
├── 🔄 run_pipeline.sh              # Pipeline automatizado
│
├── ⚙️ config/
│   └── config.yaml                 # Configuración centralizada
│
├── 💾 data/
│   └── raw/
│       └── IngresoPromedio.csv     # Dataset fuente (INE Chile)
│
├── 🌐 docs/                        # Dashboard web estático
│   ├── index.html                  # Aplicación principal
│   ├── styles.css                  # Estilos responsivos
│   ├── interactive.js              # Lógica de navegación
│   └── *.png                       # Assets gráficos
│
├── 📓 notebooks/
│   └── IngresoPromedioLosRios.ipynb # Análisis exploratorio
│
├── 🏗️ src/                         # Código fuente (Clean Architecture)
│   ├── 🧠 domain/                  # Lógica de negocio
│   ├── 🔧 infrastructure/          # Integraciones y datos
│   ├── 📋 application/             # Casos de uso
│   └── 🎭 presentation/            # Interfaces externas
│
└── 🧪 tests/                       # Suite de pruebas automatizadas
```

---

## 🎯 Casos de Uso

<table>
<tr>
<th width="33%">🏢 Sector Empresarial</th>
<th width="33%">🎓 Investigación Académica</th>
<th width="33%">🏛️ Políticas Públicas</th>
</tr>
<tr>
<td valign="top">

**Aplicaciones:**
- Auditorías de equidad salarial
- Benchmarking sectorial  
- Planificación de RRHH
- Reportes ejecutivos
- Análisis de competitividad

**Beneficios:**
- Decisiones basadas en datos
- Identificación de gaps
- Cumplimiento normativo

</td>
<td valign="top">

**Aplicaciones:**
- Estudios de mercado laboral
- Investigación de género
- Análisis socioeconómico
- Tesis y papers académicos
- Modelamiento econométrico

**Beneficios:**
- Datos validados y limpios
- Metodología reproducible
- Visualizaciones publicables

</td>
<td valign="top">

**Aplicaciones:**
- Evaluación de políticas
- Monitoreo de indicadores
- Planificación estratégica
- Informes gubernamentales
- Diseño de intervenciones

**Beneficios:**
- Evidencia robusta
- Transparencia de métodos
- Comunicación efectiva

</td>
</tr>
</table>

---

## 🚀 Roadmap y Desarrollo

### 🎯 Versión Actual (v1.0)
- ✅ Pipeline ETL completo
- ✅ Dashboard responsivo
- ✅ 4 visualizaciones core
- ✅ Arquitectura limpia
- ✅ Testing automatizado

### � Próximas Versiones

<details>
<summary><strong>v1.1 - Extensibilidad</strong></summary>

- 🔄 **API REST** para datos en tiempo real
- 📊 **Más visualizaciones** (boxplots, heatmaps)
- 🤖 **Machine Learning** para predicciones
- 📱 **PWA** para uso offline

</details>

<details>
<summary><strong>v1.2 - Integraciones</strong></summary>

- 🔗 **Conectores** a bases de datos externas
- 📧 **Reportes automáticos** por email
- 🌐 **Multi-región** support
- 📈 **Alertas inteligentes**

</details>

---

## 🤝 Contribuir al Proyecto

### 🛠️ Para Desarrolladores

```bash
# Fork y clone
git clone https://github.com/tu-usuario/IngresoPromedioLosRios.git
cd IngresoPromedioLosRios

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Instalar en modo desarrollo
pip install -e .
pip install -r requirements-dev.txt

# Ejecutar tests
pytest
```

### 📝 Guías de Contribución

<table>
<tr>
<td width="50%">

**🐛 Reportar Issues**
- Usar templates de GitHub
- Incluir pasos para reproducir
- Adjuntar logs relevantes
- Especificar versión/entorno

</td>
<td width="50%">

**✨ Pull Requests**
- Fork → Branch → PR
- Tests passing obligatorio
- Documentación actualizada
- Code review requerido

</td>
</tr>
</table>

### 🏆 Reconocimientos

Contribuidores destacados al proyecto:

<!-- CONTRIBUTORS-START -->
- 👨‍💻 **ObservaLosRios** - Creador y mantenedor principal
- 🧪 **Comunidad** - Testing y feedback
<!-- CONTRIBUTORS-END -->

---

## 📄 Licencia y Créditos

### 📜 Licencia
Este proyecto está bajo la **Licencia MIT** - ver [LICENSE](LICENSE) para detalles.

### 🏛️ Instituciones
- **Universidad Austral de Chile** - Centro de Estudios Regionales
- **ObservaLosRios** - Observatorio Regional

### 📊 Fuente de Datos
- **INE Chile** - Instituto Nacional de Estadísticas
- **Región de Los Ríos** - Datos oficiales de ingresos

### 🛠️ Stack Tecnológico

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

</div>

---

<div align="center">
  <h3>⭐ Si este proyecto te es útil, ¡considera darle una estrella! ⭐</h3>
  <p><em>Hecho con ❤️ para promover la transparencia y equidad salarial en Chile</em></p>
</div>
