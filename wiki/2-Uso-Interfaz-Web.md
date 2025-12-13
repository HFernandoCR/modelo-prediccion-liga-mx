# 2. Uso de la Interfaz Web (Streamlit)

La interfaz web es la forma más fácil e intuitiva de usar el modelo de predicción. No requiere conocimientos de programación.

---

##  Iniciar la Aplicación Web

**Paso 1:** Con el entorno virtual activado (debe mostrar `(venv)`), ejecuta:

```bash
streamlit run app.py
```

_**[AÑADIR AQUÍ]:** Captura del comando ejecutándose en la terminal_

**Paso 2:** Se abrirá automáticamente en tu navegador web (generalmente en `http://localhost:8501`)

_**[AÑADIR AQUÍ]:** Captura de la pantalla principal de Streamlit al abrir_

---

##  Modos de Operación

La aplicación tiene **dos modos principales**:

###  Modo 1: Usar Modelo Pre-entrenado (Liga MX)
- **Recomendado para:** Usuarios que quieren predicciones rápidas de la Liga MX
- **Ventaja:** No necesitas datos históricos, el modelo ya está entrenado
- **Equipos disponibles:** 18 equipos de la Liga MX actual

###  Modo 2: Entrenar Nuevo Modelo
- **Recomendado para:** Usuarios con datos de otras ligas o temporadas
- **Ventaja:** Personaliza el modelo con tus propios datos
- **Requiere:** Archivo CSV con formato específico

---

##  Modo 1: Usar Modelo Pre-entrenado

### Seleccionar Modo

**Paso 1:** En la barra lateral izquierda, selecciona **"Usar modelo pre-entrenado"**

_**[AÑADIR AQUÍ]:** Captura del sidebar mostrando la opción seleccionada_

---

### Seleccionar Equipos

**Paso 2:** Elige el equipo **local** (que juega en casa)

_**[AÑADIR AQUÍ]:** Captura del selector de equipo local desplegado_

**Paso 3:** Elige el equipo **visitante**

_**[AÑADIR AQUÍ]:** Captura del selector de equipo visitante desplegado_

**Equipos disponibles:**
- Club America
- Cruz Azul
- Tigres UANL
- Monterrey
- Pumas UNAM
- Chivas Guadalajara
- Atlas
- Santos Laguna
- Toluca
- Leon
- Puebla
- Necaxa
- Pachuca
- Queretaro
- Tijuana
- Mazatlan FC
- Juarez FC
- San Luis

---

### Obtener Predicción

**Paso 4:** Haz clic en el botón **"Predecir Resultado"**

_**[AÑADIR AQUÍ]:** Captura del botón "Predecir Resultado"_

---

### Interpretar Resultados

La predicción se divide en **3 pestañas (tabs)**:

#### Tab 1:  Predicción

_**[AÑADIR AQUÍ]:** Captura completa del tab de Predicción_

**Sección Superior - Métricas Clave:**

_**[AÑADIR AQUÍ]:** Captura de las métricas (λ local, λ visitante, marcador más probable)_

Muestra:
- **Goles Esperados Local (λ):** Promedio de goles que se espera marque el equipo local
- **Goles Esperados Visitante (λ):** Promedio de goles que se espera marque el visitante
- **Marcador Más Probable:** El resultado con mayor probabilidad

**Sección Media - Probabilidades de Resultado:**

_**[AÑADIR AQUÍ]:** Captura del gráfico de barras de probabilidades_

Gráfico de barras mostrando:
-  **Victoria Local:** Probabilidad de que gane el equipo de casa
-  **Empate:** Probabilidad de que empaten
-  **Victoria Visitante:** Probabilidad de que gane el visitante

**Sección Inferior - Matriz de Probabilidades (Heatmap):**

_**[AÑADIR AQUÍ]:** Captura del heatmap completo e interactivo_

- **Filas:** Goles del equipo local (0, 1, 2, 3, 4, 5)
- **Columnas:** Goles del equipo visitante (0, 1, 2, 3, 4, 5)
- **Color:** Más verde = mayor probabilidad
- **Hover:** Pasa el mouse sobre una celda para ver la probabilidad exacta

_**[AÑADIR AQUÍ]:** Captura del tooltip al hacer hover en el heatmap_

---

#### Tab 2:  Rankings

_**[AÑADIR AQUÍ]:** Captura completa del tab de Rankings_

**Ranking de Ataque (α - Alpha):**

_**[AÑADIR AQUÍ]:** Captura de la tabla de ranking de ataque_

- **α > 1:** Ataque superior al promedio
- **α = 1:** Ataque promedio
- **α < 1:** Ataque inferior al promedio

**Ranking de Defensa (β - Beta):**

_**[AÑADIR AQUÍ]:** Captura de la tabla de ranking de defensa_

- **β < 1:** Defensa fuerte (permite menos goles)
- **β = 1:** Defensa promedio
- **β > 1:** Defensa débil (permite más goles)

** Interpretación:**
- Un equipo ideal tendría **α alto** (buen ataque) y **β bajo** (buena defensa)

---

#### Tab 3: ℹ️ Info del Modelo

_**[AÑADIR AQUÍ]:** Captura del tab de información_

**Parámetros del Equipo Local:**

