"""
Aplicación Web - Predictor Liga MX
===================================
Interfaz Streamlit para modelo de Poisson.

Autor: Fernando
Proyecto: TecNM - Simulación
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modelo_poisson import ModeloPoissonFutbol


# =====================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================================

st.set_page_config(
    page_title="Liga MX Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================================
# FUNCIONES HELPER
# =====================================================================

@st.cache_resource
def cargar_modelo_preentrenado():
    """
    Carga modelo pre-entrenado desde parametros_modelo.csv.
    Usa caché para no recargar en cada interacción.
    """
    try:
        modelo = ModeloPoissonFutbol()
        info = modelo.cargar_parametros('parametros_modelo.csv')
        return modelo, None
    except Exception as e:
        return None, str(e)


def entrenar_modelo_nuevo(uploaded_file):
    """
    Entrena modelo desde cero usando CSV subido por usuario.

    Parameters
    ----------
    uploaded_file : UploadedFile
        Archivo CSV de Streamlit

    Returns
    -------
    tuple
        (modelo, error_msg)
    """
    try:
        # Guardar archivo temporalmente usando el nombre original
        import os
        temp_path = os.path.join('/tmp' if os.name != 'nt' else os.getenv('TEMP', '.'), uploaded_file.name)

        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getvalue())

        # Crear y entrenar modelo
        modelo = ModeloPoissonFutbol()
        modelo.cargar_datos(temp_path)
        modelo.entrenar()

        return modelo, None

    except Exception as e:
        return None, str(e)


def crear_heatmap_interactivo(matriz, equipo_local, equipo_visitante):
    """
    Crea heatmap interactivo con Plotly.
    
    Parameters
    ----------
    matriz : numpy.ndarray
        Matriz de probabilidades (goles_local x goles_visitante)
    equipo_local : str
        Nombre del equipo local
    equipo_visitante : str
        Nombre del equipo visitante
    
    Returns
    -------
    plotly.graph_objects.Figure
        Figura interactiva de Plotly
    """
    # Convertir a porcentaje
    matriz_pct = matriz * 100
    
    # Encontrar marcador más probable
    max_prob_idx = np.unravel_index(np.argmax(matriz), matriz.shape)
    
    # Crear anotaciones personalizadas
    anotaciones = []
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            # En escala de verdes: texto blanco para verde oscuro, negro para verde claro
            color = 'white' if matriz_pct[i, j] > 8 else 'black'
            peso = 'bold' if (i, j) == max_prob_idx else 'normal'
            
            anotaciones.append(
                dict(
                    x=j, y=i,
                    text=f'{matriz_pct[i, j]:.1f}%',
                    showarrow=False,
                    font=dict(color=color, size=11, family='Arial', weight=peso)
                )
            )
    
    # Crear figura
    fig = go.Figure(data=go.Heatmap(
        z=matriz_pct,
        x=[str(i) for i in range(matriz.shape[1])],
        y=[str(i) for i in range(matriz.shape[0])],
        colorscale='Greens',  # Verde claro (baja prob) a verde oscuro (alta prob)
        text=[[f'{val:.1f}%' for val in row] for row in matriz_pct],
        texttemplate='%{text}',
        textfont={"size": 11},
        colorbar=dict(title="Probabilidad (%)", ticksuffix="%"),
        hovertemplate=(
            f'<b>{equipo_local}</b>: %{{y}} goles<br>' +
            f'<b>{equipo_visitante}</b>: %{{x}} goles<br>' +
            '<b>Probabilidad</b>: %{z:.2f}%<extra></extra>'
        )
    ))
    
    # Configurar layout
    fig.update_layout(
        title=dict(
            text=f'Matriz de Probabilidades: {equipo_local} vs {equipo_visitante}',
            font=dict(size=18, family='Arial', color='#1f77b4')
        ),
        xaxis_title=f'Goles de {equipo_visitante} (Visitante)',
        yaxis_title=f'Goles de {equipo_local} (Local)',
        xaxis=dict(side='bottom', tickmode='linear'),
        yaxis=dict(autorange='reversed', tickmode='linear'),
        height=500,
        font=dict(family='Arial', size=12)
    )
    
    return fig


def crear_grafico_barras(prob_local, prob_empate, prob_visit):
    """
    Crea gráfico de barras horizontal con probabilidades.
    
    Parameters
    ----------
    prob_local : float
        Probabilidad victoria local (0-1)
    prob_empate : float
        Probabilidad empate (0-1)
    prob_visit : float
        Probabilidad victoria visitante (0-1)
    
    Returns
    -------
    plotly.graph_objects.Figure
        Gráfico de barras interactivo
    """
    fig = go.Figure()
    
    # Datos
    categorias = ['Victoria Local', 'Empate', 'Victoria Visitante']
    probabilidades = [prob_local * 100, prob_empate * 100, prob_visit * 100]
    colores = ['#1f77b4', '#ff7f0e', '#d62728']  # Azul, Naranja, Rojo
    
    # Agregar barras
    fig.add_trace(go.Bar(
        y=categorias,
        x=probabilidades,
        orientation='h',
        marker=dict(color=colores),
        text=[f'{p:.1f}%' for p in probabilidades],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Arial', weight='bold'),
        hovertemplate='<b>%{y}</b><br>Probabilidad: %{x:.2f}%<extra></extra>'
    ))
    
    # Configurar layout
    fig.update_layout(
        title=dict(
            text='Probabilidades del Resultado',
            font=dict(size=16, family='Arial')
        ),
        xaxis_title='Probabilidad (%)',
        xaxis=dict(range=[0, 100], ticksuffix='%'),
        yaxis=dict(autorange='reversed'),
        height=300,
        showlegend=False,
        font=dict(family='Arial', size=12)
    )
    
    return fig


def crear_grafico_lambdas(lambda_local, lambda_visitante, equipo_local, equipo_visitante):
    """
    Crea gráfico comparativo de tasas esperadas (λ).
    
    Parameters
    ----------
    lambda_local : float
        Tasa esperada de goles del equipo local
    lambda_visitante : float
        Tasa esperada de goles del equipo visitante
    equipo_local : str
        Nombre del equipo local
    equipo_visitante : str
        Nombre del equipo visitante
    
    Returns
    -------
    plotly.graph_objects.Figure
        Gráfico comparativo
    """
    fig = go.Figure()
    
    equipos = [equipo_local, equipo_visitante]
    lambdas = [lambda_local, lambda_visitante]
    colores = ['#1f77b4', '#d62728']
    
    fig.add_trace(go.Bar(
        x=equipos,
        y=lambdas,
        marker=dict(color=colores),
        text=[f'{l:.2f}' for l in lambdas],
        textposition='outside',
        textfont=dict(size=14, family='Arial', weight='bold'),
        hovertemplate='<b>%{x}</b><br>λ = %{y:.3f} goles esperados<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Goles Esperados (λ)',
            font=dict(size=16, family='Arial')
        ),
        yaxis_title='Goles Esperados',
        height=300,
        showlegend=False,
        font=dict(family='Arial', size=12)
    )
    
    return fig


# =====================================================================
# INTERFAZ PRINCIPAL
# =====================================================================

def main():
    """Función principal de la aplicación."""
    
    # ===== SIDEBAR =====
    st.sidebar.title("Liga MX Predictor")
    st.sidebar.markdown("---")
    
    # Modo de operación
    st.sidebar.subheader("Configuración")
    modo = st.sidebar.radio(
        "Modo de operación:",
        options=["Usar modelo pre-entrenado", "Entrenar nuevo modelo"],
        index=0
    )
    
    # Inicializar modelo según modo
    modelo = None
    
    if modo == "Usar modelo pre-entrenado":
        # Cargar modelo pre-entrenado
        with st.spinner("Cargando modelo pre-entrenado..."):
            modelo, error = cargar_modelo_preentrenado()
        
        if error:
            st.sidebar.error(f"Error al cargar modelo: {error}")
            st.stop()
        else:
            st.sidebar.success("Modelo pre-entrenado cargado")
    
    else:  # Entrenar nuevo modelo
        st.sidebar.info("Sube un archivo CSV con datos históricos")
        
        # Botón para descargar plantilla
        st.sidebar.markdown("##### Plantilla CSV")
        st.sidebar.markdown("Descarga la plantilla para saber cómo estructurar tus datos:")
        
        # Leer plantilla
        plantilla_csv = """Date,HomeTeam,AwayTeam,FTHG,FTAG
        2023-07-15,Club America,Cruz Azul,2,1
        2023-07-16,Tigres UANL,Monterrey,1,1
        2023-07-17,Guadalajara Chivas,Atlas,3,0
        2023-07-18,Pachuca,Club Leon,2,2
        2023-07-19,Toluca,Santos Laguna,1,0
        2023-07-20,UNAM Pumas,Queretaro,2,1
        2023-07-21,Puebla,Necaxa,0,0
        2023-07-22,Mazatlan FC,Club Tijuana,1,2
        2023-07-23,Atl. San Luis,Juarez,2,0
        2023-07-24,Monarcas,Veracruz,3,1"""
        
        st.sidebar.download_button(
            label="Descargar Plantilla CSV",
            data=plantilla_csv,
            file_name="plantilla_liga_mx.csv",
            mime="text/csv",
            help="CSV de ejemplo con la estructura correcta"
        )
        
        st.sidebar.markdown("---")
        
        uploaded_file = st.sidebar.file_uploader(
            "Selecciona archivo CSV:",
            type=['csv'],
            help="El CSV debe tener columnas: Date, HomeTeam, AwayTeam, FTHG, FTAG"
        )
        
        if uploaded_file is not None:
            if st.sidebar.button("Entrenar Modelo", type="primary"):
                with st.spinner("Entrenando modelo... Esto puede tomar 10-15 segundos..."):
                    modelo, error = entrenar_modelo_nuevo(uploaded_file)
                
                if error:
                    st.sidebar.error(f"Error: {error}")
                else:
                    st.sidebar.success("Modelo entrenado exitosamente")
                    # Guardar en session state
                    st.session_state['modelo_custom'] = modelo
        
        # Recuperar de session state si existe
        if 'modelo_custom' in st.session_state:
            modelo = st.session_state['modelo_custom']
    
    # Si no hay modelo, detener
    if modelo is None:
        st.info("Configura el modelo en el panel lateral para comenzar")
        st.stop()
    
    # ===== SELECTORES DE EQUIPOS =====
    st.sidebar.markdown("---")
    st.sidebar.subheader("Selección de Equipos")
    
    equipos_disponibles = sorted(modelo.equipos)
    
    equipo_local = st.sidebar.selectbox(
        "Equipo Local:",
        options=equipos_disponibles,
        index=equipos_disponibles.index('Club America') if 'Club America' in equipos_disponibles else 0
    )
    
    equipo_visitante = st.sidebar.selectbox(
        "Equipo Visitante:",
        options=equipos_disponibles,
        index=equipos_disponibles.index('Cruz Azul') if 'Cruz Azul' in equipos_disponibles else 1
    )
    
    # Validación: evitar mismo equipo
    if equipo_local == equipo_visitante:
        st.sidebar.warning("Selecciona equipos diferentes")
        st.stop()
    
    # Botón de predicción
    st.sidebar.markdown("---")
    predecir_btn = st.sidebar.button("Predecir Resultado", type="primary", use_container_width=True)
    
    # ===== ÁREA PRINCIPAL =====
    st.title("Predictor de Resultados - Liga MX")
    st.markdown("**Modelo de Regresión de Poisson** | Basado en Dixon & Coles (1997)")
    st.markdown("---")
    
    # Crear tabs
    tab1, tab2, tab3 = st.tabs(["Predicción", "Rankings", "Info del Modelo"])
    
    # ===== TAB 1: PREDICCIÓN =====
    with tab1:
        if predecir_btn:
            with st.spinner("Calculando predicción..."):
                prediccion = modelo.predecir(equipo_local, equipo_visitante, mostrar=False)
            
            # Métricas principales
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label=f" {equipo_local}",
                    value=f"λ = {prediccion['lambda_local']:.2f}",
                    help="Goles esperados del equipo local"
                )
            
            with col2:
                marcador = prediccion['marcador_mas_probable']
                prob_marcador = prediccion['prob_marcador_mas_probable']
                st.metric(
                    label=" Marcador Más Probable",
                    value=f"{marcador} ({prob_marcador*100:.1f}%)",
                    help="Resultado con mayor probabilidad"
                )
            
            with col3:
                st.metric(
                    label=f" {equipo_visitante}",
                    value=f"λ = {prediccion['lambda_visitante']:.2f}",
                    help="Goles esperados del equipo visitante"
                )
            
            st.markdown("---")
            
            # Gráfico de barras (probabilidades)
            st.subheader(" Probabilidades del Resultado")
            fig_barras = crear_grafico_barras(
                prediccion['prob_victoria_local'],
                prediccion['prob_empate'],
                prediccion['prob_victoria_visitante']
            )
            st.plotly_chart(fig_barras, use_container_width=True)
            
            # Heatmap
            st.subheader(" Matriz de Probabilidades (Todos los Marcadores)")
            fig_heatmap = crear_heatmap_interactivo(
                prediccion['matriz_probabilidades'],
                equipo_local,
                equipo_visitante
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Información adicional
            with st.expander(" Ver análisis detallado"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write("**Parámetros del Partido:**")
                    st.write(f"- α (ataque local): {modelo.alpha[equipo_local]:.3f}")
                    st.write(f"- β (defensa visitante): {modelo.beta[equipo_visitante]:.3f}")
                    st.write(f"- γ (ventaja local): {modelo.gamma:.3f}")
                
                with col_b:
                    st.write("**Interpretación:**")
                    if prediccion['lambda_local'] > prediccion['lambda_visitante']:
                        st.success(f" {equipo_local} es favorito")
                    elif prediccion['lambda_local'] < prediccion['lambda_visitante']:
                        st.error(f" {equipo_visitante} es favorito")
                    else:
                        st.info(" Partido equilibrado")
        
        else:
            st.info(" Selecciona los equipos y presiona **'Predecir Resultado'**")
    
    # ===== TAB 2: RANKINGS =====
    with tab2:
        st.subheader(" Rankings de la Liga MX")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("###  Ranking de Ataque (α)")
            ranking_ataque = modelo.obtener_ranking_ataque()
            st.dataframe(
                ranking_ataque[['Ranking', 'Equipo', 'Alpha']].rename(columns={'Alpha': 'Fuerza Ataque'}),
                use_container_width=True,
                height=600
            )
        
        with col2:
            st.markdown("###  Ranking de Defensa (β)")
            ranking_defensa = modelo.obtener_ranking_defensa()
            st.dataframe(
                ranking_defensa[['Ranking', 'Equipo', 'Beta']].rename(columns={'Beta': 'Fuerza Defensa'}),
                use_container_width=True,
                height=600
            )
        
        st.markdown("---")
        st.info(" **Nota:** En defensa, valores menores = mejor defensa")
    
    # ===== TAB 3: INFO DEL MODELO =====
    with tab3:
        st.subheader(" Información del Modelo")
        
        # Parámetros del modelo
        st.markdown("###  Parámetros del Modelo")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Equipos", len(modelo.equipos))
        
        with col2:
            if hasattr(modelo, 'datos_originales') and modelo.datos_originales is not None:
                st.metric("Partidos", len(modelo.datos_originales))
            else:
                st.metric("Partidos", "N/A")
        
        with col3:
            st.metric("γ (Ventaja Local)", f"{modelo.gamma:.3f}")
        
        with col4:
            ventaja_pct = (modelo.gamma - 1) * 100
            st.metric("Ventaja Local %", f"+{ventaja_pct:.1f}%")
        
        if hasattr(modelo, 'modelo_entrenado') and modelo.modelo_entrenado is not True and modelo.modelo_entrenado is not None:
            col5, col6 = st.columns(2)
            with col5:
                st.metric("Log-Likelihood", f"{modelo.modelo_entrenado.llf:.2f}")
            with col6:
                st.metric("AIC", f"{modelo.modelo_entrenado.aic:.2f}")
        
        # Explicación del modelo
        st.markdown("---")
        st.markdown("###  ¿Cómo funciona el Modelo de Poisson?")
        
        st.write("""
        El modelo utiliza **Regresión de Poisson** para predecir los goles en un partido de fútbol.
        
        **Fórmula principal:**
        """)
        
        st.latex(r"\lambda_{ij} = \alpha_i \times \beta_j \times \gamma")
        
        st.write("""
        Donde:
        - **λ (lambda)**: Goles esperados
        - **α (alpha)**: Fuerza de ataque del equipo local
        - **β (beta)**: Fuerza de defensa del equipo visitante
        - **γ (gamma)**: Ventaja de jugar como local
        
        **Proceso:**
        1. Se calculan λ para ambos equipos
        2. Se usa la distribución de Poisson para calcular P(goles)
        3. Se genera una matriz con todas las probabilidades de marcadores
        """)
        
        # Referencias
        st.markdown("---")
        st.markdown("###  Referencias Académicas")
        st.write("""
        - **Dixon, M. J., & Coles, S. G. (1997).** "Modelling association football scores 
          and inefficiencies in the football betting market". *Applied Statistics*, 46(2), 265-280.
        
        - **Sánchez Gálvez et al. (2022).** "Model for Prediction of the Result of a Soccer Match 
          Based on the Number of Goals Scored by a Single Team". *Computación y Sistemas*, 26(1), 295-302.
        """)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: gray;'>
            <p>Desarrollado por Fernando | TecNM - Campus Oaxaca</p>
            <p>Proyecto de Simulación | 2024</p>
        </div>
        """, unsafe_allow_html=True)


# =====================================================================
# EJECUTAR APLICACIÓN
# =====================================================================

if __name__ == "__main__":
    main()