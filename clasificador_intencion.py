import re

def normalizar_texto(texto):
    """Limpia el texto convirtiéndolo a minúsculas, quitando puntuación y acentos."""
    texto = str(texto).lower().strip()
    
    # Tabla de reemplazo de acentos comunes
    remplazos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}
    for con, sin in remplazos.items():
        texto = texto.replace(con, sin)
        
    # Exclusión de caracteres especiales y signos
    texto = re.sub(r'[¿?¡!.,;:]', '', texto)
    return texto

def clasificar_intencion(frase):
    frase_procesada = normalizar_texto(frase)
    
    # Diccionarios semánticos controlados (Keywords extendidas para robustez del MVP)
    patrones_cambiar = ['cambiar', 'reprogramar', 'mover', 'modificar', 'posponer', 'otro dia', 'reajustar']
    patrones_cancelar = ['cancelar', 'baja', 'eliminar', 'anular', 'quitar', 'no voy a ir', 'no puedo ir']
    
    # Buscar coincidencias de palabras raíz
    for palabra in patrones_cambiar:
        if palabra in frase_procesada:
            return "CAMBIAR_CITA"
            
    for palabra in patrones_cancelar:
        if palabra in frase_procesada:
            return "CANCELAR_CITA"
            
    return "INTENCION_NO_RECONOCIDA"

if __name__ == "__main__":
    # Set de pruebas del examen
    frases_ejemplo = [
        "Necesito cambiar mi cita",
        "Quiero cancelar mi cita",
        "¿Me podrían mover el turno para el próximo mes?",
        "Ya no voy a asistir a la cita medica, bórrenla por favor",
        "¿Qué especialidades atienden?"
    ]
    
    print("\n=========================================")
    print("      PRUEBA DE CLASIFICADOR DE IA       ")
    print("=========================================")
    for f in frases_ejemplo:
        resultado = clasificar_intencion(f)
        print(f"Frase original: '{f}'")
        print(f"Resultado -> [{resultado}]")
        print("-" * 41)