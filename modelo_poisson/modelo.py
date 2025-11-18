"""Clase principal del modelo de Poisson (flujo principal)."""

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings('ignore')

from . import preparacion_datos as prep
from . import predicciones as pred
from .utils import imprimir_titulo, interpretar_parametro


class ModeloPoissonFutbol:
    """Modelo Poisson: carga datos, entrena y genera predicciones."""
    
    def __init__(self):
        """Inicializa el modelo."""
        self.modelo_entrenado = None
        self.equipos = None
        self.alpha = None
        self.beta = None
        self.gamma = None
        self.datos_originales = None
        self._datos_entrenamiento = None
    
    def cargar_datos(self, ruta_csv):
        """Carga datos históricos desde CSV y devuelve DataFrame."""
        self.datos_originales, self.equipos = prep.cargar_datos_historicos(ruta_csv)
        return self.datos_originales
    
    def entrenar(self):
        """Prepara datos, construye y ajusta el GLM Poisson."""
        if self.datos_originales is None:
            raise ValueError("Primero debes cargar datos con .cargar_datos()")
        
        # Preparar datos
        self._datos_entrenamiento = prep.preparar_datos_modelo(
            self.datos_originales, self.equipos
        )
        
        # Construir fórmula
        formula = prep.construir_formula_glm(self.equipos)
        
        # Entrenar modelo
        imprimir_titulo("ENTRENANDO MODELO GLM")
        print(f"\n✓ Familia: Poisson")
        print(f"✓ Enlace: Logarítmico")
        print(f"✓ Variables: {len(self.equipos) * 2 + 1}")
        print(f"\nOptimizando con Maximum Likelihood...")
        
        self.modelo_entrenado = smf.glm(
            formula=formula,
            data=self._datos_entrenamiento,
            family=sm.families.Poisson()
        ).fit()
        
        print("✓ Convergencia exitosa")
        print(f"✓ Log-Likelihood: {self.modelo_entrenado.llf:.2f}")
        print(f"✓ AIC: {self.modelo_entrenado.aic:.2f}")
        
        # Extraer parámetros
        print("\nExtrayendo parámetros...")
        self.alpha, self.beta, self.gamma = prep.extraer_parametros_modelo(
            self.modelo_entrenado, self.equipos
        )
        
        print(f"✓ Ventaja de local (γ): {self.gamma:.3f}")
        print(f"  → Equipos locales anotan {(self.gamma-1)*100:.1f}% más goles")
        
        print("\n" + "✓" * 35)
        print("MODELO ENTRENADO EXITOSAMENTE")
        print("✓" * 35 + "\n")
        
        return self.modelo_entrenado
    
    def predecir(self, equipo_local, equipo_visitante, max_goles=5, mostrar=True):
        """Predicción de partido; devuelve un diccionario con resultados."""
        if self.modelo_entrenado is None:
            raise ValueError("Primero debes entrenar el modelo con .entrenar()")
        
        prediccion = pred.predecir_partido_completo(
            equipo_local, equipo_visitante,
            self.alpha, self.beta, self.gamma,
            self.equipos, max_goles
        )
        
        if mostrar:
            pred.mostrar_prediccion_formato(prediccion)
        
        return prediccion
    
    def obtener_ranking_ataque(self, top_n=None):
        """Devuelve DataFrame con ranking de ataque."""
        if self.alpha is None:
            raise ValueError("Primero debes entrenar el modelo")
        
        ranking = pd.DataFrame([
            {
                'Equipo': equipo,
                'Alpha': valor,
                'Interpretacion': interpretar_parametro(valor, 'alpha')
            }
            for equipo, valor in self.alpha.items()
        ]).sort_values('Alpha', ascending=False)
        
        ranking['Ranking'] = range(1, len(ranking) + 1)
        ranking = ranking[['Ranking', 'Equipo', 'Alpha', 'Interpretacion']]
        
        if top_n:
            ranking = ranking.head(top_n)
        
        return ranking.reset_index(drop=True)
    
    def obtener_ranking_defensa(self, top_n=None):
        """Devuelve DataFrame con ranking de defensa (menor = mejor)."""
        if self.beta is None:
            raise ValueError("Primero debes entrenar el modelo")
        
        ranking = pd.DataFrame([
            {
                'Equipo': equipo,
                'Beta': valor,
                'Interpretacion': interpretar_parametro(valor, 'beta')
            }
            for equipo, valor in self.beta.items()
        ]).sort_values('Beta', ascending=True)  # Menor = mejor
        
        ranking['Ranking'] = range(1, len(ranking) + 1)
        ranking = ranking[['Ranking', 'Equipo', 'Beta', 'Interpretacion']]
        
        if top_n:
            ranking = ranking.head(top_n)
        
        return ranking.reset_index(drop=True)
    
    def obtener_parametros_equipo(self, equipo):
        """Devuelve parámetros (alpha/beta) y sus interpretaciones."""
        if self.alpha is None or self.beta is None:
            raise ValueError("Primero debes entrenar el modelo")
        
        from .utils import validar_equipo
        validar_equipo(equipo, self.equipos)
        
        return {
            'equipo': equipo,
            'alpha': self.alpha[equipo],
            'beta': self.beta[equipo],
            'interpretacion_ataque': interpretar_parametro(self.alpha[equipo], 'alpha'),
            'interpretacion_defensa': interpretar_parametro(self.beta[equipo], 'beta')
        }
    
    def comparar_equipos(self, lista_equipos):
        """Compara alpha/beta de los equipos dados; retorna DataFrame."""
        comparacion = []
        
        for equipo in lista_equipos:
            if equipo in self.equipos:
                comparacion.append({
                    'Equipo': equipo,
                    'Alpha (Ataque)': self.alpha[equipo],
                    'Beta (Defensa)': self.beta[equipo]
                })
        
        return pd.DataFrame(comparacion)
    
    def simular_jornada(self, lista_partidos, mostrar=True):
        """Simula múltiples partidos; devuelve DataFrame con probabilidades."""
        resultados = []
        
        for local, visitante in lista_partidos:
            if local in self.equipos and visitante in self.equipos:
                pred_dict = self.predecir(local, visitante, mostrar=False)
                
                resultados.append({
                    'Local': local,
                    'Visitante': visitante,
                    'P(Vic_Local)_%': pred_dict['prob_victoria_local'] * 100,
                    'P(Empate)_%': pred_dict['prob_empate'] * 100,
                    'P(Vic_Visit)_%': pred_dict['prob_victoria_visitante'] * 100,
                    'Marcador_Probable': pred_dict['marcador_mas_probable']
                })
        
        df_jornada = pd.DataFrame(resultados)
        
        if mostrar:
            imprimir_titulo("PREDICCIONES DE LA JORNADA")
            print(df_jornada.to_string(index=False))
            print()
        
        return df_jornada
    
    def exportar_parametros(self, ruta_salida='parametros_modelo.csv'):
        """Exporta alpha/beta/gamma a CSV."""
        if self.alpha is None:
            raise ValueError("Primero debes entrenar el modelo")
        
        datos_export = []
        for equipo in self.equipos:
            datos_export.append({
                'Equipo': equipo,
                'Alpha_Ataque': self.alpha[equipo],
                'Beta_Defensa': self.beta[equipo],
                'Gamma_Local': self.gamma
            })
        
        df = pd.DataFrame(datos_export)
        df.to_csv(ruta_salida, index=False)
        print(f"✓ Parámetros exportados a: {ruta_salida}")
    
    def resumen_modelo(self):
        """Imprime resumen del ajuste y top equipos."""
        if self.modelo_entrenado is None:
            print("El modelo aún no ha sido entrenado.")
            return
        
        imprimir_titulo("RESUMEN DEL MODELO")
        
        print(f"\n DATOS:")
        print(f"  • Partidos históricos: {len(self.datos_originales)}")
        print(f"  • Equipos: {len(self.equipos)}")
        print(f"  • Observaciones entrenamiento: {len(self._datos_entrenamiento)}")
        
        print(f"\n CALIDAD DEL AJUSTE:")
        print(f"  • Log-Likelihood: {self.modelo_entrenado.llf:.2f}")
        print(f"  • AIC: {self.modelo_entrenado.aic:.2f}")
        
        print(f"\n PARÁMETROS:")
        print(f"  • Ventaja de local (γ): {self.gamma:.3f}")
        
        print(f"\n TOP 3 ATAQUE:")
        top_ataque = self.obtener_ranking_ataque(top_n=3)
        for _, row in top_ataque.iterrows():
            print(f"  {row['Ranking']}. {row['Equipo']}: {row['Alpha']:.3f}")
        
        print(f"\n TOP 3 DEFENSA:")
        top_defensa = self.obtener_ranking_defensa(top_n=3)
        for _, row in top_defensa.iterrows():
            print(f"  {row['Ranking']}. {row['Equipo']}: {row['Beta']:.3f}")
        
        print()