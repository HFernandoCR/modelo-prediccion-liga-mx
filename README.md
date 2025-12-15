# Modelo de Predicción para Liga MX

Modelo de Regresión de Poisson para predecir resultados de partidos de fútbol basado en Dixon & Coles (1997).

**Autores:** 
- Hector Fernando Cruz Ruiz
- José Daniel Rodriguez Juárez
- Uriel Díaz Zarate
  
**Proyecto:** TecNM - Campus Oaxaca | Simulación
**Año:** 2025

---

## Características Principales

- **Modelo Estadístico:** Regresión de Poisson con estimación por Maximum Likelihood
- **Interfaz CLI:** Script principal para entrenar y predecir desde terminal
- **Interfaz Web:** Aplicación interactiva con Streamlit
- **Rankings:** Clasificación de equipos por ataque (α) y defensa (β)
- **Predicciones:** Matriz de probabilidades para todos los marcadores posibles
- **Visualizaciones:** Gráficos interactivos con Plotly y Matplotlib
- **Exportación:** Resultados en CSV para análisis posterior

---

## Tecnologías Utilizadas

```
Python 3.8+
├── pandas      - Manipulación de datos
├── numpy       - Operaciones numéricas
├── scipy       - Distribuciones estadísticas
├── statsmodels - Modelos GLM (Poisson)
├── matplotlib  - Visualizaciones estáticas
├── seaborn     - Gráficos estadísticos
├── streamlit   - Interfaz web interactiva
└── plotly      - Visualizaciones interactivas
```

---

## Instalación

### Requisitos Previos

Verifica que tengas Python 3.8 o superior instalado:

```bash
python --version
# o en algunos sistemas:
python3 --version
```

Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/)

---

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/HFernandoCR/modelo-prediccopm-liga-mx.git
cd modelo-prediccopm-liga-mx
```

### 2. Crear entorno virtual (IMPORTANTE)

Es **fundamental** usar un entorno virtual para:
- Evitar conflictos con otras versiones de librerías en tu sistema
- Mantener las dependencias del proyecto aisladas
- Garantizar que el proyecto funcione correctamente

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verificación:** Después de activar, deberías ver `(venv)` al inicio de tu línea de comandos:
```
(venv) C:\Users\...\modelo-prediccopm-liga-mx>
```

### 3. Instalar dependencias

Con el entorno virtual **activado**, instala las dependencias:

```bash
pip install -r requirements.txt
```

### 4. Verificar instalación

Verifica que todo se instaló correctamente:

```bash
pip list
```

Deberías ver paquetes como: `pandas`, `numpy`, `streamlit`, `statsmodels`, `plotly`, etc.

**Prueba rápida:**
```bash
python -c "import streamlit, pandas, statsmodels; print('✓ Instalación exitosa')"
```

### 5. Desactivar entorno virtual (cuando termines)

Cuando hayas terminado de trabajar con el proyecto:

```bash
deactivate
```

Esto te regresa a tu entorno Python normal. Para volver a trabajar en el proyecto, simplemente reactiva el entorno con el comando del paso 2.

---

## Estructura del Proyecto

```
modelo-prediccopm-liga-mx/
│
├── modelo_poisson/              # Módulo principal del modelo
│   ├── __init__.py             # Exporta ModeloPoissonFutbol
│   ├── preparacion_datos.py   # Carga y preprocesamiento de datos
│   └── utils.py                # Funciones auxiliares
│
├── view/                        # Visualizaciones (opcional)
│   └── __init__.py
│
├── main.py                      # Script CLI - Ejecución completa
├── app.py                       # Aplicación Web Streamlit
│
├── liga_mx_data_limpia.csv     # Datos históricos de partidos
├── parametros_modelo.csv       # Parámetros entrenados (α, β, γ)
├── plantilla_liga_mx.csv       # Plantilla CSV de ejemplo
│
├── ranking_ataque.csv          # Rankings generados (salida)
├── ranking_defensa.csv
├── predicciones_jornada.csv
│
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

---

## Uso

### Opción 1: Interfaz Web (Streamlit)

La forma más sencilla de usar el modelo es a través de la aplicación web interactiva:

```bash
streamlit run app.py
```

Esto abrirá una interfaz en tu navegador donde podrás:

#### Modo 1: Usar Modelo Pre-entrenado
- Seleccionar equipos de la Liga MX
- Ver predicciones instantáneas
- Explorar rankings de ataque y defensa
- Visualizar matrices de probabilidades interactivas

#### Modo 2: Entrenar Nuevo Modelo
- Descargar plantilla CSV de ejemplo
- Subir tu propio archivo CSV con datos históricos
- Entrenar modelo personalizado
- Hacer predicciones con el nuevo modelo

**Formato del CSV:**
```csv
Date,HomeTeam,AwayTeam,FTHG,FTAG
2023-07-15,Club America,Cruz Azul,2,1
2023-07-16,Tigres UANL,Monterrey,1,1
...
```

