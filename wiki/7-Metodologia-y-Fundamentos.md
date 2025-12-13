# 7. Metodología y Fundamentos Matemáticos

Esta página explica los fundamentos teóricos y matemáticos del modelo de predicción de Poisson.

---

##  Base Teórica

### Modelo Dixon & Coles (1997)

El modelo implementado está basado en el trabajo académico:

> **Dixon, M. J., & Coles, S. G. (1997).** "Modelling association football scores and inefficiencies in the football betting market". *Applied Statistics*, 46(2), 265-280.

**Idea principal:**
- Modelar los goles de cada equipo usando **distribuciones de Poisson independientes**
- Estimar parámetros de ataque (α) y defensa (β) para cada equipo
- Incluir factor de ventaja de local (γ)

---

##  Distribución de Poisson

### ¿Qué es la Distribución de Poisson?

La **Distribución de Poisson** modela eventos que ocurren de forma independiente a una tasa promedio.

**Fórmula:**

```
P(X = k) = (λ^k × e^(-λ)) / k!
```

Donde:
- **X**: Variable aleatoria (número de goles)
- **k**: Número específico de goles (0, 1, 2, 3, ...)
- **λ** (lambda): Tasa promedio esperada de goles
- **e**: Número de Euler (≈ 2.71828)
- **k!**: Factorial de k

_**[AÑADIR AQUÍ]:** Gráfico de la distribución de Poisson para diferentes valores de λ_

---

### Ejemplo Numérico

Si **λ = 1.5** (se esperan 1.5 goles en promedio):

```python
from scipy.stats import poisson

lambda_val = 1.5

for k in range(6):
    prob = poisson.pmf(k, lambda_val)
    print(f"P(X = {k}) = {prob:.4f} = {prob*100:.2f}%")
```

**Salida:**
```
P(X = 0) = 0.2231 = 22.31%   Probabilidad de 0 goles
P(X = 1) = 0.3347 = 33.47%   Probabilidad de 1 gol
P(X = 2) = 0.2510 = 25.10%   Probabilidad de 2 goles
P(X = 3) = 0.1255 = 12.55%
P(X = 4) = 0.0471 = 4.71%
P(X = 5) = 0.0141 = 1.41%
```

_**[AÑADIR AQUÍ]:** Gráfico de barras mostrando estas probabilidades_

**Interpretación:**
- Con λ = 1.5, lo **más probable** es marcar **1 gol** (33.47%)
- Pero también hay buena probabilidad de 0 goles (22.31%) o 2 goles (25.10%)

---

##  Aplicación al Fútbol

### ¿Por qué Poisson funciona para el fútbol?

1. **Eventos independientes:** Cada gol es relativamente independiente del anterior
2. **Tasa promedio:** Los equipos tienen un promedio de goles por partido
3. **Eventos raros:** Los goles son eventos relativamente poco frecuentes (λ suele ser < 3)

**Supuestos del modelo:**
- Los goles del equipo local son **independientes** de los goles del visitante
- La tasa de goles es **constante** durante el partido
- Los equipos no cambian su rendimiento significativamente entre partidos

---

##  Cálculo de λ (Lambda)

### Fórmula para Goles Esperados

Para un partido entre equipo **i** (local) y equipo **j** (visitante):

```
λ_local = α_i × β_j × γ
λ_visitante = α_j × β_i
```

Donde:
- **α_i**: Fuerza de ataque del equipo i
- **β_j**: Debilidad defensiva del equipo j
- **γ** (gamma): Ventaja de local (típicamente 1.2 - 1.4)

---

### Interpretación de los Parámetros

#### α (Alpha) - Fuerza de Ataque

Representa **cuántos goles marca** el equipo respecto al promedio.

- **α = 1.0**: Equipo marca goles al promedio de la liga
- **α = 1.2**: Equipo marca **20% más** goles que el promedio
- **α = 0.8**: Equipo marca **20% menos** goles que el promedio

**Ejemplo:**
- Si el promedio de la liga es 1.5 goles por partido:
  - α = 1.2  marca ~1.8 goles en promedio
  - α = 0.8  marca ~1.2 goles en promedio

---

#### β (Beta) - Debilidad Defensiva

