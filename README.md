# Modelo Poisson - Liga MX

Instrucciones mínimas para ejecutar el proyecto localmente.

Requisitos
- Python 3.8+
- Paquetes: `pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`

Instalación (PowerShell):

```powershell
Set-Location -LiteralPath 'c:\Users\Fer\Simulación\Proyecto'
python -m pip install -r requirements.txt
```

Archivo de datos
- Coloca `liga_mx_data_limpia.csv` en la raíz del proyecto (junto a `main.py`).
- Columnas requeridas: `Temporada, Fecha, Equipo_Local, Equipo_Visitante, Goles_Local, Goles_Visitante`.

Ejecutar

```powershell
Set-Location -LiteralPath 'c:\Users\Fer\Simulación\Proyecto'
python main.py
```

Salida
- Archivos generados: `ranking_ataque.csv`, `ranking_defensa.csv`, `parametros_modelo.csv`, `predicciones_jornada.csv`.

Notas
- El código ya incluye mensajes claros en caso de ausencia del CSV.
- Si no necesitas visualizaciones, no es obligatorio instalar `matplotlib`/`seaborn`.
# Modelo de Predicción para Liga MX 🏆

Modelo de Regresión de Poisson para predecir resultados de partidos de fútbol.  
Basado en Dixon & Coles (1997).

**Proyecto:** TecNM - Simulación

---

## Arquitectura del proyecto

```
proyecto/
│
├── modelo_poisson/             
│   ├── __init__.py            
│   ├── modelo.py              
│   ├── preparacion_datos.py   
│   ├── predicciones.py         
│   └── utils.py               
│
├── visualizacion/               
│   ├── __init__.py
│   └── graficos.py            
│
├── main.py                      
├── liga_mx_data_limpia.csv     
├── requirements.txt             
└── README.md                
```

## Instalación

```bash
# Clonar repositorio (o copiar archivos)
cd proyecto

# Instalar dependencias
pip install -r requirements.txt
```

---

## Uso Básico

### Opción 1: Usar el script principal

```bash
python main.py
```

Esto ejecutará:
1. Carga de datos
2. Entrenamiento del modelo
3. Rankings de ataque/defensa
4. Predicciones de ejemplo
5. Exportación de resultados

### Opción 2: Uso programático

```python
from modelo_poisson import ModeloPoissonFutbol

# Crear modelo
modelo = ModeloPoissonFutbol()

# Cargar y entrenar
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Hacer predicción
prediccion = modelo.predecir('Club America', 'Cruz Azul')

# Obtener rankings
ranking_ataque = modelo.obtener_ranking_ataque(top_n=10)
ranking_defensa = modelo.obtener_ranking_defensa(top_n=10)

# Acceder a parámetros
print(f"Alpha América: {modelo.alpha['Club America']}")
print(f"Beta América: {modelo.beta['Club America']}")
print(f"Gamma (local): {modelo.gamma}")
```

---

## Descripción de Módulos

### 1. `modelo_poisson/modelo.py`

**Clase principal:** `ModeloPoissonFutbol`

**Responsabilidad:** Dirige todo el flujo del modelo

**Métodos principales:**
- `cargar_datos(ruta_csv)`: Carga datos históricos
- `entrenar()`: Entrena el modelo GLM
- `predecir(local, visitante)`: Predice un partido
- `obtener_ranking_ataque()`: Ranking por α
- `obtener_ranking_defensa()`: Ranking por β
- `resumen_modelo()`: Muestra resumen completo

**Ejemplo:**
```python
modelo = ModeloPoissonFutbol()
modelo.cargar_datos('datos.csv')
modelo.entrenar()
modelo.predecir('Equipo A', 'Equipo B')
```

---

### 2. `modelo_poisson/preparacion_datos.py`

**Responsabilidad:** Preprocesamiento de datos

