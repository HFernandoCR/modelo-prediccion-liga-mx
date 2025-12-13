# 5. Ejemplos y Casos de Uso

Esta página contiene ejemplos prácticos y casos de uso reales del modelo de predicción.

---

##  Ejemplos Rápidos

### Ejemplo 1: Predicción Simple

**Objetivo:** Predecir el resultado del Clásico Joven (Club America vs Cruz Azul)

```python
from modelo_poisson import ModeloPoissonFutbol

# Crear y entrenar modelo
modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Predecir
resultado = modelo.predecir('Club America', 'Cruz Azul', mostrar=True)
```

_**[AÑADIR AQUÍ]:** Captura de la salida del código_

**Salida:**
```
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

---

### Ejemplo 2: Obtener Rankings

**Objetivo:** Ver los 5 mejores ataques y defensas

```python
from modelo_poisson import ModeloPoissonFutbol

modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Top 5 ataques
print("=== TOP 5 ATAQUES ===")
top_ataque = modelo.obtener_ranking_ataque(top_n=5)
print(top_ataque)

# Top 5 defensas
print("\n=== TOP 5 DEFENSAS ===")
top_defensa = modelo.obtener_ranking_defensa(top_n=5)
print(top_defensa)
```

_**[AÑADIR AQUÍ]:** Captura de la salida del código_

---

### Ejemplo 3: Analizar un Equipo Específico

**Objetivo:** Analizar las fortalezas y debilidades de Tigres UANL

```python
from modelo_poisson import ModeloPoissonFutbol

modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Obtener parámetros
params = modelo.obtener_parametros_equipo('Tigres UANL')

print(f"Tigres UANL:")
print(f"  Alpha (Ataque): {params['alpha']:.3f}")
print(f"  Beta (Defensa): {params['beta']:.3f}")
print(f"  Interpretación: {params['interpretacion_alpha']}")
```

_**[AÑADIR AQUÍ]:** Captura de la salida del código_

---

##  Casos de Uso Avanzados

### Caso 1: Predicciones de Jornada Completa

**Escenario:** Quieres predecir todos los partidos de la Jornada 15

```python
from modelo_poisson import ModeloPoissonFutbol

modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Partidos de la Jornada 15
partidos_j15 = [
    ('Club America', 'Cruz Azul'),
    ('Monterrey', 'Tigres UANL'),
    ('Chivas Guadalajara', 'Atlas'),
    ('Pumas UNAM', 'Toluca'),
    ('Leon', 'Santos Laguna'),
    ('Puebla', 'Necaxa'),
    ('Pachuca', 'Queretaro'),
    ('Tijuana', 'Mazatlan FC'),
    ('Juarez FC', 'San Luis')
]

# Simular jornada
resultados = modelo.simular_jornada(partidos_j15, mostrar=True)

# Exportar a CSV
import pandas as pd
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv('jornada_15_predicciones.csv', index=False)
print("\n Predicciones exportadas a 'jornada_15_predicciones.csv'")
```

_**[AÑADIR AQUÍ]:** Captura de la salida mostrando todos los partidos_

_**[AÑADIR AQUÍ]:** Captura del archivo CSV abierto en Excel_

---

### Caso 2: Comparar Múltiples Equipos

**Escenario:** Comparar los "Grandes" de la Liga MX

```python
from modelo_poisson import ModeloPoissonFutbol

modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Equipos "grandes"
grandes = [
    'Club America',
    'Cruz Azul',
    'Chivas Guadalajara',
    'Pumas UNAM',
    'Tigres UANL',
    'Monterrey'
]

# Comparar
comparacion = modelo.comparar_equipos(grandes)

# Mostrar en formato tabla
import pandas as pd
df = pd.DataFrame(comparacion)
df = df.sort_values('alpha', ascending=False)

print("\n=== COMPARACIÓN DE GRANDES ===")
print(df.to_string(index=False))
```

_**[AÑADIR AQUÍ]:** Captura de la tabla de comparación_

---

### Caso 3: Análisis de Ventaja Local

**Escenario:** Comparar cómo afecta jugar en casa vs visita

```python
from modelo_poisson import ModeloPoissonFutbol

modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

equipo = 'Club America'
rival = 'Cruz Azul'

