# 3. Uso de la Interfaz CLI (Terminal)

La interfaz de línea de comandos (CLI) te permite ejecutar el modelo directamente desde la terminal, ideal para automatización o usuarios avanzados.

---

##  Ejecutar el Script Principal

### Ejecución Simple

**Paso 1:** Con el entorno virtual activado, ejecuta:

```bash
python main.py
```

_**[AÑADIR AQUÍ]:** Captura del comando ejecutándose en la terminal_

El script ejecutará automáticamente un **flujo completo** de análisis.

---

##  ¿Qué hace el script?

El script `main.py` ejecuta las siguientes operaciones en orden:

### 1️⃣ Carga de Datos

```
==========================================================
CARGANDO DATOS
==========================================================
 Datos cargados exitosamente: 612 partidos
```

_**[AÑADIR AQUÍ]:** Captura de la sección de carga de datos_

---

### 2️⃣ Entrenamiento del Modelo

```
==========================================================
ENTRENANDO MODELO
==========================================================
 Modelo entrenado exitosamente
```

_**[AÑADIR AQUÍ]:** Captura del entrenamiento del modelo_

---

### 3️⃣ Resumen del Modelo

```
==========================================================
RESUMEN DEL MODELO
==========================================================

Información del Modelo:
  • Número de equipos: 18
  • Observaciones: 612 partidos
  • Log-Likelihood: -1234.56
  • AIC: 2567.89

Parámetros Globales:
  • Ventaja de local (γ): 1.32
```

_**[AÑADIR AQUÍ]:** Captura completa del resumen del modelo_

**Interpretación:**
- **Log-Likelihood:** Medida de ajuste del modelo (más alto = mejor)
- **AIC (Akaike Information Criterion):** Criterio de selección de modelos (más bajo = mejor)
- **γ (gamma):** Factor multiplicador de ventaja de local (típicamente 1.2-1.4)

---

### 4️⃣ Rankings de Ataque y Defensa

#### Ranking de Ataque (Top 10)

```
==========================================================
RANKING DE ATAQUE (Top 10)
==========================================================

Ranking  Equipo              Alpha    Interpretación
------   -----------------   ------   ------------------
1        Club America        1.245    Superior
2        Tigres UANL         1.198    Superior
3        Monterrey           1.156    Superior
...
```

_**[AÑADIR AQUÍ]:** Captura del ranking de ataque_

#### Ranking de Defensa (Top 10)

```
==========================================================
RANKING DE DEFENSA (Top 10)
==========================================================

Ranking  Equipo              Beta     Interpretación
------   -----------------   ------   ------------------
1        Toluca              0.812    Fuerte
2        Cruz Azul           0.867    Fuerte
3        Monterrey           0.891    Buena
...
```

_**[AÑADIR AQUÍ]:** Captura del ranking de defensa_

---

### 5️⃣ Predicciones de Ejemplo

El script genera predicciones para clásicos de la Liga MX:

```
==========================================================
PREDICCIÓN: Club America vs Cruz Azul
==========================================================

Goles Esperados:
  • Club America (Local): λ = 1.85
  • Cruz Azul (Visitante): λ = 1.12

Marcador Más Probable: 2-1 (Probabilidad: 14.3%)

Probabilidades del Resultado:
  • Victoria Local:     58.7%
  • Empate:            23.1%
  • Victoria Visitante: 18.2%
```

_**[AÑADIR AQUÍ]:** Captura de una predicción completa_

**Ejemplos incluidos:**
- Club America vs Cruz Azul
- Tigres UANL vs Monterrey (Clásico Regio)
- Chivas Guadalajara vs Atlas (Clásico Tapatío)

---

### 6️⃣ Análisis de Equipos Específicos

```
==========================================================
ANÁLISIS: Club America
==========================================================

Parámetros:
  • Alpha (Ataque): 1.245 (Superior)
  • Beta (Defensa): 0.923 (Buena)

Fortalezas:
   Ataque 24.5% superior al promedio
   Defensa permite 7.7% menos goles que el promedio

Descripción:
  Club America es un equipo balanceado con ataque superior
  y defensa sólida, ideal para victoria en casa.
```

_**[AÑADIR AQUÍ]:** Captura del análisis de un equipo_

---

