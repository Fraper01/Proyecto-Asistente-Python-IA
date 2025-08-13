"""
Asistente de Aprendizaje de Python con Ollama
------------------------------------------------------
Este script combina la funcionalidad de dos proyectos: un chat de consola y un
asistente educativo de Python. La aplicación se conecta a un modelo de IA local
a través de la API de Ollama para ofrecer información sobre librerías de Python.

Características principales:
- Interfaz de consola simple y amigable.
- Utiliza la API de Ollama para obtener información sobre librerías de Python.
- El modelo de IA actúa como un experto en programación de Python.
- Un prompt bien estructurado guía a la IA para dar respuestas detalladas y útiles.
- Muestra el streaming de la respuesta de la IA en tiempo real.
- Elaboración por Francisco Javier Pérez, 2025
"""

import os
import requests
import json
import sys

# 🌐 Dirección local de la API de Ollama
OLLAMA_URL = "http://localhost:11434/api/chat"
# ✅ Modelo de IA a utilizar, puedes cambiarlo si tienes otros instalados
MODEL = "llama3"

def limpiar_terminal():
    """Limpia la pantalla de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_respuesta_ia_stream(respuesta_stream):
    """
    Muestra la respuesta de la IA en la consola, letra por letra,
    simulando una conversación en tiempo real.
    """
    print("🤖 Asistente de Python: ", end="", flush=True)
    for chunk in respuesta_stream:
        # Extraer el contenido del mensaje
        try:
            data = json.loads(chunk)
            if "message" in data and "content" in data["message"]:
                content = data["message"]["content"]
                print(content, end="", flush=True)
        except json.JSONDecodeError:
            continue
    print("\n")  

def obtener_informacion_ia(libreria: str, tema: str) -> str:
    """
    Envía un prompt a la IA para que actúe como un experto en Python
    y devuelve la respuesta en streaming.
    """
    prompt = f"""
    **Instrucciones:**
    Actúa como un experto asistente en programación de Python. Tu objetivo es proporcionar información detallada y precisa sobre la **librería** y el **tema** que se te solicitan, usando ejemplos de código.

    **Parámetros:**
    * **Librería:** {libreria}
    * **Tema:** {tema}

    **Formato de la respuesta:**
    Proporciona la información de la siguiente manera:
    1. **Definición del Tema:** Explica qué es, su propósito principal y cuándo se utiliza.
    2. **Ejemplo de Uso:** Incluye un ejemplo de código en Python sencillo y funcional.
    3. **Consideraciones Importantes:** Menciona buenas prácticas o posibles errores comunes.
    
    Asegúrate de responder en español y de forma clara para un programador intermedio. No incluyas un saludo o despedida en tu respuesta, ve directo al grano y trata en lo posible de no usar mas de 100 token.
    """
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Eres un asistente experto en programación de Python."},
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        if response.status_code == 200:
            return response.iter_lines(decode_unicode=True)
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return []
    except requests.exceptions.ConnectionError:
        print("\n❌ Error de conexión: Asegúrate de que Ollama esté en ejecución y el modelo esté descargado.")
        return []

def menu_pandas():
    """
    Muestra el menú de opciones para la librería Pandas.
    """
    while True:
        limpiar_terminal()
        titulo = "Librerías de Python - Pandas"
        ancho_linea = 40
        print("-" * ancho_linea)
        print(titulo.center(ancho_linea))
        print("-" * ancho_linea)
        print("1. ¿Qué es Pandas?")
        print("2. ¿Qué es un DataFrame?")
        print("3. ¿Qué es una Series?")
        print("4. Crear y visualizar un DataFrame")
        print("9. Regresar al menú principal")
        print("-" * ancho_linea)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == '1':
            respuesta = obtener_informacion_ia(libreria="Pandas", tema="Definición de Pandas")
            mostrar_respuesta_ia_stream(respuesta)
        elif opcion == '2':
            respuesta = obtener_informacion_ia(libreria="Pandas", tema="Qué es un DataFrame")
            mostrar_respuesta_ia_stream(respuesta)
        elif opcion == '3':
            respuesta = obtener_informacion_ia(libreria="Pandas", tema="Qué es una Series")
            mostrar_respuesta_ia_stream(respuesta)
        elif opcion == '4':
            respuesta = obtener_informacion_ia(libreria="Pandas", tema="Crear y visualizar DataFrame")
            mostrar_respuesta_ia_stream(respuesta)
        elif opcion == '9':
            break
        else:
            print("Opción inválida. Por favor, intenta de nuevo.")
        input("Pulsa Enter para continuar...")

def main_menu():
    """
    Muestra el menú principal de librerías.
    """
    while True:
        limpiar_terminal()
        titulo = "Asistente de IA para Python"
        ancho_linea = 40
        print("Elaborado por: Monica & Francisco")
        print("-" * ancho_linea)
        print(titulo.center(ancho_linea))
        print("-" * ancho_linea)
        print("1. Pandas")
        print("2. NumPy")
        print("3. Matplotlib")
        print("4. Scikit-learn")
        print("9. Salir")
        print("-" * ancho_linea)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == '1':
            menu_pandas()
        elif opcion == '2' or opcion == '3' or opcion == '4':
            print("🛠️ Funcionalidad en construcción. Por favor, selecciona Pandas.")
            input("Pulsa Enter para continuar...")
        elif opcion == '9':
            print("\n👋 ¡Gracias por usar el asistente! Hasta luego.")
            break
        else:
            print("Opción inválida. Por favor, intenta de nuevo.")
            input("Pulsa Enter para continuar...")

if __name__ == "__main__":
    main_menu()