# Predicción como local
print(f"=== {equipo} jugando en CASA ===")
pred_casa = modelo.predecir(equipo, rival, mostrar=True)

print("\n" + "="*60 + "\n")

# Predicción como visitante
print(f"=== {equipo} jugando de VISITA ===")
pred_visita = modelo.predecir(rival, equipo, mostrar=True)

# Análisis
print("\n=== ANÁLISIS DE VENTAJA LOCAL ===")
print(f"Lambda como local:     {pred_casa['lambda_local']:.2f} goles")
print(f"Lambda como visitante: {pred_visita['lambda_visitante']:.2f} goles")
diferencia = pred_casa['lambda_local'] - pred_visita['lambda_visitante']
print(f"Diferencia:            {diferencia:.2f} goles ({diferencia/pred_visita['lambda_visitante']*100:.1f}%)")
```

_**[AÑADIR AQUÍ]:** Captura del análisis completo_

---

### Caso 4: Identificar "Chollo" (Value Bet)

**Escenario:** Encontrar apuestas con valor positivo

```python
from modelo_poisson import ModeloPoissonFutbol

modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Cuotas de la casa de apuestas (ejemplo)
cuotas = {
    'local': 1.75,
    'empate': 3.50,
    'visitante': 4.50
}

# Predecir
partido = ('Tigres UANL', 'Juarez FC')
pred = modelo.predecir(partido[0], partido[1], mostrar=False)

# Calcular probabilidades implícitas de las cuotas
prob_impl_local = 1 / cuotas['local']
prob_impl_empate = 1 / cuotas['empate']
prob_impl_visitante = 1 / cuotas['visitante']

# Comparar con modelo
print(f"=== ANÁLISIS DE VALUE BET: {partido[0]} vs {partido[1]} ===\n")

print("VICTORIA LOCAL:")
print(f"  Cuota:              {cuotas['local']:.2f}x")
print(f"  Prob. Implícita:    {prob_impl_local*100:.1f}%")
print(f"  Prob. Modelo:       {pred['prob_victoria_local']*100:.1f}%")
valor_local = (cuotas['local'] * pred['prob_victoria_local']) - 1
print(f"  Valor Esperado:     {valor_local*100:+.1f}%")
if valor_local > 0:
    print(f"   VALUE BET - Apostar!")
else:
    print(f"   No hay valor")

print("\nEMPATE:")
print(f"  Cuota:              {cuotas['empate']:.2f}x")
print(f"  Prob. Implícita:    {prob_impl_empate*100:.1f}%")
print(f"  Prob. Modelo:       {pred['prob_empate']*100:.1f}%")
valor_empate = (cuotas['empate'] * pred['prob_empate']) - 1
print(f"  Valor Esperado:     {valor_empate*100:+.1f}%")
if valor_empate > 0:
    print(f"   VALUE BET - Apostar!")
else:
    print(f"   No hay valor")

print("\nVICTORIA VISITANTE:")
print(f"  Cuota:              {cuotas['visitante']:.2f}x")
print(f"  Prob. Implícita:    {prob_impl_visitante*100:.1f}%")
print(f"  Prob. Modelo:       {pred['prob_victoria_visitante']*100:.1f}%")
valor_visitante = (cuotas['visitante'] * pred['prob_victoria_visitante']) - 1
print(f"  Valor Esperado:     {valor_visitante*100:+.1f}%")
if valor_visitante > 0:
    print(f"   VALUE BET - Apostar!")
else:
    print(f"   No hay valor")
```

_**[AÑADIR AQUÍ]:** Captura del análisis de value bet_

---

### Caso 5: Fantasy Football - Seleccionar Delantero

**Escenario:** Elegir qué delantero incluir en tu equipo fantasy

```python
from modelo_poisson import ModeloPoissonFutbol

modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Partidos de la jornada con delanteros disponibles
candidatos = [
    {'delantero': 'Henry Martin', 'equipo': 'Club America', 'rival': 'Juarez FC'},
    {'delantero': 'Gignac', 'equipo': 'Tigres UANL', 'rival': 'San Luis'},
    {'delantero': 'Funes Mori', 'equipo': 'Monterrey', 'rival': 'Necaxa'},
]

print("=== ANÁLISIS FANTASY FOOTBALL ===\n")

