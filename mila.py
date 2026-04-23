import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

frases = [
    "hola", "buenos dias", "hey", "buenas", "que tal",
    "adios", "hasta luego", "chao", "nos vemos", "bye",
    "como te llamas", "quien eres", "que eres", "presentate",
    "ayuda", "no entiendo", "explica", "que significa", "como funciona",
    "gracias", "muchas gracias", "te lo agradezco",
]

intenciones = [
    "saludo", "saludo", "saludo", "saludo", "saludo",
    "despedida", "despedida", "despedida", "despedida", "despedida",
    "identidad", "identidad", "identidad", "identidad",
    "ayuda", "ayuda", "ayuda", "ayuda", "ayuda",
    "agradecimiento", "agradecimiento", "agradecimiento",
]

vectorizador = TfidfVectorizer()
X = vectorizador.fit_transform(frases)

modelo = LogisticRegression()
modelo.fit(X, intenciones)

instrucciones = {
    "saludo": "El usuario saluda. Responde de forma cordial y pregunta cómo puedes ayudar.",
    "despedida": "El usuario se despide. Deséale un feliz día de manera educada.",
    "identidad": "Explica que eres Mila, una asistente virtual diseñada para ayudar.",
    "ayuda": "El usuario necesita asistencia. Responde con paciencia y ofrece una explicación clara.",
    "agradecimiento": "El usuario da las gracias. Responde con amabilidad diciendo que es un placer ayudar.",
    "general": "Mantén siempre un tono respetuoso, profesional y positivo.",
}

def clasificar_intencion(mensaje):
    vector = vectorizador.transform([mensaje])
    return modelo.predict(vector)[0]

def preguntar_mila(historial, mensaje):
    intencion = clasificar_intencion(mensaje)
    instruccion = instrucciones.get(intencion, instrucciones["general"])

    historial.append({"role": "user", "content": mensaje})

    respuesta = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3",
            "messages": [
                {"role": "system", "content": f"Eres Mila, una asistente inteligente y amable. Responde siempre en español. {instruccion}"}
            ] + historial,
            "stream": False
        }
    )

    contenido = respuesta.json()["message"]["content"]
    historial.append({"role": "assistant", "content": contenido})
    return contenido

def main():
    historial = []
    print("Mila: Hola, soy Mila. Escribe 'salir' para terminar.\n")

    activo = True
    while activo:
        entrada = input("Tu: ").strip()
        if entrada.lower() == "salir":
            print("Mila: Hasta luego.")
            activo = False
        elif entrada:
            respuesta = preguntar_mila(historial, entrada)
            print(f"Mila: {respuesta}\n")

if __name__ == "__main__":
    main() 
