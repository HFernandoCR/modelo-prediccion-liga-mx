# Bienvenido a la Wiki del Modelo de Predicción Liga MX

> **Modelo de Regresión de Poisson** para predecir resultados de partidos de fútbol
>
> **Autores:** Hector, Daniel, Uriel
> **Proyecto:** TecNM - Campus Oaxaca | Simulación
> **Año:** 2025

---

##  ¿Qué es este proyecto?

Este proyecto implementa un modelo estadístico basado en la **Distribución de Poisson** para predecir resultados de partidos de fútbol de la Liga MX. Utiliza técnicas de regresión avanzadas (GLM) para estimar las capacidades ofensivas y defensivas de cada equipo.

### Capturas del Sistema

_**[AÑADIR AQUÍ]:** Captura de pantalla de la interfaz principal de Streamlit_

_**[AÑADIR AQUÍ]:** Captura de pantalla de una predicción de ejemplo_

---

##  Navegación de la Wiki

### Para Usuarios Nuevos

1. **[Guía de Instalación Paso a Paso](1-Guia-de-Instalacion)** - Comienza aquí si es tu primera vez
2. **[Uso de la Interfaz Web](2-Uso-Interfaz-Web)** - La forma más fácil de usar el modelo
3. **[Interpretación de Resultados](4-Interpretacion-de-Resultados)** - Entiende qué significan las predicciones

### Para Usuarios Avanzados

4. **[Uso de la Interfaz CLI](3-Uso-CLI)** - Ejecuta el modelo desde terminal
5. **[Ejemplos y Casos de Uso](5-Ejemplos-y-Casos-de-Uso)** - Integra el modelo en tus scripts
6. **[Metodología y Fundamentos](7-Metodologia-y-Fundamentos)** - Detalles matemáticos del modelo

### Solución de Problemas

7. **[FAQ y Troubleshooting](6-FAQ-y-Troubleshooting)** - Problemas comunes y soluciones

---

##  Inicio Rápido

### Opción 1: Interfaz Web (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/HFernandoCR/modelo-prediccopm-liga-mx.git
cd modelo-prediccopm-liga-mx

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar interfaz web
streamlit run app.py
```

### Opción 2: Script CLI

```bash
python main.py
```

---

##  Características Principales

| Característica | Descripción |
|----------------|-------------|
|  **Modelo Estadístico** | Regresión de Poisson con Maximum Likelihood |
|  **Interfaz Web** | Aplicación interactiva con Streamlit |
|  **Interfaz CLI** | Script para ejecutar desde terminal |
|  **Rankings** | Clasificación de equipos por ataque (α) y defensa (β) |
|  **Predicciones** | Matriz de probabilidades para todos los marcadores |
|  **Visualizaciones** | Gráficos interactivos con Plotly |
|  **Exportación** | Resultados en CSV |

---

##  Tecnologías Utilizadas

```
Python 3.8+
├── pandas       - Manipulación de datos
├── numpy        - Operaciones numéricas
├── scipy        - Distribuciones estadísticas
├── statsmodels  - Modelos GLM (Poisson)
├── matplotlib   - Visualizaciones estáticas
├── seaborn      - Gráficos estadísticos
├── streamlit    - Interfaz web interactiva
└── plotly       - Visualizaciones interactivas
```

---

##  Video Demostrativo

> **[Ver video completo en Google Drive](https://drive.google.com/file/d/1uUBmX_DafaqtpT0YhSbXM9D529yJRdZu/view?usp=drive_link)**

El video muestra:
-  Predicciones con modelo pre-entrenado
-  Entrenamiento con datos personalizados
-  Visualizaciones interactivas
-  Interpretación de resultados

---

##  Estructura de la Documentación

### Nivel Básico
- Para usuarios sin experiencia en Python
- Guías paso a paso con capturas
- Explicaciones simples de conceptos

### Nivel Intermedio
- Para usuarios con conocimientos básicos de Python
- Uso programático del modelo
- Integración en proyectos propios

### Nivel Avanzado
- Detalles matemáticos del modelo
- Personalización de parámetros
- Extensión del modelo

---

##  Contribuciones y Contacto

**Autores:** Hector, Daniel, Uriel
**Institución:** TecNM - Campus Oaxaca
**Curso:** Simulación - 2025

Para reportar bugs o sugerir mejoras:
- Crea un [Issue en GitHub](https://github.com/HFernandoCR/modelo-prediccopm-liga-mx/issues)
- Contacta a los autores del proyecto

---

##  Licencia

Este proyecto es de uso académico para el TecNM - Campus Oaxaca.

---

** Desarrollado con Python 3.8+ | Streamlit | Statsmodels | Plotly**