Donde:
- `Date`: Fecha del partido
- `HomeTeam`: Equipo local
- `AwayTeam`: Equipo visitante
- `FTHG`: Full Time Home Goals (goles del local)
- `FTAG`: Full Time Away Goals (goles del visitante)

---

### Opción 2: Script CLI (Terminal)

Para ejecutar el flujo completo desde la terminal:

```bash
python main.py
```

Este script ejecuta automáticamente:

1. **Carga de datos** desde `liga_mx_data_limpia.csv`
2. **Entrenamiento del modelo** con GLM Poisson
3. **Resumen del modelo** (log-likelihood, AIC, parámetros)
4. **Rankings** de ataque y defensa (Top 10)
5. **Predicciones de ejemplo** (Clásicos de la Liga MX)
6. **Análisis de equipos específicos**
7. **Comparación de equipos grandes**
8. **Simulación de jornada completa**
9. **Exportación de resultados** a CSV

**Archivos generados:**
- `ranking_ataque.csv` - Ranking completo de ataque
- `ranking_defensa.csv` - Ranking completo de defensa
- `parametros_modelo.csv` - Parámetros α, β, γ de todos los equipos
- `predicciones_jornada.csv` - Predicciones de jornada simulada

---

### Opción 3: Uso Programático

Puedes importar el modelo en tus propios scripts:

```python
from modelo_poisson import ModeloPoissonFutbol

# Crear y entrenar modelo
modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Hacer predicción
prediccion = modelo.predecir('Club America', 'Cruz Azul', mostrar=True)

# Acceder a resultados
print(f"Lambda Local: {prediccion['lambda_local']:.2f}")
print(f"Lambda Visitante: {prediccion['lambda_visitante']:.2f}")
print(f"Marcador más probable: {prediccion['marcador_mas_probable']}")
print(f"Probabilidad victoria local: {prediccion['prob_victoria_local']*100:.1f}%")

# Obtener rankings
ranking_ataque = modelo.obtener_ranking_ataque(top_n=10)
ranking_defensa = modelo.obtener_ranking_defensa(top_n=10)

# Análisis de equipo
params = modelo.obtener_parametros_equipo('Club America')
print(f"Alpha: {params['alpha']:.3f}")
print(f"Beta: {params['beta']:.3f}")

# Comparar equipos
equipos = ['Club America', 'Cruz Azul', 'Tigres UANL']
comparacion = modelo.comparar_equipos(equipos)

# Simular jornada
partidos = [
    ('Club America', 'Cruz Azul'),
    ('Monterrey', 'Tigres UANL'),
    ('Toluca', 'Santos Laguna')
]
resultados = modelo.simular_jornada(partidos, mostrar=True)

# Exportar parámetros
modelo.exportar_parametros('mi_modelo.csv')
```

---

## Metodología - Modelo de Poisson

### Fundamento Matemático

El modelo utiliza la **Distribución de Poisson** para modelar el número de goles en un partido:

```
P(X = k) = (λ^k × e^(-λ)) / k!
```

Donde `λ` (lambda) es la tasa esperada de goles.

### Cálculo de Goles Esperados

Para un partido entre equipo `i` (local) y equipo `j` (visitante):

```
λ_local = α_i × β_j × γ
λ_visitante = α_j × β_i
```

**Parámetros del modelo:**

- **α (alpha)**: Fuerza de ataque
  - α > 1: Ataque superior al promedio
  - α = 1: Ataque promedio
  - α < 1: Ataque inferior al promedio

- **β (beta)**: Fuerza de defensa
  - β < 1: Defensa fuerte (permite menos goles)
  - β = 1: Defensa promedio
  - β > 1: Defensa débil (permite más goles)

- **γ (gamma)**: Ventaja de local
  - Típicamente γ ≈ 1.2 - 1.4
  - Representa el incremento en goles esperados al jugar en casa

### Estimación de Parámetros

- **Método:** Maximum Likelihood Estimation (MLE)
- **Implementación:** Generalized Linear Model (GLM) con familia Poisson y enlace logarítmico
- **Librería:** `statsmodels.api.GLM`

### Proceso de Predicción

1. Calcular `λ_local` y `λ_visitante` usando los parámetros entrenados
2. Generar matriz de probabilidades para todos los marcadores posibles (ej. 0-0, 0-1, ..., 5-5)
3. Calcular probabilidades agregadas:
   - **P(Victoria Local)**: Suma de probabilidades donde goles_local > goles_visitante
   - **P(Empate)**: Suma de probabilidades donde goles_local = goles_visitante
   - **P(Victoria Visitante)**: Suma de probabilidades donde goles_local < goles_visitante
4. Identificar el marcador con mayor probabilidad

---

## Descripción de Módulos

### 1. `modelo_poisson/__init__.py`

Exporta la clase principal `ModeloPoissonFutbol` para facilitar imports:

```python
from modelo_poisson import ModeloPoissonFutbol
```