### 7️⃣ Comparación de Equipos

```
==========================================================
COMPARACIÓN DE EQUIPOS
==========================================================

Comparando: Club America, Cruz Azul, Tigres UANL

      Equipo         Alpha   Beta   Balance
---   ------------   -----   ----   --------
1     Club America   1.245   0.923  Ataque
2     Tigres UANL    1.198   0.945  Ataque
3     Cruz Azul      1.089   0.867  Balanceado
```

_**[AÑADIR AQUÍ]:** Captura de la comparación de equipos_

---

### 8️⃣ Simulación de Jornada

```
==========================================================
SIMULACIÓN DE JORNADA
==========================================================

Partido                          Marcador  Prob.   Resultado
------------------------------   --------  -----   ---------
Club America vs Cruz Azul        2-1       14.3%   Local
Monterrey vs Tigres UANL         1-1       13.8%   Empate
Toluca vs Santos Laguna          2-0       15.2%   Local
...
```

_**[AÑADIR AQUÍ]:** Captura de la simulación de jornada completa_

---

### 9️⃣ Exportación de Resultados

```
==========================================================
EXPORTANDO RESULTADOS
==========================================================

 Exportado: ranking_ataque.csv
 Exportado: ranking_defensa.csv
 Exportado: parametros_modelo.csv
 Exportado: predicciones_jornada.csv

Archivos guardados en el directorio actual
```

_**[AÑADIR AQUÍ]:** Captura de la exportación de archivos_

**Archivos generados:**
- `ranking_ataque.csv` - Ranking completo de todos los equipos por ataque
- `ranking_defensa.csv` - Ranking completo de todos los equipos por defensa
- `parametros_modelo.csv` - Parámetros α, β, γ de todos los equipos
- `predicciones_jornada.csv` - Predicciones de jornada simulada

---

##  Archivos CSV Generados

### Visualizar los archivos

Puedes abrir estos archivos con Excel, Google Sheets, o cualquier editor de texto.

_**[AÑADIR AQUÍ]:** Captura de ranking_ataque.csv abierto en Excel_

_**[AÑADIR AQUÍ]:** Captura de parametros_modelo.csv abierto en Excel_

---

##  Uso Programático Avanzado

### Importar el Modelo en tus Scripts

Puedes importar y usar el modelo en tus propios scripts Python:

```python
from modelo_poisson import ModeloPoissonFutbol

# Crear instancia
modelo = ModeloPoissonFutbol()

# Cargar datos
modelo.cargar_datos('liga_mx_data_limpia.csv')

# Entrenar
modelo.entrenar()

# Hacer predicción
prediccion = modelo.predecir('Club America', 'Cruz Azul', mostrar=True)

# Acceder a los resultados
print(f"Lambda Local: {prediccion['lambda_local']:.2f}")
print(f"Lambda Visitante: {prediccion['lambda_visitante']:.2f}")
print(f"Marcador: {prediccion['marcador_mas_probable']}")
print(f"Probabilidad: {prediccion['prob_victoria_local']*100:.1f}%")
```

_**[AÑADIR AQUÍ]:** Captura de un script personalizado ejecutándose_

---

### Métodos Disponibles

#### `modelo.cargar_datos(ruta_csv)`
Carga datos históricos desde un archivo CSV.

```python
modelo.cargar_datos('mis_datos.csv')
```

---

#### `modelo.entrenar()`
Entrena el modelo con los datos cargados.

```python
modelo.entrenar()
```

---

#### `modelo.predecir(local, visitante, mostrar=True)`
Predice el resultado de un partido.

```python
resultado = modelo.predecir('Tigres UANL', 'Monterrey', mostrar=False)
```

**Retorna un diccionario con:**
- `lambda_local`: Goles esperados del local
- `lambda_visitante`: Goles esperados del visitante
- `marcador_mas_probable`: Tupla (goles_local, goles_visitante)
- `prob_marcador_mas_probable`: Probabilidad del marcador
- `prob_victoria_local`: Probabilidad de victoria local
- `prob_empate`: Probabilidad de empate
- `prob_victoria_visitante`: Probabilidad de victoria visitante
- `matriz_probabilidades`: Matriz completa de probabilidades

---

#### `modelo.obtener_ranking_ataque(top_n=None)`
Obtiene el ranking de ataque.