Representa **cuántos goles permite** el equipo respecto al promedio.

 **IMPORTANTE:** β mide **debilidad**, no fortaleza.

- **β = 1.0**: Equipo permite goles al promedio de la liga
- **β = 1.2**: Equipo permite **20% más** goles (mala defensa)
- **β = 0.8**: Equipo permite **20% menos** goles (buena defensa)

**Ejemplo:**
- Si el promedio de la liga es permitir 1.3 goles:
  - β = 1.2  permite ~1.56 goles en promedio (débil)
  - β = 0.8  permite ~1.04 goles en promedio (fuerte)

---

#### γ (Gamma) - Ventaja de Local

Representa el **incremento multiplicador** de goles esperados al jugar en casa.

- **γ = 1.0**: No hay ventaja de local
- **γ = 1.3**: Los locales marcan **30% más** goles de lo esperado
- **γ = 1.5**: Ventaja muy grande (raro en fútbol profesional)

**Valores típicos por liga:**
- Liga MX: γ ≈ 1.25 - 1.35
- Premier League: γ ≈ 1.30
- Bundesliga: γ ≈ 1.28
- Ligas menores: γ ≈ 1.40+ (mayor ventaja de local)

---

### Ejemplo de Cálculo Completo

**Partido:** Club America (local) vs Cruz Azul (visitante)

**Parámetros:**
- Club America: α = 1.245, β = 0.923
- Cruz Azul: α = 1.089, β = 0.867
- γ = 1.32 (ventaja de local en Liga MX)

**Cálculo de λ:**

```
λ_America = α_America × β_CruzAzul × γ
          = 1.245 × 0.867 × 1.32
          = 1.425

λ_CruzAzul = α_CruzAzul × β_America
           = 1.089 × 0.923
           = 1.005
```

**Resultado:**
- **Club America** espera marcar **1.425 goles**
- **Cruz Azul** espera marcar **1.005 goles**

_**[AÑADIR AQUÍ]:** Diagrama visual del cálculo_

---

##  Estimación de Parámetros (MLE)

### Maximum Likelihood Estimation

Los parámetros α, β, γ se estiman mediante **Maximum Likelihood Estimation (MLE)**.

**Idea:** Encontrar los valores de α, β, γ que **maximizan la probabilidad** de haber observado los resultados históricos.

---

### Función de Verosimilitud (Likelihood)

Para un conjunto de partidos históricos, la verosimilitud es:

```
L(α, β, γ | datos) = ∏ P(goles_local_i | λ_local_i) × P(goles_visitante_i | λ_visitante_i)
```

Donde el producto (∏) es sobre todos los partidos i en los datos.

**En la práctica:**
Se maximiza el **log-likelihood** (logaritmo de la verosimilitud) por conveniencia numérica:

```
log L = ∑ [log P(goles_local_i | λ_local_i) + log P(goles_visitante_i | λ_visitante_i)]
```

---

### Implementación: GLM (Generalized Linear Model)

El modelo usa **GLM con familia Poisson** implementado en `statsmodels`:

```python
import statsmodels.api as sm

# Crear modelo GLM
modelo_local = sm.GLM(
    goles_local,
    X_design,
    family=sm.families.Poisson()
)

# Entrenar (encontrar α, β, γ óptimos)
resultado = modelo_local.fit()
```

**Enlace logarítmico:**
El GLM usa un **enlace logarítmico**, que significa:

```
log(λ) = β₀ + β₁×X₁ + β₂×X₂ + ...
```

Por lo tanto:
```
λ = exp(β₀ + β₁×X₁ + β₂×X₂ + ...)
```

_**[AÑADIR AQUÍ]:** Diagrama del flujo de entrenamiento GLM_

---

##  Predicción de Resultados

### Paso 1: Calcular λ para Ambos Equipos

Como se explicó anteriormente:
```
λ_local = α_local × β_visitante × γ
λ_visitante = α_visitante × β_local
```

---

### Paso 2: Generar Matriz de Probabilidades

Para cada combinación de goles (i, j):

```
P(Local = i, Visitante = j) = P(Local = i) × P(Visitante = j)
                              = Poisson(i; λ_local) × Poisson(j; λ_visitante)
```

