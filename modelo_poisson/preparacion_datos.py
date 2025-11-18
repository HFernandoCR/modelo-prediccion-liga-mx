"""Funciones para cargar y preparar datos para el GLM Poisson."""

import pandas as pd
from .utils import sanitizar_nombre, imprimir_titulo


def cargar_datos_historicos(ruta_csv):
    """Lee CSV, valida columnas y devuelve DataFrame y lista de equipos."""
    # Cargar CSV
    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_csv}")
    
    # Validar columnas requeridas
    columnas_requeridas = ['Temporada', 'Fecha', 'Equipo_Local', 
                           'Equipo_Visitante', 'Goles_Local', 'Goles_Visitante']
    
    columnas_faltantes = set(columnas_requeridas) - set(df.columns)
    if columnas_faltantes:
        raise ValueError(f"Faltan columnas requeridas: {columnas_faltantes}")
    
    # Obtener lista única de equipos
    equipos_local = set(df['Equipo_Local'].unique())
    equipos_visitante = set(df['Equipo_Visitante'].unique())
    equipos = sorted(list(equipos_local | equipos_visitante))
    
    # Mostrar información
    imprimir_titulo("DATOS CARGADOS")
    print(f"✓ Total de partidos: {len(df)}")
    print(f"✓ Temporadas: {df['Temporada'].nunique()}")
    print(f"✓ Número de equipos: {len(equipos)}")
    print(f"\nEquipos encontrados:")
    for i, equipo in enumerate(equipos, 1):
        print(f"  {i:2d}. {equipo}")
    
    return df, equipos


def crear_variables_dummy(df, equipos):
    """Agrega variables dummy para ataque/defensa por equipo."""
    df_con_dummies = df.copy()
    
    print("\nCreando variables dummy...")
    
    # Variables para cada equipo
    for equipo in equipos:
        nombre_var = sanitizar_nombre(equipo)
        
        # Variable de ataque: 1 si el equipo está jugando (local o visitante)
        df_con_dummies[f'ataque_{nombre_var}'] = (
            (df['Equipo_Local'] == equipo) | 
            (df['Equipo_Visitante'] == equipo)
        ).astype(int)
        
        # Variable de defensa: 1 si el equipo está siendo atacado
        df_con_dummies[f'defensa_{nombre_var}'] = (
            (df['Equipo_Local'] == equipo) | 
            (df['Equipo_Visitante'] == equipo)
        ).astype(int)
    
    print(f"✓ {len(equipos) * 2} variables dummy creadas")
    
    return df_con_dummies


def preparar_datos_modelo(df, equipos):
    """Construye dataset combinado (observaciones local+visitante) listo para GLM."""
    imprimir_titulo("PREPARANDO DATOS PARA ENTRENAMIENTO")
    
    # ==========================================
    # PARTE 1: DATOS PARA GOLES DEL LOCAL
    # ==========================================
    print("\n[1/3] Preparando datos de goles del LOCAL...")
    
    datos_local = pd.DataFrame()
    datos_local['goles'] = df['Goles_Local'].values
    
    # Variables dummy de ATAQUE (equipo local ataca)
    for equipo in equipos:
        nombre_var = sanitizar_nombre(equipo)
        datos_local[f'ataque_{nombre_var}'] = (
            df['Equipo_Local'] == equipo
        ).astype(int).values
    
    # Variables dummy de DEFENSA (equipo visitante defiende)
    for equipo in equipos:
        nombre_var = sanitizar_nombre(equipo)
        datos_local[f'defensa_{nombre_var}'] = (
            df['Equipo_Visitante'] == equipo
        ).astype(int).values
    
    # Variable de ventaja de local
    datos_local['home'] = 1
    
    print(f"  ✓ {len(datos_local)} observaciones del LOCAL")
    
    # ==========================================
    # PARTE 2: DATOS PARA GOLES DEL VISITANTE
    # ==========================================
    print("\n[2/3] Preparando datos de goles del VISITANTE...")
    
    datos_visitante = pd.DataFrame()
    datos_visitante['goles'] = df['Goles_Visitante'].values
    
    # Variables dummy de ATAQUE (equipo visitante ataca)
    for equipo in equipos:
        nombre_var = sanitizar_nombre(equipo)
        datos_visitante[f'ataque_{nombre_var}'] = (
            df['Equipo_Visitante'] == equipo
        ).astype(int).values
    
    # Variables dummy de DEFENSA (equipo local defiende)
    for equipo in equipos:
        nombre_var = sanitizar_nombre(equipo)
        datos_visitante[f'defensa_{nombre_var}'] = (
            df['Equipo_Local'] == equipo
        ).astype(int).values
    
    # Variable de ventaja de local (0 para visitante)
    datos_visitante['home'] = 0
    
    print(f"  ✓ {len(datos_visitante)} observaciones del VISITANTE")
    
    # ==========================================
    # PARTE 3: COMBINAR DATASETS
    # ==========================================
    print("\n[3/3] Combinando datasets...")
    
    datos_completos = pd.concat([datos_local, datos_visitante], 
                                 ignore_index=True)
    
    print(f"  ✓ Dataset final: {len(datos_completos)} observaciones")
    print(f"  ✓ Variables: {datos_completos.shape[1]} columnas")
    
    return datos_completos


def construir_formula_glm(equipos):
    """Genera la fórmula string para ajustar el GLM (sin intercepto)."""
    variables_ataque = [f'ataque_{sanitizar_nombre(eq)}' for eq in equipos]
    variables_defensa = [f'defensa_{sanitizar_nombre(eq)}' for eq in equipos]
    
    formula = ('goles ~ ' + 
               ' + '.join(variables_ataque + variables_defensa) + 
               ' + home - 1')
    
    return formula


def extraer_parametros_modelo(modelo_entrenado, equipos):
    """Extrae alpha, beta y gamma (expo de coeficientes del modelo)."""
    import numpy as np
    
    params = modelo_entrenado.params
    
    # Extraer alphas (ataque)
    alpha = {}
    for equipo in equipos:
        nombre_var = sanitizar_nombre(equipo)
        coef_log = params.get(f'ataque_{nombre_var}', 0)
        alpha[equipo] = np.exp(coef_log)
    
    # Extraer betas (defensa)
    beta = {}
    for equipo in equipos:
        nombre_var = sanitizar_nombre(equipo)
        coef_log = params.get(f'defensa_{nombre_var}', 0)
        beta[equipo] = np.exp(coef_log)
    
    # Extraer gamma (ventaja de local)
    gamma = np.exp(params['home'])
    
    return alpha, beta, gamma