resultados_fantasy = []

for c in candidatos:
    pred = modelo.predecir(c['equipo'], c['rival'], mostrar=False)

    # Score fantasy = goles esperados × probabilidad de victoria
    score = pred['lambda_local'] * pred['prob_victoria_local']

    resultados_fantasy.append({
        'Delantero': c['delantero'],
        'Equipo': c['equipo'],
        'vs': c['rival'],
        'Lambda': pred['lambda_local'],
        'Prob. Victoria': pred['prob_victoria_local'],
        'Score Fantasy': score
    })

# Ordenar por score
import pandas as pd
df = pd.DataFrame(resultados_fantasy)
df = df.sort_values('Score Fantasy', ascending=False)

print(df.to_string(index=False))
print(f"\n Mejor elección: {df.iloc[0]['Delantero']} ({df.iloc[0]['Equipo']})")
```

_**[AÑADIR AQUÍ]:** Captura del análisis de fantasy_

---

### Caso 6: Análisis Temporal - Comparar Temporadas

**Escenario:** Ver cómo ha evolucionado un equipo entre temporadas

```python
from modelo_poisson import ModeloPoissonFutbol

# Modelo temporada 2023
modelo_2023 = ModeloPoissonFutbol()
modelo_2023.cargar_datos('liga_mx_2023.csv')
modelo_2023.entrenar()

# Modelo temporada 2024
modelo_2024 = ModeloPoissonFutbol()
modelo_2024.cargar_datos('liga_mx_2024.csv')
modelo_2024.entrenar()

# Comparar Club America
equipo = 'Club America'

params_2023 = modelo_2023.obtener_parametros_equipo(equipo)
params_2024 = modelo_2024.obtener_parametros_equipo(equipo)

print(f"=== EVOLUCIÓN DE {equipo} ===\n")

print("TEMPORADA 2023:")
print(f"  Alpha: {params_2023['alpha']:.3f}")
print(f"  Beta:  {params_2023['beta']:.3f}")

print("\nTEMPORADA 2024:")
print(f"  Alpha: {params_2024['alpha']:.3f}")
print(f"  Beta:  {params_2024['beta']:.3f}")

print("\nCAMBIOS:")
cambio_alpha = ((params_2024['alpha'] / params_2023['alpha']) - 1) * 100
cambio_beta = ((params_2024['beta'] / params_2023['beta']) - 1) * 100

print(f"  Ataque:  {cambio_alpha:+.1f}%")
print(f"  Defensa: {cambio_beta:+.1f}% (negativo = mejor)")

if cambio_alpha > 5:
    print("\n Ataque mejoró significativamente")
elif cambio_alpha < -5:
    print("\n Ataque empeoró")
else:
    print("\n️ Ataque se mantuvo estable")

if cambio_beta < -5:
    print(" Defensa mejoró significativamente")
elif cambio_beta > 5:
    print(" Defensa empeoró")
else:
    print("️ Defensa se mantuvo estable")
```

_**[AÑADIR AQUÍ]:** Captura del análisis temporal_

---

### Caso 7: Exportar Todo a CSV

**Escenario:** Exportar todos los datos para análisis en Excel

```python
from modelo_poisson import ModeloPoissonFutbol
import pandas as pd

modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Exportar parámetros de todos los equipos
modelo.exportar_parametros('parametros_todos.csv')

# Exportar rankings
ranking_ataque = modelo.obtener_ranking_ataque()
ranking_ataque.to_csv('ranking_ataque_completo.csv', index=False)

ranking_defensa = modelo.obtener_ranking_defensa()
ranking_defensa.to_csv('ranking_defensa_completo.csv', index=False)

# Generar matriz de probabilidades para todos los partidos posibles
equipos = modelo.equipos
predicciones_todas = []

for local in equipos:
    for visitante in equipos:
        if local != visitante:
            pred = modelo.predecir(local, visitante, mostrar=False)
            predicciones_todas.append({
                'Local': local,
                'Visitante': visitante,
                'Lambda_Local': pred['lambda_local'],
                'Lambda_Visitante': pred['lambda_visitante'],
                'Marcador_Probable': f"{pred['marcador_mas_probable'][0]}-{pred['marcador_mas_probable'][1]}",
                'Prob_Victoria_Local': pred['prob_victoria_local'],
                'Prob_Empate': pred['prob_empate'],
                'Prob_Victoria_Visitante': pred['prob_victoria_visitante']
            })