```python
top_10_ataque = modelo.obtener_ranking_ataque(top_n=10)
print(top_10_ataque)
```

---

#### `modelo.obtener_ranking_defensa(top_n=None)`
Obtiene el ranking de defensa.

```python
top_10_defensa = modelo.obtener_ranking_defensa(top_n=10)
print(top_10_defensa)
```

---

#### `modelo.obtener_parametros_equipo(equipo)`
Obtiene los parámetros α, β de un equipo.

```python
params = modelo.obtener_parametros_equipo('Club America')
print(f"Alpha: {params['alpha']:.3f}")
print(f"Beta: {params['beta']:.3f}")
```

---

#### `modelo.comparar_equipos(lista_equipos)`
Compara múltiples equipos.

```python
equipos = ['Club America', 'Cruz Azul', 'Tigres UANL']
comparacion = modelo.comparar_equipos(equipos)
```

---

#### `modelo.simular_jornada(partidos, mostrar=True)`
Simula una jornada completa.

```python
partidos = [
    ('Club America', 'Cruz Azul'),
    ('Monterrey', 'Tigres UANL'),
    ('Toluca', 'Santos Laguna')
]
resultados = modelo.simular_jornada(partidos, mostrar=True)
```

---

#### `modelo.exportar_parametros(ruta_csv)`
Exporta parámetros a CSV.

```python
modelo.exportar_parametros('mi_modelo.csv')
```

---

##  Personalizar el Script Principal

Puedes editar [main.py](../main.py) para cambiar:

- Los equipos a analizar
- Los partidos a predecir
- Los archivos de salida
- El formato de visualización

**Ejemplo: Cambiar los partidos predichos**

Edita la sección en `main.py`:

```python
# Predicciones de ejemplo
print_title("PREDICCIONES DE EJEMPLO")

# Agrega tus propios partidos aquí
modelo.predecir('Pumas UNAM', 'Necaxa', mostrar=True)
modelo.predecir('Leon', 'Puebla', mostrar=True)
```

_**[AÑADIR AQUÍ]:** Captura del archivo main.py abierto en un editor_

---

##  Casos de Uso Avanzados

### Automatizar Predicciones Semanales

Crea un script que genera predicciones para la jornada cada semana:

```python
from modelo_poisson import ModeloPoissonFutbol
from datetime import datetime

# Cargar y entrenar
modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Partidos de la semana
partidos_semana = [
    ('Club America', 'Cruz Azul'),
    ('Monterrey', 'Tigres UANL'),
    # ... más partidos
]

# Generar reporte
fecha = datetime.now().strftime('%Y-%m-%d')
modelo.simular_jornada(partidos_semana, mostrar=True)
modelo.exportar_parametros(f'predicciones_{fecha}.csv')
```

---

### Comparar Modelos de Diferentes Temporadas

```python
# Modelo temporada 2023
modelo_2023 = ModeloPoissonFutbol()
modelo_2023.cargar_datos('liga_mx_2023.csv')
modelo_2023.entrenar()

# Modelo temporada 2024
modelo_2024 = ModeloPoissonFutbol()
modelo_2024.cargar_datos('liga_mx_2024.csv')
modelo_2024.entrenar()

# Comparar predicciones
pred_2023 = modelo_2023.predecir('Club America', 'Cruz Azul', mostrar=False)
pred_2024 = modelo_2024.predecir('Club America', 'Cruz Azul', mostrar=False)

print(f"Predicción 2023: {pred_2023['marcador_mas_probable']}")
print(f"Predicción 2024: {pred_2024['marcador_mas_probable']}")
```

---

##  Próximos Pasos

Ahora que dominas la interfaz CLI:

1. **[Interpretación de Resultados](4-Interpretacion-de-Resultados)** - Entiende los números
2. **[Ejemplos y Casos de Uso](5-Ejemplos-y-Casos-de-Uso)** - Más ejemplos prácticos
3. **[Metodología](7-Metodologia-y-Fundamentos)** - Fundamentos matemáticos

---

[️ Anterior: Interfaz Web](2-Uso-Interfaz-Web) | [ Home](Home) | [️ Siguiente: Interpretación](4-Interpretacion-de-Resultados)
