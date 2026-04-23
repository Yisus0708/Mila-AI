# 🤖 MILA — Asistente Inteligente con IA Local

> Proyecto académico que demuestra la evolución de la Inteligencia Artificial desde sus fundamentos matemáticos de 1943 hasta los modelos de lenguaje modernos, implementando un asistente conversacional en tres niveles de complejidad creciente.

---

## 📋 Tabla de Contenidos

- [¿Qué es MILA?](#-qué-es-mila)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Requisitos previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Nivel 1 — mila.py](#-nivel-1--milapy)
- [Nivel 2 — mila2.py](#-nivel-2--mila2py)
- [Nivel 3 — mila3.py](#-nivel-3--mila3py)
- [Fórmulas y fundamentos matemáticos](#-fórmulas-y-fundamentos-matemáticos)
- [Estructura del proyecto](#-estructura-del-proyecto)

---

## ¿Qué es MILA?

MILA es una asistente virtual construida en Python que combina tres enfoques distintos de la inteligencia artificial trabajando en conjunto:

- **Neurona McCulloch-Pitts (1943)** — el primer modelo matemático de neurona artificial
- **Machine Learning clásico** — clasificación de intenciones con TF-IDF y Regresión Logística
- **LLM moderno (Llama3)** — generación de respuestas naturales vía Ollama local

El proyecto está estructurado en tres archivos, cada uno una evolución del anterior.

---

## 🛠 Tecnologías utilizadas

| Tecnología | Función |
|------------|---------|
| Python 3.10+ | Lenguaje base |
| scikit-learn | TF-IDF + Regresión Logística |
| requests | Comunicación con Ollama |
| Ollama + Llama3 | Modelo de lenguaje local |
| pygame | Interfaz gráfica animada (mila3) |
| speech_recognition | Reconocimiento de voz (mila3) |
| pyttsx3 | Síntesis de voz offline (mila3) |
| threading | Procesamiento paralelo (mila3) |

---

## 📦 Requisitos previos

### 1. Instalar Ollama

Ollama permite correr modelos de lenguaje grandes (LLMs) de forma local, sin internet.

**Linux / macOS:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** Descargar el instalador desde [https://ollama.com](https://ollama.com)

### 2. Descargar el modelo Llama3

```bash
ollama pull llama3
```

### 3. Verificar que Ollama esté corriendo

```bash
ollama serve
```

Debe estar activo en `http://localhost:11434`

---

## 🔧 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/mila-asistente.git
cd mila-asistente

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install scikit-learn requests pygame SpeechRecognition pyttsx3
```

---

## 🟢 Nivel 1 — mila.py

### ¿Qué hace?

El prototipo base. MILA recibe texto del usuario, clasifica la **intención** del mensaje usando machine learning, y genera una respuesta contextual usando Llama3.

### Flujo de funcionamiento

```
Usuario escribe
      ↓
TF-IDF convierte el texto en vector numérico
      ↓
Regresión Logística predice la intención
(saludo / despedida / identidad / ayuda / agradecimiento)
      ↓
Se selecciona una instrucción específica para esa intención
      ↓
Se envía al LLM (Llama3 vía Ollama) con el historial completo
      ↓
MILA responde en español
```

### Cómo ejecutarlo

```bash
python mila.py
```

### Intenciones reconocidas

| Intención | Frases de ejemplo |
|-----------|------------------|
| saludo | hola, buenos días, hey |
| despedida | adiós, chao, bye |
| identidad | quién eres, cómo te llamas |
| ayuda | ayuda, no entiendo, explica |
| agradecimiento | gracias, muchas gracias |

---

## 🔵 Nivel 2 — mila2.py

### ¿Qué agrega?

Incorpora la **Neurona McCulloch-Pitts** implementada desde cero, creando una arquitectura de **tres capas de IA** que trabajan en cascada. También agrega manejo de errores y limitación del historial.

### Arquitectura de tres capas

```
Capa 1 — Neurona McCulloch-Pitts (1943)
   ↓ Si detecta saludo o despedida → responde directo (sin LLM)
   ↓ Si no detecta nada → pasa a la siguiente capa

Capa 2 — TF-IDF + Regresión Logística (ML clásico)
   ↓ Clasifica la intención del mensaje
   ↓ Selecciona instrucción de contexto

Capa 3 — Llama3 vía Ollama (LLM moderno)
   ↓ Genera respuesta natural en español
   ↓ Con los últimos 10 mensajes del historial
```

### Cómo ejecutarlo

```bash
python mila2.py
```

### Diferencias con mila.py

- ✅ Neurona McCulloch-Pitts para filtrar casos simples
- ✅ Historial limitado a 10 mensajes (eficiencia de memoria)
- ✅ Manejo de errores con `try/except`
- ✅ Respuestas directas para saludos/despedidas sin consumir el LLM

---

## 🟣 Nivel 3 — mila3.py

### ¿Qué agrega?

La versión completa con **voz, interfaz gráfica animada y activación por palabra clave**, similar a Alexa o Google Assistant.

### Componentes principales

**Reconocimiento de voz**
- Escucha continuamente el micrófono
- Se activa solo cuando detecta la palabra clave `"mila"`
- Usa Google Speech-to-Text para convertir audio a texto

**Síntesis de voz**
- Responde hablando en español con `pyttsx3`
- Funciona completamente sin internet

**Interfaz gráfica (Pygame)**
- Esfera 3D de 300 puntos generados con la espiral de Fibonacci
- Cambia de color según el estado de MILA
- Los puntos pulsan con ondas seno/coseno sincronizadas con el volumen de voz

**Estados visuales**

| Estado | Color | Descripción |
|--------|-------|-------------|
| ESPERANDO | Azul `(0, 100, 255)` | Modo bajo consumo, esperando "mila" |
| ESCUCHANDO | Verde turquesa `(0, 255, 200)` | Activa y procesando |

### Cómo ejecutarlo

```bash
python mila3.py
```

### Comandos de voz

- Decir **"mila"** → activa la asistente
- Decir **"adiós"** o **"descansa"** → vuelve al modo espera
- Cualquier otra frase → MILA consulta al LLM y responde

### Threading (procesamiento paralelo)

```
Hilo principal → animación Pygame a 60 fps
Hilo secundario (daemon) → bucle de voz (escuchar → procesar → hablar)
```

---

## 📐 Fórmulas y fundamentos matemáticos

### 1. Neurona McCulloch-Pitts (1943)

La neurona más simple de la historia de la IA. Recibe entradas binarias, las pondera y activa si supera un umbral.

**Fórmula:**

$$y = \begin{cases} 1 & \text{si } \sum_{i=1}^{n} w_i \cdot x_i \geq \theta \\ 0 & \text{si } \sum_{i=1}^{n} w_i \cdot x_i < \theta \end{cases}$$

Donde:
- `xᵢ` = entradas binarias (0 o 1) — presencia de palabras clave
- `wᵢ` = pesos (en este proyecto, todos igual a 1)
- `θ` (theta) = umbral de activación (en este proyecto, θ = 1)
- `y` = salida de la neurona (0 = no activa, 1 = activa)

**Ejemplo en el código:**
```python
entradas = [1, 0, 0]  # "hola" presente, "buenos" no, "hey" no
pesos    = [1, 1, 1]
umbral   = 1

suma = (1×1) + (1×0) + (1×0) = 1
# 1 >= 1 → neurona se activa → es un saludo
```

---

### 2. TF-IDF (Term Frequency — Inverse Document Frequency)

Convierte texto en vectores numéricos según la importancia de cada palabra.

**Fórmula TF (frecuencia del término):**

$$TF(t, d) = \frac{\text{veces que } t \text{ aparece en } d}{\text{total de términos en } d}$$

**Fórmula IDF (frecuencia inversa de documento):**

$$IDF(t) = \log\left(\frac{N}{1 + df(t)}\right)$$

**TF-IDF combinado:**

$$TF\text{-}IDF(t, d) = TF(t, d) \times IDF(t)$$

Donde:
- `t` = término (palabra)
- `d` = documento (frase del usuario)
- `N` = total de documentos en el corpus
- `df(t)` = número de documentos que contienen el término `t`

---

### 3. Regresión Logística

Clasifica el vector TF-IDF en una de las intenciones posibles usando la **función sigmoide**.

**Función sigmoide:**

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

**Predicción:**

$$P(y = k \mid x) = \frac{e^{w_k \cdot x}}{\sum_{j=1}^{K} e^{w_j \cdot x}}$$

Esta es la versión multiclase llamada **Softmax**, donde:
- `x` = vector TF-IDF del mensaje
- `wₖ` = pesos aprendidos para la clase `k`
- `K` = número total de clases (5 intenciones)

---

### 4. Espiral de Fibonacci en la esfera (mila3.py)

Para distribuir 300 puntos uniformemente en la superficie de una esfera, se usa la **espiral de Fibonacci** (también llamada espiral áurea):

**Fórmulas:**

$$y_i = 1 - \frac{2i}{N - 1}, \quad i = 0, 1, \ldots, N-1$$

$$r_i = \sqrt{1 - y_i^2}$$

$$\theta_i = \pi \cdot (1 + \sqrt{5}) \cdot i$$

$$x_i = \cos(\theta_i) \cdot r_i, \quad z_i = \sin(\theta_i) \cdot r_i$$

Donde `N` = número total de puntos (300) y `√5 ≈ 2.236` es la razón áurea.

---

### 5. Ondas de deformación de la esfera (mila3.py)

Cada punto de la esfera se deforma con una función de onda compuesta para simular pulsación:

$$\text{onda} = \sin(y \cdot 5 + t \cdot 4) \cdot \cos(x \cdot 5 + t \cdot 2) \cdot A$$

$$\text{distancia} = 160 + \text{onda}$$

Donde:
- `t` = tiempo actual en segundos
- `A` = amplitud (10 en espera, 25 escuchando, +volumen de voz)

---

## 📁 Estructura del proyecto

```
mila-asistente/
│
├── mila.py        # Nivel 1 — Chatbot base (TF-IDF + Regresión Logística + LLM)
├── mila2.py       # Nivel 2 — Neurona McCulloch-Pitts + ML + LLM
├── mila3.py       # Nivel 3 — Voz + Interfaz gráfica + Palabra clave
└── README.md      # Este archivo
```

---

## 👤 Autor

Proyecto académico de demostración de conceptos de Inteligencia Artificial.

---

## 📄 Licencia

MIT License — libre para uso educativo.