**Ejemplo:**
```python
from scipy.stats import poisson

lambda_local = 1.85
lambda_visitante = 1.12

# Probabilidad de marcador 2-1
prob_2_1 = poisson.pmf(2, lambda_local) * poisson.pmf(1, lambda_visitante)
print(f"P(2-1) = {prob_2_1:.4f} = {prob_2_1*100:.2f}%")
```

_**[AÑADIR AQUÍ]:** Visualización de la matriz de probabilidades con código_

---

### Paso 3: Calcular Probabilidades Agregadas

#### Probabilidad de Victoria Local

```
P(Victoria Local) = ∑∑ P(i, j)  para todo i > j
```

Es decir, sumar todas las celdas donde goles_local > goles_visitante.

#### Probabilidad de Empate

```
P(Empate) = ∑ P(i, i)  para todo i
```

Sumar la diagonal: P(0,0) + P(1,1) + P(2,2) + ...

#### Probabilidad de Victoria Visitante

```
P(Victoria Visitante) = ∑∑ P(i, j)  para todo i < j
```

Sumar todas las celdas donde goles_local < goles_visitante.

_**[AÑADIR AQUÍ]:** Heatmap con regiones coloreadas por resultado_

---

### Paso 4: Identificar Marcador Más Probable

Buscar la celda (i, j) con **mayor probabilidad** en la matriz.

```python
import numpy as np

# Generar matriz
matriz = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        matriz[i, j] = poisson.pmf(i, lambda_local) * poisson.pmf(j, lambda_visitante)

# Encontrar máximo
max_idx = np.unravel_index(matriz.argmax(), matriz.shape)
prob_max = matriz[max_idx]

print(f"Marcador más probable: {max_idx[0]}-{max_idx[1]}")
print(f"Probabilidad: {prob_max*100:.2f}%")
```

---

##  Métricas de Calidad del Modelo

### Log-Likelihood

Mide **qué tan bien** el modelo explica los datos observados.

```
Log-Likelihood = ∑ log P(datos | modelo)
```

- **Más alto (menos negativo)** = Mejor ajuste
- Ejemplo: -1234.56 es mejor que -1500.00

---

### AIC (Akaike Information Criterion)

Penaliza modelos complejos para evitar overfitting.

```
AIC = 2k - 2×log-likelihood
```

Donde **k** es el número de parámetros.

- **Más bajo** = Mejor modelo
- Útil para **comparar modelos diferentes**

---

### Pseudo R²

No es un R² verdadero, pero da idea de ajuste:

```
Pseudo R² = 1 - (Log-Likelihood del modelo / Log-Likelihood del modelo nulo)
```

- Valores típicos: 0.1 - 0.3 en modelos de fútbol
- **No es comparable** con R² de regresión lineal

---

##  Limitaciones del Modelo

### Supuestos que pueden no cumplirse

1. **Independencia de goles:**
   - En realidad, un gol puede cambiar la táctica del equipo
   - El modelo asume que cada gol es independiente

2. **Tasa constante:**
   - Los equipos pueden jugar diferente en diferentes momentos
   - Lesiones, forma reciente, motivación no se consideran

3. **Distribución de Poisson:**
   - Subestima empates 0-0 y 1-1 (tendencia real)
   - Dixon & Coles proponen ajuste para goles bajos

---

### Factores no modelados

El modelo **NO considera:**
-  Lesiones de jugadores clave
-  Clima y condiciones del campo
-  Motivación (necesidad de puntos)
-  Rachas recientes (buena/mala forma)
-  Árbitros
-  Enfrentamientos directos (Head-to-Head)
-  Estilo de juego (defensivo vs ofensivo)

---

##  Extensiones Posibles

### Mejoras al Modelo Básico

#### 1. Ajuste Dixon-Coles para Goles Bajos

Añadir factor de corrección para 0-0, 1-0, 0-1, 1-1:

```
P_ajustado(i, j) = τ(i, j) × P_Poisson(i, j)
```

Donde τ es un factor de ajuste estimado.

---

#### 2. Factor de Decaimiento Temporal

Dar **más peso** a partidos recientes:

```
peso_partido = exp(-ξ × días_desde_partido)
```

