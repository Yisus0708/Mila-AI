import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class NeuronaMcCullochPitts:

    def __init__(self, pesos, umbral):
        self.pesos = pesos
        self.umbral = umbral

    def activar(self, entradas):

        suma = 0

        for w, x in zip(self.pesos, entradas):
            suma += w * x

        if suma >= self.umbral:
            return 1
        else:
            return 0


def detectar_saludo_mp(mensaje):

    palabras = mensaje.lower().split()

    entradas = [
        1 if "hola" in palabras else 0,
        1 if "buenos" in palabras else 0,
        1 if "hey" in palabras else 0
    ]

    neurona = NeuronaMcCullochPitts(
        pesos=[1,1,1],
        umbral=1
    )

    return neurona.activar(entradas)


def detectar_despedida_mp(mensaje):

    palabras = mensaje.lower().split()

    entradas = [
        1 if "adios" in palabras else 0,
        1 if "chao" in palabras else 0,
        1 if "bye" in palabras else 0
    ]

    neurona = NeuronaMcCullochPitts(
        pesos=[1,1,1],
        umbral=1
    )

    return neurona.activar(entradas)


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

    mensaje = mensaje.lower()

    if detectar_saludo_mp(mensaje):
        respuesta = "¡Hola! Soy Mila. ¿En qué puedo ayudarte?"
        historial.append({"role": "assistant", "content": respuesta})
        return respuesta, historial

    if detectar_despedida_mp(mensaje):
        respuesta = "Hasta luego ¡Que tengas un excelente día!"
        historial.append({"role": "assistant", "content": respuesta})
        return respuesta, historial

    intencion = clasificar_intencion(mensaje)
    instruccion = instrucciones.get(intencion, instrucciones["general"])

    historial.append({"role": "user", "content": mensaje})

    historial = historial[-10:]

    try:

        respuesta = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",
                "messages": [
                    {
                        "role": "system",
                        "content": f"Eres Mila, una asistente inteligente y amable. Responde siempre en español. {instruccion}"
                    }
                ] + historial,
                "stream": False
            }
        )

        contenido = respuesta.json()["message"]["content"]

    except Exception as e:

        contenido = "Hubo un error conectando con Mila."

    historial.append({"role": "assistant", "content": contenido})

    return contenido, historial


def main():

    historial = []

    print("\nMila iniciada correctamente.")
    print("Escribe 'salir' para terminar.\n")

    activo = True

    while activo:

        entrada = input("Tu: \n").strip()

        if entrada.lower() == "salir":

            print("Mila: Hasta luego")
            activo = False

        elif entrada:

            respuesta, historial = preguntar_mila(
                historial,
                entrada
            )

            print(f"Mila: {respuesta}\n")


if __name__ == "__main__":
    main()