**Funciones principales:**
- `cargar_datos_historicos(ruta)`: Carga y valida CSV
- `preparar_datos_modelo(df, equipos)`: Crea variables dummy
- `construir_formula_glm(equipos)`: Genera fórmula
- `extraer_parametros_modelo(modelo, equipos)`: Extrae α, β, γ

**Flujo de trabajo:**
```python
# 1. Cargar
df, equipos = cargar_datos_historicos('datos.csv')

# 2. Preparar
datos_entrenamiento = preparar_datos_modelo(df, equipos)

# 3. Fórmula
formula = construir_formula_glm(equipos)

# 4. Entrenar (en modelo.py)
modelo_glm = smf.glm(formula, datos_entrenamiento, ...)

# 5. Extraer
alpha, beta, gamma = extraer_parametros_modelo(modelo_glm, equipos)
```

---

### 3. `modelo_poisson/predicciones.py`

**Responsabilidad:** Cálculos de predicción

**Funciones principales:**
- `calcular_goles_esperados()`: Calcula λ
- `generar_matriz_probabilidades()`: Crea matriz P(i-j)
- `calcular_probabilidades_resultado()`: P(Victoria), P(Empate)
- `encontrar_marcador_mas_probable()`: Marcador con mayor P
- `predecir_partido_completo()`: Predicción integral
- `mostrar_prediccion_formato()`: Muestra resultados

**Ejemplo:**
```python
from modelo_poisson import predicciones as pred

# Calcular λ
lambda_local, lambda_visitante = pred.calcular_goles_esperados(
    'Equipo A', 'Equipo B', alpha, beta, gamma
)

# Generar matriz
matriz = pred.generar_matriz_probabilidades(lambda_local, lambda_visitante)

# Encontrar marcador más probable
marcador, prob, indices = pred.encontrar_marcador_mas_probable(matriz)
```

---

### 4. `modelo_poisson/utils.py`

**Responsabilidad:** Utilidades generales

**Funciones principales:**
- `sanitizar_nombre(nombre)`: Convierte a variable válida
- `validar_equipo(equipo, lista)`: Valida existencia
- `interpretar_parametro(valor, tipo)`: Interpreta α o β
- `formatear_probabilidad(prob)`: Convierte a %
- `imprimir_titulo(titulo)`: Separadores visuales

**Ejemplo:**
```python
from modelo_poisson.utils import sanitizar_nombre, interpretar_parametro

# Sanitizar
nombre = sanitizar_nombre("Club América")  # → "Club_América"

# Interpretar
texto = interpretar_parametro(1.35, 'alpha')
# → "Ataque 35.0% superior al promedio (Muy fuerte)"
```

---

### 5. `visualizacion/graficos.py`

**Responsabilidad:** Visualizaciones

**Funciones principales:**
- `crear_heatmap_probabilidades()`: Matriz de calor
- `graficar_rankings()`: Gráficos de barras
- `graficar_distribucion_goles()`: Distribución Poisson

**Ejemplo:**
```python
from visualizacion import crear_heatmap_probabilidades

# Crear heatmap
crear_heatmap_probabilidades(
    matriz, 
    'Club America', 
    'Cruz Azul',
    guardar=True,
    ruta='heatmap_america_vs_cruzazul.png'
)
```

---

## Metodología Implementada

### Modelo Matemático

**Distribución de Poisson:**
```
P(X = k) = (λ^k × e^(-λ)) / k!
```

**Goles Esperados:**
```
λ_local = α_local × β_visitante × γ
λ_visitante = α_visitante × β_local
```

**Donde:**
- α = Fuerza de ataque (α > 1 = ataque fuerte)
- β = Fuerza de defensa (β < 1 = defensa fuerte)
- γ = Ventaja de local (típicamente ~1.3)

### Estimación de Parámetros

- **Método:** Maximum Likelihood Estimation (MLE)
- **Implementación:** GLM con familia Poisson y enlace logarítmico
- **Librería:** statsmodels