# 6. FAQ y Troubleshooting

Preguntas frecuentes y soluciones a problemas comunes.

---

##  Preguntas Frecuentes (FAQ)

### Sobre el Modelo

#### ¿Qué tan preciso es el modelo?

El modelo predice **tendencias y probabilidades**, no resultados exactos. Típicamente:
- **Favorito correcto:** 60-70% de las veces
- **Marcador exacto:** 10-20% de las veces (es normal, hay muchos marcadores posibles)

El modelo es mejor para identificar **quién tiene más probabilidad de ganar**, no el marcador exacto.

---

#### ¿Por qué mi predicción no coincide con el resultado real?

El modelo trabaja con **probabilidades**, no certezas. Si predice 60% de victoria local:
- **40% de las veces** el resultado será diferente (empate o victoria visitante)
- Esto es **normal y esperado** en un modelo probabilístico

Además, el modelo **no considera:**
- Lesiones de jugadores clave
- Motivación (necesidad de puntos)
- Clima extremo
- Árbitros
- Rachas recientes

---

#### ¿Con qué frecuencia debo actualizar el modelo?

**Recomendación:**
- **Cada 2-3 jornadas:** Para mantener el modelo actualizado
- **Después de transferencias importantes:** Si hay cambios significativos en planteles
- **Inicio de temporada:** Los primeros partidos pueden tener parámetros desactualizados

---

#### ¿Puedo usar el modelo para otras ligas?

**Sí**, solo necesitas:
1. Archivo CSV con el formato correcto
2. Al menos 30-50 partidos por equipo
3. Entrenar un modelo nuevo con esos datos

Funciona en cualquier liga: Premier League, La Liga, Bundesliga, etc.

---

#### ¿Por qué algunos equipos tienen α o β muy cercano a 1?

α = 1 y β = 1 representan el **promedio de la liga**. Equipos con valores cercanos a 1 son **equipos medianos**, ni muy fuertes ni muy débiles.

---

### Sobre los Parámetros

#### ¿Qué es mejor: α=1.2 con β=1.1 o α=1.0 con β=0.9?

Depende del contexto:

**α=1.2, β=1.1 (Equipo Ofensivo):**
- Mejor para **jugar de local** (aprovecha la ventaja)
- Partidos con **más goles** (over 2.5)
- Más espectacular pero inconsistente

**α=1.0, β=0.9 (Equipo Defensivo):**
- Mejor para **jugar de visita** (defensa sólida)
- Partidos con **menos goles** (under 2.5)
- Más consistente pero menos espectacular

El equipo "ideal" tendría **α alto y β bajo** (ataque fuerte + defensa fuerte).

---

#### ¿Por qué γ (gamma) es siempre el mismo para todos?

γ representa la **ventaja promedio de local en la liga**, no de cada equipo. En el modelo básico de Poisson, γ es **global**.

Algunos equipos tienen más ventaja de local que otros (ejemplo: mejor afición), pero el modelo no lo diferencia.

---

### Sobre Predicciones

#### ¿Qué significa "Marcador Más Probable: 2-1 (14.3%)"?

Significa:
- De **todos los marcadores posibles** (0-0, 1-0, 2-1, 3-2, etc.), el **más probable** es 2-1
- Pero solo tiene **14.3%** de probabilidad, así que hay **85.7%** de probabilidad de que sea otro marcador

**No te fíes solo del marcador más probable.** Mira las probabilidades de victoria/empate/derrota.

---

#### ¿Cómo usar el modelo para apuestas?

1. **Compara probabilidades del modelo con cuotas**:
   - Si el modelo dice 60% de victoria local y las cuotas pagan 2.0x
   - Valor esperado = 2.0 × 0.60 = 1.20 (20% de ganancia esperada)
   - Es una **apuesta con valor positivo**

2. **No apuestes a marcador exacto** (muy baja probabilidad)

3. **Usa para apuestas de resultado** (1X2) o **totales de goles** (over/under)

** ADVERTENCIA:** El modelo NO garantiza ganancias. Las apuestas siempre tienen riesgo.

---

#### ¿El modelo considera partidos de visitante vs local?

**Sí**, automáticamente:
- El primer equipo se considera **local**
- El segundo equipo se considera **visitante**
- La ventaja de local (γ) se aplica automáticamente

```python
modelo.predecir('Club America', 'Cruz Azul')
# Club America = local (con ventaja γ)
# Cruz Azul = visitante (sin ventaja)
```

