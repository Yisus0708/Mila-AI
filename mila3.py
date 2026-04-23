import pygame
import math
import speech_recognition as sr
import threading
import sys
import time
import pyttsx3
import requests

PALABRA_CLAVE = "mila"
estado = "ESPERANDO"
color_esfera = (0, 100, 255)
volumen_voz = 0
activo = True

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    if "spanish" in voice.name.lower():
        engine.setProperty('voice', voice.id)
engine.setProperty('rate', 180)

def hablar(texto):
    global volumen_voz
    print(f"[MILA]: {texto}")
    volumen_voz = 20
    engine.say(texto)
    engine.runAndWait()
    volumen_voz = 0

def consultar_ia(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": f"Eres Mila, una asistente inteligente y amable. Responde siempre en español. Si la pregunta es simple responde corto y directo. Si la pregunta necesita pasos o lista, usa numeración. Usuario dice: {prompt}",
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=180)
        return response.json().get("response", "Error al procesar.")
    except:
        return "No pude obtener respuesta. Intenta de nuevo."

def bucle_voz():
    global estado, color_esfera, volumen_voz, activo
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 1200
    recognizer.dynamic_energy_threshold = True

    print(f">>> [SISTEMA]: Nucleo listo. Palabra clave: '{PALABRA_CLAVE}'")

    while activo:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, phrase_time_limit=5)
                texto = recognizer.recognize_google(audio, language="es-ES").lower()
                print(f"Escuchado: {texto}")

                if estado == "ESPERANDO" and PALABRA_CLAVE in texto:
                    estado = "ESCUCHANDO"
                    color_esfera = (0, 255, 200)
                    hablar("En linea. En que puedo ayudarte?")

                elif estado == "ESCUCHANDO":
                    if "descansa" in texto or "adios" in texto:
                        estado = "ESPERANDO"
                        color_esfera = (0, 100, 255)
                        hablar("Entrando en modo de bajo consumo.")
                    else:
                        hablar("Dame un momento, estoy procesando tu pregunta.")
                        respuesta = consultar_ia(texto)
                        hablar(respuesta)

        except Exception:
            continue

threading.Thread(target=bucle_voz, daemon=True).start()

WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MILA - Asistente Inteligente")
clock = pygame.time.Clock()

num_puntos = 300
puntos = []
for i in range(num_puntos):
    y = 1 - (i / float(num_puntos - 1)) * 2
    radius_at_y = math.sqrt(1 - y * y)
    theta = math.pi * (1 + 5**0.5) * i
    x = math.cos(theta) * radius_at_y
    z = math.sin(theta) * radius_at_y
    puntos.append([x, y, z])

angulo_rotacion = 0

corriendo = True
while corriendo:
    screen.fill((5, 5, 15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            activo = False
            pygame.quit()
            sys.exit()

    angulo_rotacion += 0.01
    t = time.time()

    for p in puntos:
        x_orig, y_orig, z_orig = p

        x = x_orig * math.cos(angulo_rotacion) - z_orig * math.sin(angulo_rotacion)
        z = x_orig * math.sin(angulo_rotacion) + z_orig * math.cos(angulo_rotacion)
        y = y_orig

        amplitud = 25 if estado == "ESCUCHANDO" else 10
        amplitud += volumen_voz

        onda = math.sin(y * 5 + t * 4) * math.cos(x * 5 + t * 2) * amplitud
        distancia = 160 + onda

        factor_persp = 400 / (z + 4)
        plot_x = int(x * distancia * (factor_persp / 200) + WIDTH / 2)
        plot_y = int(y * distancia * (factor_persp / 200) + HEIGHT / 2)

        brillo = int(max(50, 255 * (z + 1) / 2))
        r, g, b = color_esfera
        color_final = (max(0, r-50), min(255, g + brillo//4), min(255, b + brillo//2))

        size = max(1, int(2 * (z + 1.5)))
        pygame.draw.circle(screen, color_final, (plot_x, plot_y), size)

    surface_glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(surface_glow, (color_esfera[0], color_esfera[1], color_esfera[2], 30), (WIDTH//2, HEIGHT//2), 180 + volumen_voz)
    screen.blit(surface_glow, (0, 0))

    pygame.display.flip()
    clock.tick(60)