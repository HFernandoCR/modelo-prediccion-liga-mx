"""Visualización: heatmaps y gráficos para las predicciones."""

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALIZACION_DISPONIBLE = True
except ImportError:
    VISUALIZACION_DISPONIBLE = False
    print("matplotlib/seaborn no disponibles. Visualizaciones deshabilitadas.")

import numpy as np


def crear_heatmap_probabilidades(matriz, equipo_local, equipo_visitante,
                                  guardar=False, ruta='heatmap.png'):
    """Dibuja heatmap de la matriz de probabilidades; puede guardar archivo."""
    if not VISUALIZACION_DISPONIBLE:
        print("Visualización no disponible. Instala: pip install matplotlib seaborn")
        return
    
    plt.figure(figsize=(10, 8))
    
    # Crear heatmap
    sns.heatmap(
        matriz * 100,  # Convertir a porcentaje
        annot=True,
        fmt='.1f',
        cmap='YlOrRd',
        xticklabels=range(matriz.shape[1]),
        yticklabels=range(matriz.shape[0]),
        cbar_kws={'label': 'Probabilidad (%)'},
        linewidths=0.5,
        linecolor='gray'
    )
    
    plt.xlabel(f'Goles de {equipo_visitante} (visitante)', fontsize=12, fontweight='bold')
    plt.ylabel(f'Goles de {equipo_local} (local)', fontsize=12, fontweight='bold')
    plt.title(f'Matriz de Probabilidades: {equipo_local} vs {equipo_visitante}',
              fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if guardar:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"✓ Heatmap guardado en: {ruta}")
    else:
        plt.show()
    
    plt.close()


def graficar_rankings(ranking_ataque, ranking_defensa, guardar=False, ruta='rankings.png'):
    """Grafica rankings de ataque/defensa; opcionalmente guarda la imagen."""
    if not VISUALIZACION_DISPONIBLE:
        print("Visualización no disponible.")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico de ataque
    top_ataque = ranking_ataque.head(10)
    ax1.barh(top_ataque['Equipo'], top_ataque['Alpha'], color='steelblue')
    ax1.set_xlabel('Fuerza de Ataque (α)', fontweight='bold')
    ax1.set_title('Top 10 Equipos - Fuerza de Ataque', fontweight='bold', fontsize=14)
    ax1.axvline(x=1.0, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Promedio')
    ax1.legend()
    ax1.invert_yaxis()
    
    # Gráfico de defensa
    top_defensa = ranking_defensa.head(10)
    ax2.barh(top_defensa['Equipo'], top_defensa['Beta'], color='coral')
    ax2.set_xlabel('Fuerza de Defensa (β)', fontweight='bold')
    ax2.set_title('Top 10 Equipos - Mejor Defensa', fontweight='bold', fontsize=14)
    ax2.axvline(x=1.0, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Promedio')
    ax2.legend()
    ax2.invert_yaxis()
    
    plt.tight_layout()
    
    if guardar:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico de rankings guardado en: {ruta}")
    else:
        plt.show()
    
    plt.close()


def graficar_distribucion_goles(lambda_local, lambda_visitante, max_goles=6):
    """Grafica la distribución Poisson de goles para local y visitante."""
    if not VISUALIZACION_DISPONIBLE:
        return
    
    from scipy.stats import poisson
    
    goles = np.arange(0, max_goles + 1)
    prob_local = [poisson.pmf(k, lambda_local) for k in goles]
    prob_visitante = [poisson.pmf(k, lambda_visitante) for k in goles]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(goles))
    width = 0.35
    
    ax.bar(x - width/2, prob_local, width, label='Local', alpha=0.8, color='steelblue')
    ax.bar(x + width/2, prob_visitante, width, label='Visitante', alpha=0.8, color='coral')
    
    ax.set_xlabel('Número de Goles', fontweight='bold')
    ax.set_ylabel('Probabilidad', fontweight='bold')
    ax.set_title('Distribución de Probabilidad de Goles', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(goles)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    plt.close()