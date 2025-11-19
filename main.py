"""
Script principal - Modelo de Predicción para Liga MX
"""

from modelo_poisson import ModeloPoissonFutbol


def main():
    """
    Función principal que ejecuta todo el flujo del modelo.
    """
    print("MODELO DE PREDICCIÓN PARA LIGA MX")
    
    # ==========================================
    # PASO 1: CREAR INSTANCIA Y CARGAR DATOS
    # ==========================================
    print("PASO 1: Inicialización\n" + "-" * 70)
    modelo = ModeloPoissonFutbol()
    
    try:
        modelo.cargar_datos('liga_mx_data_limpia.csv')
    except FileNotFoundError:
        print("\nError: Archivo 'liga_mx_data_limpia.csv' no encontrado")
        print("   Asegúrate de que el archivo esté en el directorio actual\n")
        return
    
    # ==========================================
    # PASO 2: ENTRENAR MODELO
    # ==========================================
    print("\n\nPASO 2: Entrenamiento\n" + "-" * 70)
    modelo.entrenar()
    
    # ==========================================
    # PASO 3: MOSTRAR RESUMEN
    # ==========================================
    print("\n\nPASO 3: Resumen del Modelo\n" + "-" * 70)
    modelo.resumen_modelo()
    
    # ==========================================
    # PASO 4: RANKINGS
    # ==========================================
    print("\n\nPASO 4: Rankings Completos\n" + "-" * 70)
    
    print("\n RANKING DE ATAQUE (Top 10):")
    print("=" * 70)
    ranking_ataque = modelo.obtener_ranking_ataque(top_n=10)
    print(ranking_ataque[['Ranking', 'Equipo', 'Alpha']].to_string(index=False))
    
    print("\n\n RANKING DE DEFENSA (Top 10):")
    print("=" * 70)
    print("Nota: Valores menores = mejor defensa\n")
    ranking_defensa = modelo.obtener_ranking_defensa(top_n=10)
    print(ranking_defensa[['Ranking', 'Equipo', 'Beta']].to_string(index=False))
    
    # ==========================================
    # PASO 5: PREDICCIONES DE EJEMPLO
    # ==========================================
    print("\n\nPASO 5: Predicciones de Ejemplo\n" + "-" * 70)
    print("\n EJEMPLO 1: Clásico Capitalino")
    modelo.predecir('Club America', 'Cruz Azul')
    
    print("\n EJEMPLO 2: Clásico Regiomontano")
    modelo.predecir('Monterrey', 'Tigres UANL')
    
    print("\n EJEMPLO 3: Clásico Nacional")
    modelo.predecir('Guadalajara Chivas', 'Club America')
    
    # ==========================================
    # PASO 6: ANÁLISIS DE EQUIPO ESPECÍFICO
    # ==========================================
    print("\n\nPASO 6: Análisis de Equipo Específico\n" + "-" * 70)
    print("\n Análisis de Club América:\n")
    
    params_america = modelo.obtener_parametros_equipo('Club America')
    print(f"Equipo: {params_america['equipo']}")
    print(f"  • Alpha (Ataque): {params_america['alpha']:.3f}")
    print(f"    {params_america['interpretacion_ataque']}")
    print(f"  • Beta (Defensa): {params_america['beta']:.3f}")
    print(f"    {params_america['interpretacion_defensa']}")
    
    # ==========================================
    # PASO 7: COMPARACIÓN DE EQUIPOS
    # ==========================================
    print("\n\nPASO 7: Comparación de Equipos\n" + "-" * 70)
    print("\n Comparación de equipos grandes:\n")
    
    equipos_grandes = ['Club America', 'Guadalajara Chivas', 
                       'Cruz Azul', 'UNAM Pumas']
    comparacion = modelo.comparar_equipos(equipos_grandes)
    print(comparacion.to_string(index=False))
    
    # ==========================================
    # PASO 8: SIMULACIÓN DE JORNADA
    # ==========================================
    print("\n\nPASO 8: Simulación de Jornada Completa\n" + "-" * 70)
    
    partidos_jornada = [
        ('Club America', 'Guadalajara Chivas'),
        ('Monterrey', 'Tigres UANL'),
        ('Cruz Azul', 'UNAM Pumas'),
        ('Santos Laguna', 'Pachuca'),
        ('Toluca', 'Atlas')
    ]
    
    print("\n Predicciones de la Jornada:\n")
    jornada_df = modelo.simular_jornada(partidos_jornada, mostrar=True)
    
    # ==========================================
    # PASO 9: EXPORTAR RESULTADOS
    # ==========================================
    print("\n\nPASO 9: Exportar Resultados\n" + "-" * 70)
    print()
    
    # Exportar rankings COMPLETOS (todos los equipos, no solo top 10)
    ranking_ataque_completo = modelo.obtener_ranking_ataque(top_n=None)
    ranking_ataque_completo.to_csv('ranking_ataque.csv', index=False)
    print("✓ Ranking de ataque exportado: ranking_ataque.csv (21 equipos)")
    
    ranking_defensa_completo = modelo.obtener_ranking_defensa(top_n=None)
    ranking_defensa_completo.to_csv('ranking_defensa.csv', index=False)
    print("✓ Ranking de defensa exportado: ranking_defensa.csv (21 equipos)")
    
    # Exportar parámetros
    modelo.exportar_parametros('parametros_modelo.csv')
    
    # Exportar predicciones de jornada
    jornada_df.to_csv('predicciones_jornada.csv', index=False)
    print("✓ Predicciones de jornada exportadas: predicciones_jornada.csv")
    
    # ==========================================
    # FINALIZACIÓN
    # ==========================================
    print("\n\n" + "=" * 70)
    print(" EJECUCIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    
    print("\n Archivos generados:")
    print("  • ranking_ataque.csv")
    print("  • ranking_defensa.csv")
    print("  • parametros_modelo.csv")
    print("  • predicciones_jornada.csv")
    
    print("\n Próximos pasos:")
    print("  • Revisar los archivos CSV generados")
    print("  • Probar predicciones con otros equipos")
    print("  • Integrar con interfaz Streamlit (Tarea 3.3)")
    
    
    return modelo


if __name__ == "__main__":
    modelo_entrenado = main()