Donde ξ controla qué tan rápido decae el peso.

---

#### 3. Ventaja de Local Específica por Equipo

En lugar de γ global, estimar γ_i para cada equipo:

```
λ_local = α_i × β_j × γ_i
```

Algunos equipos tienen aficiones más fuertes.

---

#### 4. Regresión de Parámetros

Modelar α y β como función de variables:
- Valor de mercado de la plantilla
- Edad promedio
- Presupuesto del club

---

##  Validación del Modelo

### Backtesting

**Proceso:**
1. Entrenar modelo con datos de temporadas pasadas
2. Predecir resultados de partidos futuros
3. Comparar predicciones con resultados reales

**Métricas de evaluación:**
- **Accuracy de favorito:** % de veces que predijo el favorito correctamente
- **RPS (Ranked Probability Score):** Mide error en probabilidades ordenadas
- **Calibración:** Las probabilidades predichas se cumplen en la realidad

_**[AÑADIR AQUÍ]:** Gráfico de curva de calibración_

---

### Cross-Validation

Dividir datos en:
- **Training set:** Para entrenar parámetros
- **Test set:** Para validar predicciones

Repetir múltiples veces y promediar resultados.

---

##  Referencias Académicas

### Artículos Fundamentales

1. **Dixon, M. J., & Coles, S. G. (1997).**
   "Modelling association football scores and inefficiencies in the football betting market"
   *Applied Statistics*, 46(2), 265-280.
   - **Modelo base** de Poisson para fútbol

2. **Maher, M. J. (1982).**
   "Modelling association football scores"
   *Statistica Neerlandica*, 36(3), 109-118.
   - **Primer modelo** de Poisson para fútbol

3. **Karlis, D., & Ntzoufras, I. (2003).**
   "Analysis of sports data by using bivariate Poisson models"
   *Journal of the Royal Statistical Society*, 52(3), 381-393.
   - **Modelos bivariados** para capturar dependencia

4. **Sánchez Gálvez et al. (2022).**
   "Model for Prediction of the Result of a Soccer Match Based on the Number of Goals Scored by a Single Team"
   *Computación y Sistemas*, 26(1), 295-302.
   - Aplicación moderna del modelo

---

### Recursos Adicionales

- **Book:** "Handbook of Statistical Methods and Analyses in Sports" - Chapman & Hall
- **Blog:** [Opisthokonta](http://www.opisthokonta.net/) - Análisis de fútbol con modelos estadísticos
- **Blog:** [Soccermatics](https://soccermatics.readthedocs.io/) - Matemáticas del fútbol

---

##  Implementación en el Código

### Arquitectura del Proyecto

```
modelo_poisson/
├── preparacion_datos.py     # Carga y preprocesamiento
│   ├── cargar_datos_historicos()
│   ├── preparar_datos_modelo()
│   └── construir_formula_glm()
│
├── modelo.py                 # Clase principal
│   └── ModeloPoissonFutbol
│       ├── entrenar()        # MLE con GLM
│       ├── predecir()        # Cálculo de λ y probabilidades
│       └── obtener_ranking() # Ordenar por α o β
│
├── predicciones.py          # Cálculos de predicción
│   ├── calcular_lambda()
│   ├── generar_matriz_probabilidades()
│   └── calcular_probabilidades_resultado()
│
└── utils.py                 # Utilidades
    ├── sanitizar_nombre()
    └── interpretar_parametro()
```

_**[AÑADIR AQUÍ]:** Diagrama de flujo de la arquitectura_

---

##  Conclusión

El modelo de Poisson es:

 **Sencillo** de entender e implementar
 **Interpretable** (α, β, γ tienen significado claro)
 **Efectivo** para identificar favoritos
 **Robusto** con suficientes datos

 **Limitado** por supuestos simplificadores
 **No considera** contexto (lesiones, forma, etc.)
 **Requiere actualización** regular con nuevos datos

**Es una herramienta útil** pero debe usarse junto con:
- Análisis cualitativo (ver partidos, conocer equipos)
- Contexto (lesiones, motivación, etc.)
- Sentido común

---

[️ Anterior: FAQ](6-FAQ-y-Troubleshooting) | [ Home](Home)
