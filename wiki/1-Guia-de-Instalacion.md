# 1. Guía de Instalación Paso a Paso

Esta guía te llevará paso a paso por el proceso de instalación del modelo de predicción de Liga MX.

---

##  Requisitos Previos

### Verificar Python Instalado

Antes de comenzar, necesitas tener **Python 3.8 o superior** instalado.

**Paso 1:** Abre tu terminal o PowerShell y ejecuta:

```bash
python --version
```

o en algunos sistemas:

```bash
python3 --version
```

_**[AÑADIR AQUÍ]:** Captura de pantalla mostrando el resultado del comando `python --version`_

**Deberías ver algo como:**
```
Python 3.8.10
```
o superior (3.9, 3.10, 3.11, 3.12, etc.)

---

### Si no tienes Python instalado

**Paso 2:** Descarga Python desde [python.org](https://www.python.org/downloads/)

_**[AÑADIR AQUÍ]:** Captura de pantalla de la página de descarga de Python_

** IMPORTANTE para Windows:**
- Durante la instalación, marca la casilla **"Add Python to PATH"**

_**[AÑADIR AQUÍ]:** Captura del instalador de Python con la opción "Add Python to PATH" marcada_

---

##  Paso 1: Clonar el Repositorio

### Opción A: Usando Git (Recomendado)

**Paso 3:** Abre tu terminal en la carpeta donde quieras guardar el proyecto y ejecuta:

```bash
git clone https://github.com/HFernandoCR/modelo-prediccopm-liga-mx.git
```

_**[AÑADIR AQUÍ]:** Captura de pantalla del proceso de clonación en la terminal_

**Paso 4:** Entra al directorio del proyecto:

```bash
cd modelo-prediccopm-liga-mx
```

_**[AÑADIR AQUÍ]:** Captura mostrando el cambio de directorio_

---

### Opción B: Descarga Directa (Sin Git)

Si no tienes Git instalado:

1. Ve al repositorio: https://github.com/HFernandoCR/modelo-prediccopm-liga-mx
2. Haz clic en el botón verde **"Code"**
3. Selecciona **"Download ZIP"**

_**[AÑADIR AQUÍ]:** Captura del botón "Download ZIP" en GitHub_

4. Extrae el archivo ZIP en tu carpeta deseada
5. Abre la terminal en esa carpeta

---

##  Paso 2: Crear Entorno Virtual

### ¿Por qué usar un entorno virtual?

Un entorno virtual es **FUNDAMENTAL** para:
-  Evitar conflictos con otras versiones de librerías en tu sistema
-  Mantener las dependencias del proyecto aisladas
-  Garantizar que el proyecto funcione correctamente
-  No contaminar tu instalación global de Python

---

### Crear el entorno virtual

**Paso 5:** Ejecuta el siguiente comando según tu sistema operativo:

#### Windows (PowerShell o CMD)

```powershell
python -m venv venv
```

_**[AÑADIR AQUÍ]:** Captura de la creación del entorno virtual en Windows_

#### Linux/Mac (Terminal)

```bash
python3 -m venv venv
```

_**[AÑADIR AQUÍ]:** Captura de la creación del entorno virtual en Linux/Mac_

**Nota:** Esto creará una carpeta llamada `venv` en tu proyecto. Verás algo como:

```
modelo-prediccopm-liga-mx/
├── venv/            Nueva carpeta creada
├── modelo_poisson/
├── main.py
└── ...
```

---

##  Paso 3: Activar el Entorno Virtual

**Paso 6:** Activa el entorno virtual:

#### Windows (PowerShell)

```powershell
.\venv\Scripts\activate
```

_**[AÑADIR AQUÍ]:** Captura de la activación del entorno en PowerShell_

#### Windows (CMD)

```cmd
.\venv\Scripts\activate.bat
```

#### Linux/Mac

```bash
source venv/bin/activate
```

_**[AÑADIR AQUÍ]:** Captura de la activación del entorno en Linux/Mac_

---

###  Verificar que el entorno está activado

Después de activar, deberías ver `(venv)` al inicio de tu línea de comandos:

**Windows:**
```
(venv) C:\Users\TuNombre\modelo-prediccopm-liga-mx>
```

**Linux/Mac:**
```
(venv) ~/modelo-prediccopm-liga-mx$
```

_**[AÑADIR AQUÍ]:** Captura mostrando el prompt con (venv) al inicio_

** Si no ves (venv):** El entorno no está activado. Repite el Paso 6.

---

##  Paso 4: Instalar Dependencias

Con el entorno virtual **ACTIVADO** (debe mostrar `(venv)`):

**Paso 7:** Instala todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

_**[AÑADIR AQUÍ]:** Captura del proceso de instalación de paquetes_

Verás una salida similar a:

```
Collecting pandas>=1.3.0
  Downloading pandas-2.1.3-cp311-cp311-win_amd64.whl (11.0 MB)
Collecting numpy>=1.21.0
  Downloading numpy-1.26.2-cp311-cp311-win_amd64.whl (15.5 MB)
...
Successfully installed pandas-2.1.3 numpy-1.26.2 streamlit-1.28.1 ...
```

**Este proceso puede tardar 2-5 minutos** dependiendo de tu conexión a internet.

---

##  Paso 5: Verificar Instalación

**Paso 8:** Verifica que todos los paquetes se instalaron correctamente:

```bash
pip list
```

_**[AÑADIR AQUÍ]:** Captura del comando `pip list` mostrando los paquetes instalados_

Deberías ver en la lista:
- `pandas`
- `numpy`
- `streamlit`
- `statsmodels`
- `plotly`
- `matplotlib`
- `seaborn`
- `scipy`

---

### Prueba rápida de funcionamiento

**Paso 9:** Ejecuta esta prueba para confirmar que los imports funcionan:

```bash
python -c "import streamlit, pandas, statsmodels; print(' Instalación exitosa')"
```

_**[AÑADIR AQUÍ]:** Captura del mensaje de éxito_

Si ves ` Instalación exitosa`, ¡todo está listo! 

---

##  Próximos Pasos

Ahora que tienes todo instalado, puedes:

1. **[Usar la Interfaz Web](2-Uso-Interfaz-Web)** - La forma más fácil de comenzar
2. **[Usar la Interfaz CLI](3-Uso-CLI)** - Ejecutar desde terminal
3. **[Ver Ejemplos](5-Ejemplos-y-Casos-de-Uso)** - Casos de uso prácticos

---

##  Desactivar el Entorno Virtual

Cuando termines de trabajar con el proyecto:

**Paso 10:** Desactiva el entorno virtual:

```bash
deactivate
```

_**[AÑADIR AQUÍ]:** Captura mostrando la desactivación (el prompt sin `(venv)`)_

Esto te regresa a tu entorno Python normal. El prefijo `(venv)` desaparecerá.

---

##  Resumen de Comandos

### Cada vez que trabajes en el proyecto:

```bash
# 1. Navega al directorio del proyecto
cd modelo-prediccopm-liga-mx

# 2. Activa el entorno virtual
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Trabaja en el proyecto
streamlit run app.py  # o python main.py

# 4. Al terminar, desactiva
deactivate
```

---

##  Problemas Comunes

### Error: "python no se reconoce como comando"

**Solución:** Python no está en el PATH del sistema
1. Reinstala Python marcando "Add Python to PATH"
2. O usa `py` en lugar de `python`

### Error: "Cannot activate virtual environment"

**Windows - Error de política de ejecución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error al instalar dependencias

**Solución:** Actualiza pip primero
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

##  Más Ayuda

Si tienes problemas:
- Consulta la página de **[FAQ y Troubleshooting](6-FAQ-y-Troubleshooting)**
- Crea un [Issue en GitHub](https://github.com/HFernandoCR/modelo-prediccopm-liga-mx/issues)

---

[️ Volver a Home](Home) | [️ Siguiente: Uso de Interfaz Web](2-Uso-Interfaz-Web)
