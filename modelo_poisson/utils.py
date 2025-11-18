"""Utilidades: sanitizar nombres, validaciones y formatos simples."""

import re


def sanitizar_nombre(nombre):
    """Convierte nombre de equipo a identificador seguro (guiones bajos)."""
    # Reemplazar espacios, puntos y guiones por guiones bajos
    nombre_limpio = nombre.replace(' ', '_').replace('.', '').replace('-', '_')
    
    # Eliminar caracteres especiales excepto guiones bajos
    nombre_limpio = re.sub(r'[^\w]', '', nombre_limpio)
    
    return nombre_limpio


def validar_equipo(equipo, lista_equipos):
    """Verifica que `equipo` esté en `lista_equipos`, lanza ValueError si no."""
    if equipo not in lista_equipos:
        raise ValueError(
            f"Equipo '{equipo}' no encontrado. "
            f"Equipos disponibles: {', '.join(sorted(lista_equipos))}"
        )
    return True


def calcular_percentil(valor, valores_lista):
    """Devuelve el percentil de `valor` en `valores_lista` (0-100)."""
    valores_ordenados = sorted(valores_lista)
    posicion = valores_ordenados.index(valor)
    return (posicion / len(valores_ordenados)) * 100


def interpretar_parametro(parametro, tipo='alpha'):
    """Devuelve una interpretación breve del parámetro (alpha o beta)."""
    diferencia_pct = (parametro - 1.0) * 100
    
    if tipo == 'alpha':
        # Para ataque: valores mayores = mejor
        if parametro > 1.3:
            categoria = "Muy fuerte"
        elif parametro > 1.15:
            categoria = "Fuerte"
        elif parametro > 1.05:
            categoria = "Ligeramente superior"
        elif parametro > 0.95:
            categoria = "Promedio"
        elif parametro > 0.85:
            categoria = "Ligeramente inferior"
        else:
            categoria = "Débil"
        
        return f"Ataque {abs(diferencia_pct):.1f}% {'superior' if diferencia_pct > 0 else 'inferior'} al promedio ({categoria})"
    
    else:  # beta
        # Para defensa: valores menores = mejor
        if parametro < 0.75:
            categoria = "Muy fuerte"
        elif parametro < 0.85:
            categoria = "Fuerte"
        elif parametro < 0.95:
            categoria = "Ligeramente superior"
        elif parametro < 1.05:
            categoria = "Promedio"
        elif parametro < 1.15:
            categoria = "Ligeramente inferior"
        else:
            categoria = "Débil"
        
        return f"Defensa {abs(diferencia_pct):.1f}% {'mejor' if diferencia_pct < 0 else 'peor'} que el promedio ({categoria})"


def formatear_probabilidad(probabilidad, decimales=1):
    """Formatea float 0..1 como porcentaje con `decimales` decimales."""
    return f"{probabilidad * 100:.{decimales}f}%"


def imprimir_separador(caracter='=', longitud=70):
    """Imprime una línea separadora repetida `longitud` veces."""
    print(caracter * longitud)


def imprimir_titulo(titulo, caracter='='):
    """Imprime `titulo` rodeado por líneas de separación."""
    imprimir_separador(caracter)
    print(titulo)
    imprimir_separador(caracter)