### 2. `modelo_poisson/preparacion_datos.py`

**Funciones principales:**

- `cargar_datos_historicos(ruta)`: Carga y valida CSV de partidos
- `preparar_datos_modelo(df, equipos)`: Crea variables dummy para GLM
- `construir_formula_glm(equipos)`: Genera fórmula Patsy
- `extraer_parametros_modelo(modelo, equipos)`: Extrae α, β, γ del modelo entrenado

### 3. `modelo_poisson/utils.py`

Utilidades generales:

- `sanitizar_nombre(nombre)`: Convierte nombres a variables válidas
- `validar_equipo(equipo, lista)`: Valida existencia de equipo
- `interpretar_parametro(valor, tipo)`: Interpreta α o β en texto
- `formatear_probabilidad(prob)`: Convierte a porcentaje
- `imprimir_titulo(titulo)`: Separadores visuales para CLI

### 4. `main.py`

Script principal que ejecuta el flujo completo:
- Carga datos desde `liga_mx_data_limpia.csv`
- Entrena modelo
- Genera rankings, predicciones y análisis
- Exporta resultados a CSV

### 5. `app.py`

Aplicación web interactiva con Streamlit:

**Características:**
- Sidebar con configuración de modo (pre-entrenado / entrenar nuevo)
- Selector de equipos con validación
- Visualizaciones interactivas con Plotly:
  - Heatmap de probabilidades (escala verde)
  - Gráfico de barras de resultados
  - Métricas de goles esperados (λ)
- Tabs organizados:
  - **Predicción**: Resultados y matrices
  - **Rankings**: Ataque y defensa
  - **Info del Modelo**: Parámetros y metodología
- Descarga de plantilla CSV
- Session state para modelo entrenado

**Funciones helper:**
- `cargar_modelo_preentrenado()`: Carga desde `parametros_modelo.csv`
- `entrenar_modelo_nuevo(uploaded_file)`: Entrena desde CSV subido
- `crear_heatmap_interactivo()`: Heatmap Plotly con tooltips
- `crear_grafico_barras()`: Probabilidades de resultado
- `crear_grafico_lambdas()`: Comparación de goles esperados

---

## Referencias Académicas

- **Dixon, M. J., & Coles, S. G. (1997).** "Modelling association football scores and inefficiencies in the football betting market". *Applied Statistics*, 46(2), 265-280.

- **Sánchez Gálvez et al. (2022).** "Model for Prediction of the Result of a Soccer Match Based on the Number of Goals Scored by a Single Team". *Computación y Sistemas*, 26(1), 295-302.

---

## Ejemplos de Salida

### Predicción de Partido

```
PREDICCIÓN: Club America vs Cruz Azul
==========================================================

Goles Esperados:
  • Club America (Local): λ = 1.85
  • Cruz Azul (Visitante): λ = 1.12

Marcador Más Probable: 2-1 (Probabilidad: 14.3%)

Probabilidades del Resultado:
  • Victoria Local:    58.7%
  • Empate:           23.1%
  • Victoria Visitante: 18.2%
```

### Rankings

**Ranking de Ataque (α):**
```
Ranking  Equipo              Alpha
1        Club America        1.245
2        Tigres UANL         1.198
3        Monterrey           1.156
```

**Ranking de Defensa (β):**
```
Ranking  Equipo              Beta
1        Toluca              0.812
2        Cruz Azul           0.867
3        Monterrey           0.891
```

---

## Video de Demostración

> **[Ver video completo en Google Drive](https://drive.google.com/file/d/1uUBmX_DafaqtpT0YhSbXM9D529yJRdZu/view?usp=drive_link)**
> 
> El video muestra el funcionamiento completo del sistema:
> - Predicciones con modelo pre-entrenado
> - Entrenamiento con datos personalizados
> - Visualizaciones interactivas
> - Interpretación de resultados

---

## Mejoras Futuras

- [ ] Integrar ventaja de visitante diferenciada por equipo
- [ ] Agregar factor temporal (decay para partidos antiguos)
- [ ] Implementar modelo Dixon-Coles completo con ajuste de empates 0-0, 1-0, 0-1, 1-1
- [ ] API REST con FastAPI para predicciones
- [ ] Dashboard con análisis histórico de precisión del modelo
- [ ] Integración con bases de datos (PostgreSQL/MongoDB)
- [ ] Tests unitarios con pytest

---

## Notas Importantes

- El modelo requiere al menos **30-50 partidos por equipo** para estimaciones confiables
- Los parámetros α, β, γ deben actualizarse periódicamente con nuevos datos
- La ventaja de local (γ) puede variar según la liga y temporada
- No incluye factores externos: lesiones, clima, motivación, etc.
- Es un modelo probabilístico: las predicciones no son determinísticas

---


## Licencia

Este proyecto es de uso académico para el TecNM.

---

**Desarrollado con Python 3.8+ | Streamlit | Statsmodels | Plotly**