_**[AÑADIR AQUÍ]:** Captura de los parámetros del equipo local_

Muestra:
- **Alpha (α):** Fuerza ofensiva
- **Beta (β):** Debilidad defensiva
- **Interpretación:** Texto descriptivo de las capacidades

**Parámetros del Equipo Visitante:**

Similar al local pero para el equipo visitante.

**Ventaja de Local (γ - Gamma):**

_**[AÑADIR AQUÍ]:** Captura del parámetro gamma_

- Típicamente entre 1.2 - 1.4
- Representa el factor de incremento de goles esperados al jugar en casa

**Metodología del Modelo:**

_**[AÑADIR AQUÍ]:** Captura de la sección de metodología_

Explicación breve del modelo de Poisson y las fórmulas utilizadas.

---

##  Modo 2: Entrenar Nuevo Modelo

### Cuando usar este modo

- Tienes datos de otra liga (Premier League, La Liga, etc.)
- Quieres entrenar con una temporada específica
- Tienes datos históricos propios

---

### Paso A: Preparar tu archivo CSV

**Formato requerido:**

```csv
Date,HomeTeam,AwayTeam,FTHG,FTAG
2023-07-15,Club America,Cruz Azul,2,1
2023-07-16,Tigres UANL,Monterrey,1,1
2023-07-22,Cruz Azul,Pumas UNAM,3,0
...
```

**Columnas necesarias:**
- `Date`: Fecha del partido (formato: YYYY-MM-DD)
- `HomeTeam`: Nombre del equipo local
- `AwayTeam`: Nombre del equipo visitante
- `FTHG`: Full Time Home Goals (goles del local)
- `FTAG`: Full Time Away Goals (goles del visitante)

---

### Paso B: Descargar Plantilla (Opcional)

**Paso 1:** En el sidebar, selecciona **"Entrenar nuevo modelo"**

_**[AÑADIR AQUÍ]:** Captura del sidebar con modo "Entrenar nuevo modelo" seleccionado_

**Paso 2:** Haz clic en el botón **" Descargar plantilla CSV"**

_**[AÑADIR AQUÍ]:** Captura del botón de descarga de plantilla_

Esto descargará un archivo de ejemplo que puedes modificar.

---

### Paso C: Subir tu CSV

**Paso 3:** Haz clic en **"Browse files"** o arrastra tu archivo CSV

_**[AÑADIR AQUÍ]:** Captura del componente de carga de archivos_

**Paso 4:** Selecciona tu archivo CSV desde tu computadora

_**[AÑADIR AQUÍ]:** Captura del diálogo de selección de archivos_

---

### Paso D: Entrenar el Modelo

El modelo se entrenará automáticamente al subir el archivo.

_**[AÑADIR AQUÍ]:** Captura del mensaje de éxito "Modelo entrenado exitosamente"_

Verás:
-  Mensaje de confirmación
-  Número de equipos detectados
-  Número de partidos procesados

---

### Paso E: Hacer Predicciones

Una vez entrenado, el flujo es igual que en el Modo 1:

1. Selecciona equipo local
2. Selecciona equipo visitante
3. Haz clic en "Predecir Resultado"

_**[AÑADIR AQUÍ]:** Captura de una predicción con modelo personalizado_

---

##  Consejos y Buenas Prácticas

### Para Mejores Resultados

 **Datos suficientes:** Al menos 30-50 partidos por equipo
 **Datos recientes:** Temporadas actuales predicen mejor que datos muy antiguos
 **Nombres consistentes:** Usa siempre el mismo nombre para cada equipo

### Errores Comunes a Evitar

 **CSV mal formateado:** Revisa que tenga las 5 columnas exactas
 **Nombres con tildes/símbolos raros:** Pueden causar problemas de encoding
 **Pocos partidos:** Menos de 20 partidos por equipo da resultados poco confiables

---

##  Cerrar la Aplicación

Para detener la aplicación web:

**Opción 1:** Cierra la pestaña del navegador y presiona `Ctrl + C` en la terminal

_**[AÑADIR AQUÍ]:** Captura de terminal mostrando Ctrl+C deteniendo Streamlit_

**Opción 2:** Presiona `Ctrl + C` en la terminal directamente

---

##  Próximos Pasos

Ahora que sabes usar la interfaz web:

1. **[Interpretación de Resultados](4-Interpretacion-de-Resultados)** - Entiende qué significan los números
2. **[Ejemplos y Casos de Uso](5-Ejemplos-y-Casos-de-Uso)** - Ejemplos prácticos
3. **[Uso de CLI](3-Uso-CLI)** - Si prefieres trabajar desde terminal

---

##  Problemas Comunes

### La aplicación no abre en el navegador

**Solución:** Abre manualmente `http://localhost:8501` en tu navegador

### Error al subir CSV

**Solución:** Verifica que:
- El archivo tenga extensión `.csv`
- Tenga las columnas: Date, HomeTeam, AwayTeam, FTHG, FTAG
- Esté codificado en UTF-8

### Los equipos no aparecen después de entrenar

**Solución:**
- Refresca la página (F5)
- Verifica que el CSV tenga al menos 20 partidos

---

[️ Anterior: Instalación](1-Guia-de-Instalacion) | [ Home](Home) | [️ Siguiente: Uso CLI](3-Uso-CLI)