df_todas = pd.DataFrame(predicciones_todas)
df_todas.to_csv('matriz_predicciones_completa.csv', index=False)

print(" Archivos exportados:")
print("  • parametros_todos.csv")
print("  • ranking_ataque_completo.csv")
print("  • ranking_defensa_completo.csv")
print("  • matriz_predicciones_completa.csv")
```

_**[AÑADIR AQUÍ]:** Captura de los archivos CSV en el explorador_

_**[AÑADIR AQUÍ]:** Captura de matriz_predicciones_completa.csv en Excel con formato condicional_

---

##  Plantillas Útiles

### Plantilla: Script de Análisis Semanal

Guarda esto como `analisis_semanal.py`:

```python
"""
Script para generar análisis semanal de la Liga MX
Ejecutar: python analisis_semanal.py
"""

from modelo_poisson import ModeloPoissonFutbol
from datetime import datetime
import pandas as pd

# Configuración
ARCHIVO_DATOS = 'liga_mx_data_limpia.csv'
PARTIDOS_SEMANA = [
    # Agregar partidos de la semana aquí
    ('Club America', 'Cruz Azul'),
    ('Monterrey', 'Tigres UANL'),
    # ...
]

def main():
    print("="*60)
    print("ANÁLISIS SEMANAL - LIGA MX")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60 + "\n")

    # Cargar y entrenar modelo
    print("Cargando modelo...")
    modelo = ModeloPoissonFutbol()
    modelo.cargar_datos(ARCHIVO_DATOS)
    modelo.entrenar()
    print(" Modelo entrenado\n")

    # Simular jornada
    print("Generando predicciones...\n")
    resultados = modelo.simular_jornada(PARTIDOS_SEMANA, mostrar=True)

    # Exportar
    fecha = datetime.now().strftime('%Y%m%d')
    archivo_salida = f'predicciones_{fecha}.csv'

    df = pd.DataFrame(resultados)
    df.to_csv(archivo_salida, index=False)

    print(f"\n Predicciones exportadas a '{archivo_salida}'")

if __name__ == '__main__':
    main()
```

_**[AÑADIR AQUÍ]:** Captura ejecutando el script_

---

### Plantilla: Dashboard en Jupyter Notebook

```python
# Celda 1: Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from modelo_poisson import ModeloPoissonFutbol

%matplotlib inline
sns.set_style('darkgrid')

# Celda 2: Cargar modelo
modelo = ModeloPoissonFutbol()
modelo.cargar_datos('liga_mx_data_limpia.csv')
modelo.entrenar()

# Celda 3: Rankings visuales
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Ataque
ranking_ataque = modelo.obtener_ranking_ataque(top_n=10)
ax1.barh(ranking_ataque['equipo'], ranking_ataque['alpha'], color='green')
ax1.set_xlabel('Alpha (Ataque)')
ax1.set_title('Top 10 Mejores Ataques')
ax1.invert_yaxis()

# Defensa
ranking_defensa = modelo.obtener_ranking_defensa(top_n=10)
ax2.barh(ranking_defensa['equipo'], ranking_defensa['beta'], color='blue')
ax2.set_xlabel('Beta (Defensa)')
ax2.set_title('Top 10 Mejores Defensas')
ax2.invert_yaxis()

plt.tight_layout()
plt.show()

# Celda 4: Predicción interactiva
def predecir_interactivo(local, visitante):
    pred = modelo.predecir(local, visitante, mostrar=True)
    return pred

# Ejemplo
predecir_interactivo('Club America', 'Cruz Azul')
```

_**[AÑADIR AQUÍ]:** Captura del Jupyter Notebook con gráficos_

---

##  Próximos Pasos

1. **[Troubleshooting](6-FAQ-y-Troubleshooting)** - Solución de problemas comunes
2. **[Metodología](7-Metodologia-y-Fundamentos)** - Entender las matemáticas
3. **[Home](Home)** - Volver al inicio

---

[️ Anterior: Interpretación](4-Interpretacion-de-Resultados) | [ Home](Home) | [️ Siguiente: FAQ](6-FAQ-y-Troubleshooting)