---

##  Troubleshooting - Problemas Comunes

### Problemas de Instalación

#### Error: "python no se reconoce como un comando interno o externo"

**Causa:** Python no está en el PATH del sistema

**Soluciones:**

1. **Reinstalar Python:**
   - Descarga desde [python.org](https://www.python.org/downloads/)
   - **MARCA** la casilla "Add Python to PATH" durante instalación

_**[AÑADIR AQUÍ]:** Captura de instalador con PATH marcado_

2. **Usar `py` en lugar de `python`:**
   ```bash
   py --version
   py -m venv venv
   ```

3. **Agregar manualmente al PATH:**
   - Buscar "Variables de entorno" en Windows
   - Agregar `C:\Python311` (o tu ruta) al PATH

_**[AÑADIR AQUÍ]:** Captura de variables de entorno_

---

#### Error: "No se puede activar el entorno virtual" (Windows)

**Error completo:**
```
.\venv\Scripts\activate : No se puede cargar el archivo... porque la ejecución de scripts está deshabilitada en este sistema.
```

**Causa:** Política de ejecución de PowerShell

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

_**[AÑADIR AQUÍ]:** Captura ejecutando el comando_

Luego intenta activar de nuevo:
```powershell
.\venv\Scripts\activate
```

---

#### Error al instalar dependencias: "Failed building wheel for..."

**Causa:** Falta compilador C++ o pip desactualizado

**Soluciones:**

1. **Actualizar pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Instalar Microsoft C++ Build Tools:**
   - Descarga desde [visualstudio.microsoft.com](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Instala "Desktop development with C++"

3. **Instalar paquetes pre-compilados:**
   ```bash
   pip install --only-binary :all: -r requirements.txt
   ```

---

### Problemas con Streamlit

#### Error: "streamlit: command not found"

**Causa:** Entorno virtual no está activado

**Solución:**
1. Verifica que veas `(venv)` en tu prompt
2. Si no lo ves, activa el entorno:
   ```bash
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

---

#### Streamlit no abre el navegador automáticamente

**Solución:**
- Abre manualmente: `http://localhost:8501`
- O usa:
  ```bash
  streamlit run app.py --server.headless false
  ```

---

#### Error: "Address already in use"

**Causa:** Otra aplicación Streamlit está corriendo en el puerto 8501

**Solución:**

1. **Cerrar la aplicación anterior:**
   - Busca la terminal con Streamlit y presiona `Ctrl+C`

2. **Usar otro puerto:**
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

### Problemas con el Modelo

#### Error: "Equipo no encontrado en el modelo"

**Causa:** El nombre del equipo no coincide exactamente

**Solución:**
1. **Ver lista de equipos disponibles:**
   ```python
   modelo = ModeloPoissonFutbol()
   modelo.cargar_datos('liga_mx_data_limpia.csv')
   print(modelo.equipos)
   ```

2. **Usar el nombre exacto:**
   -  `'America'` o `'América'`
   -  `'Club America'`

_**[AÑADIR AQUÍ]:** Captura del error y la solución_

---

#### Error: "Modelo no convergió" o "Singular matrix"

**Causa:** Datos insuficientes o equipos con pocos partidos

**Solución:**
1. **Verifica que cada equipo tenga al menos 20-30 partidos**
2. **Elimina equipos con muy pocos datos:**
   ```python
   # Antes de entrenar
   df = pd.read_csv('datos.csv')
   counts = df['HomeTeam'].value_counts() + df['AwayTeam'].value_counts()
   equipos_validos = counts[counts >= 20].index
   df = df[df['HomeTeam'].isin(equipos_validos) & df['AwayTeam'].isin(equipos_validos)]
   ```

---

#### El modelo da probabilidades extrañas (ejemplo: 95% de victoria)

**Posibles causas:**
1. **Diferencia de nivel muy grande** (ejemplo: campeón vs último lugar)
   - Esto es normal, el modelo detectó la diferencia
2. **Datos desbalanceados** (un equipo con muchas victorias en la muestra)
   - Actualiza con datos más recientes

---

### Problemas con CSV

#### Error: "UnicodeDecodeError" al cargar CSV

**Causa:** Encoding incorrecto del archivo

**Solución:**
1. **Guardar CSV como UTF-8:**
   - Excel: "Guardar como"  "CSV UTF-8"
   - Google Sheets: "Archivo"  "Descargar"  "CSV"

2. **Especificar encoding:**
   ```python
   modelo.cargar_datos('datos.csv', encoding='latin-1')
   ```

_**[AÑADIR AQUÍ]:** Captura de Excel guardando como UTF-8_

---

#### Error: "KeyError: 'FTHG'" al cargar datos

**Causa:** El CSV no tiene las columnas correctas

**Solución:**
Verifica que tu CSV tenga **exactamente** estas columnas:
- `Date`
- `HomeTeam`
- `AwayTeam`
- `FTHG` (Full Time Home Goals)
- `FTAG` (Full Time Away Goals)

_**[AÑADIR AQUÍ]:** Captura de un CSV bien formateado_

---

#### Los nombres de equipos tienen caracteres raros (�)

**Causa:** Problema de encoding

**Solución:**
1. Abre el CSV en un editor de texto (Notepad++, VSCode)
2. Cambia encoding a UTF-8
3. Guarda el archivo
4. Vuelve a cargar

---

##  Comandos Útiles para Diagnóstico

### Verificar instalación de Python

```bash
python --version
python -m pip --version
```

### Verificar paquetes instalados

```bash
pip list
pip show streamlit
pip show statsmodels
```

### Ver información del entorno

```bash
python -c "import sys; print(sys.executable)"
python -c "import streamlit; print(streamlit.__version__)"
```

### Reinstalar un paquete problemático

```bash
pip uninstall statsmodels
pip install statsmodels --no-cache-dir
```

### Limpiar caché de pip

```bash
pip cache purge
```

---

##  Problemas de Rendimiento

### Streamlit corre muy lento

**Soluciones:**
1. **Usar modelo pre-entrenado** en lugar de entrenar en cada predicción
2. **Cachear resultados:**
   ```python
   @st.cache_resource
   def cargar_modelo():
       modelo = ModeloPoissonFutbol()
       modelo.cargar_datos('liga_mx_data_limpia.csv')
       modelo.entrenar()
       return modelo
   ```

3. **Reducir tamaño del dataset** (solo temporadas recientes)

---

### El entrenamiento tarda mucho

**Causas:**
- Dataset muy grande (>2000 partidos)
- Muchos equipos (>30)

**Soluciones:**
1. **Filtrar por temporada:**
   ```python
   df = pd.read_csv('datos.csv')
   df['Date'] = pd.to_datetime(df['Date'])
   df = df[df['Date'] >= '2023-01-01']
   ```

2. **Es normal:** Un modelo con 18 equipos y 600 partidos puede tardar 5-10 segundos

---

##  Mejores Prácticas

### Para evitar problemas:

 **Siempre usa entorno virtual**
 **Mantén Python actualizado** (3.8+)
 **Actualiza pip regularmente:** `pip install --upgrade pip`
 **Usa nombres de equipos consistentes** en tu CSV
 **Guarda CSVs en UTF-8**
 **Incluye suficientes datos** (mínimo 30 partidos por equipo)
 **Actualiza el modelo regularmente** con nuevos datos

---

##  ¿Aún tienes problemas?

Si ninguna solución funcionó:

1. **Revisa la documentación oficial:**
   - [Streamlit Docs](https://docs.streamlit.io/)
   - [Statsmodels Docs](https://www.statsmodels.org/)

2. **Crea un Issue en GitHub:**
   - Ve a: https://github.com/HFernandoCR/modelo-prediccopm-liga-mx/issues
   - Incluye:
     - Mensaje de error completo
     - Versión de Python (`python --version`)
     - Sistema operativo
     - Pasos para reproducir el problema

_**[AÑADIR AQUÍ]:** Captura de cómo crear un Issue en GitHub_

3. **Verifica que tienes la última versión:**
   ```bash
   git pull origin main
   ```

---

##  Próximos Pasos

1. **[Metodología y Fundamentos](7-Metodologia-y-Fundamentos)** - Detalles matemáticos del modelo
2. **[Ejemplos](5-Ejemplos-y-Casos-de-Uso)** - Más casos de uso prácticos
3. **[Home](Home)** - Volver al inicio

---

[️ Anterior: Ejemplos](5-Ejemplos-y-Casos-de-Uso) | [ Home](Home) | [️ Siguiente: Metodología](7-Metodologia-y-Fundamentos)
