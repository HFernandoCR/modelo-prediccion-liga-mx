"""Funciones de predicción (modelo de Poisson)."""

import numpy as np
from scipy.stats import poisson
from .utils import validar_equipo, formatear_probabilidad, imprimir_titulo


def calcular_goles_esperados(equipo_local, equipo_visitante, alpha, beta, gamma):
    """Calcula λ para local y visitante."""
    lambda_local = alpha[equipo_local] * beta[equipo_visitante] * gamma
    lambda_visitante = alpha[equipo_visitante] * beta[equipo_local]
    
    return lambda_local, lambda_visitante


def generar_matriz_probabilidades(lambda_local, lambda_visitante, max_goles=5):
    """Matriz P(i,j)=P_local(i)*P_visitante(j)."""
    matriz = np.zeros((max_goles + 1, max_goles + 1))
    
    for i in range(max_goles + 1):
        for j in range(max_goles + 1):
            # P(local = i)
            prob_local = poisson.pmf(i, lambda_local)
            # P(visitante = j)
            prob_visitante = poisson.pmf(j, lambda_visitante)
            # P(marcador i-j) (independencia)
            matriz[i, j] = prob_local * prob_visitante
    
    return matriz


def calcular_probabilidades_resultado(matriz):
    """Devuelve P(victoria local, empate, victoria visitante)."""
    # Victoria local: triángulo INFERIOR (i > j)
    # triángulo inferior (i>j)
    prob_victoria_local = np.sum(np.tril(matriz, k=-1))
    
    # Empate: diagonal
    prob_empate = np.sum(np.diag(matriz))
    
    # triángulo superior (j>i)
    prob_victoria_visitante = np.sum(np.triu(matriz, k=1))
    
    return prob_victoria_local, prob_empate, prob_victoria_visitante


def encontrar_marcador_mas_probable(matriz):
    """Marcador más probable, su probabilidad e índices."""
    indice_max = np.unravel_index(matriz.argmax(), matriz.shape)
    marcador = f"{indice_max[0]}-{indice_max[1]}"
    probabilidad = matriz[indice_max]
    
    return marcador, probabilidad, indice_max


def calcular_over_under(matriz, limite=2.5):
    """Probabilidades Over/Under para total de goles."""
    prob_over = 0
    prob_under = 0
    
    filas, cols = matriz.shape
    for i in range(filas):
        for j in range(cols):
            goles_totales = i + j
            if goles_totales > limite:
                prob_over += matriz[i, j]
            else:
                prob_under += matriz[i, j]
    
    return prob_over, prob_under


def predecir_partido_completo(equipo_local, equipo_visitante, alpha, beta, 
                               gamma, equipos, max_goles=5):
    """Predicción completa: λ, matriz, probabilidades y métricas."""
    # validar equipos
    validar_equipo(equipo_local, equipos)
    validar_equipo(equipo_visitante, equipos)
    
    # calcular λ
    lambda_local, lambda_visitante = calcular_goles_esperados(
        equipo_local, equipo_visitante, alpha, beta, gamma
    )
    
    # generar matriz
    matriz = generar_matriz_probabilidades(
        lambda_local, lambda_visitante, max_goles
    )
    
    # probabilidades de resultado
    prob_local, prob_empate, prob_visitante = calcular_probabilidades_resultado(matriz)
    
    # marcador más probable
    marcador, prob_marcador, indices = encontrar_marcador_mas_probable(matriz)
    
    # over/under
    prob_over, prob_under = calcular_over_under(matriz, limite=2.5)
    
    return {
        'equipo_local': equipo_local,
        'equipo_visitante': equipo_visitante,
        'lambda_local': lambda_local,
        'lambda_visitante': lambda_visitante,
        'matriz_probabilidades': matriz,
        'prob_victoria_local': prob_local,
        'prob_empate': prob_empate,
        'prob_victoria_visitante': prob_visitante,
        'marcador_mas_probable': marcador,
        'prob_marcador_mas_probable': prob_marcador,
        'indices_marcador': indices,
        'prob_over_2_5': prob_over,
        'prob_under_2_5': prob_under
    }


def mostrar_prediccion_formato(prediccion):
    """Imprime la predicción en consola."""
    imprimir_titulo(f"PREDICCIÓN: {prediccion['equipo_local']} vs {prediccion['equipo_visitante']}")
    
    print(f"\n GOLES ESPERADOS:")
    print(f"  • {prediccion['equipo_local']} (local): "
          f"λ = {prediccion['lambda_local']:.3f} goles")
    print(f"  • {prediccion['equipo_visitante']} (visitante): "
          f"λ = {prediccion['lambda_visitante']:.3f} goles")
    
    print(f"\n PROBABILIDADES DE RESULTADO:")
    print(f"  • Victoria {prediccion['equipo_local']}: "
          f"{formatear_probabilidad(prediccion['prob_victoria_local'])}")
    print(f"  • Empate: "
          f"{formatear_probabilidad(prediccion['prob_empate'])}")
    print(f"  • Victoria {prediccion['equipo_visitante']}: "
          f"{formatear_probabilidad(prediccion['prob_victoria_visitante'])}")
    
    print(f"\n MARCADOR MÁS PROBABLE:")
    print(f"  • {prediccion['marcador_mas_probable']} "
          f"({formatear_probabilidad(prediccion['prob_marcador_mas_probable'])})")
    
    print(f"\n OVER/UNDER 2.5 GOLES:")
    print(f"  • Over 2.5: {formatear_probabilidad(prediccion['prob_over_2_5'])}")
    print(f"  • Under 2.5: {formatear_probabilidad(prediccion['prob_under_2_5'])}")
    
    print(f"\n MATRIZ DE PROBABILIDADES (%):")
    print(f"  Filas = Goles de {prediccion['equipo_local']} (local)")
    print(f"  Columnas = Goles de {prediccion['equipo_visitante']} (visitante)\n")
    
    mostrar_matriz_formateada(prediccion['matriz_probabilidades'])
    
    print("=" * 70 + "\n")


def mostrar_matriz_formateada(matriz):
    """Imprime matriz de probabilidades en porcentaje."""
    filas, cols = matriz.shape
    matriz_pct = matriz * 100  # Convertir a porcentaje
    
    # Encabezado
    print("     ", end="")
    for j in range(cols):
        print(f"  {j}  ", end="")
    print()
    print("    " + "-" * (6 * cols))
    
    # Filas
    for i in range(filas):
        print(f" {i} | ", end="")
        for j in range(cols):
            print(f"{matriz_pct[i,j]:4.1f} ", end="")
        print()


def simular_partido_montecarlo(lambda_local, lambda_visitante, n_simulaciones=1000):
    """Simula partidos por Monte Carlo y devuelve conteos y porcentajes."""
    np.random.seed(42)  # Para reproducibilidad
    
    goles_local = np.random.poisson(lambda_local, n_simulaciones)
    goles_visitante = np.random.poisson(lambda_visitante, n_simulaciones)
    
    victorias_local = np.sum(goles_local > goles_visitante)
    empates = np.sum(goles_local == goles_visitante)
    victorias_visitante = np.sum(goles_local < goles_visitante)
    
    return {
        'n_simulaciones': n_simulaciones,
        'victorias_local': victorias_local,
        'empates': empates,
        'victorias_visitante': victorias_visitante,
        'pct_victorias_local': victorias_local / n_simulaciones,
        'pct_empates': empates / n_simulaciones,
        'pct_victorias_visitante': victorias_visitante / n_simulaciones
    }