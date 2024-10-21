import os
from dotenv import load_dotenv  # Para cargar las variables de entorno
import fitz
import nltk
import streamlit as st
import openai   # OpenAI debe importarse como 'openai', no 'OpenAI'



# Cargar las stopwords de NLTK
nltk.download('stopwords')

load_dotenv()

# Obtener la clave API desde la variable de entorno
api_key = os.getenv("OPENAI_API_KEY")


if api_key is None:
    st.error("No se encontró la clave API de OpenAI. Verifica las variables de entorno en Streamlit Cloud.")
else:
    # Asignar la clave API globalmente
    openai.api_key = api_key

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def preprocess_text(text):
    # Reemplazar saltos de línea por espacios
    text = text.replace('\n', ' ')
    # Eliminar espacios duplicados
    text = ' '.join(text.split())
    return text

def remove_stopwords(text):
    stop_words = set(nltk.corpus.stopwords.words('spanish'))  # Usa 'english' para inglés o cambia según tu idioma
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)


def clean_text(text):
    # Eliminar líneas repetidas o redundantes
    lines = text.split('.')
    unique_lines = list(dict.fromkeys(lines))  # Remueve duplicados mientras mantiene el orden
    cleaned_text = '.'.join(unique_lines)
    return cleaned_text

# Inicializar una variable para almacenar todo el texto concatenado

# La variable Texto_Final contiene todo el texto de los PDFs procesado y concatenado

@st.cache_data
def load_text_files():
    # Especifica la ruta del archivo de texto
    file_path = r'DOCUMENTOS/RESUMEN MANUAL GARANTIAS.txt'

    # Lee el archivo de texto y almacena el contenido en una variable
    with open(file_path, 'r', encoding='utf-8') as file:
        Texto_Final = file.read()

    # Especifica la ruta del archivo de texto
    file_path = r'DOCUMENTOS/Resumen GPT.txt'

    # Lee el archivo de texto y almacena el contenido en una variable
    with open(file_path, 'r', encoding='utf-8') as file:
        document_text = file.read()

    processed_text = preprocess_text(document_text)
    final_text = remove_stopwords(processed_text)
    cleaned_text = clean_text(final_text)
    Texto_Final2=cleaned_text

    return Texto_Final,Texto_Final2

# Cargar textos y almacenarlos en variables
Texto_Final,Texto_Final2 = load_text_files()
#st.write(Texto_Final) 

# Definir función principal de Streamlit
def run_chatbot():
#    st.title("🤖 Arquitectura de Datos - Asistente Manual de Garantias")
    logo_path ="FNG.png"

    col1, col2 = st.columns([1, 5])

    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image(logo_path, width=120)  # Ajusta el tamaño del logo si es necesario

    with col2:
        #st.title("Subd. Arquitectura de Datos")
        #st.title("🤖 Arquitectura de Datos - Asistente Manual de Garantias")
        #st.markdown("<h1 style='color:white; font-size: 1.5em;'>🤖 Subdirección Arquitectura de Datos -<br> Asistente Manual de Garantías</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center;">
                <h1 style='color:white; font-size: 2.0em;'>🤖 Subdirección Arquitectura de Datos -<br> Asistente - Manual de Garantías</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    #st.title("🤖 Arquitectura de Datos - Asistente Manual de Garantias")

    st.markdown(
            """
            <style>
            .main {
                background-color: #111111;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    # Inicializar el historial de mensajes si no existe en session_state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"""
            
            Eres un asistente el cual dará apoyo al área comercial, se necesita que des respuestas claras y concisas respecto al tema que se te pregunta, los contenidos sobre el cuales unicamente puedes responder son: {Texto_Final} y {Texto_Final2}.
            
            """},
            {"role": "system", "content": "No respondas con Fondo Nacional de Garantías, siempre abrévialo como FNG."}
        ]

    # Display chat messages from history on app rerun


    prompt = st.chat_input("En que te puedo ayudar?")

    if prompt:
        # Definir los mensajes que se enviarán al modelo de IA

        messages = st.session_state.messages


        st.session_state.messages.append({"role": "user", "content": prompt})
            

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Seleccionar modelo: gpt-3.5-turbo | gpt-4 | gpt-4-turbo
            messages=messages,
            temperature=1
            #max_tokens=300
        )

        contenido = response.choices[0].message.content
        
        # Mostrar la respuesta en la aplicación Streamlit
        #st.write(f"**Respuesta de la IA:** {contenido}")

        st.session_state.messages.append({"role": "assistant", "content": contenido})


    # Mostrar el historial completo de la conversación
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write(f"**🧑‍💻 Tú:** {message['content']}")
            elif message["role"] == "assistant":
                st.write(f"**ChatBot💭:** {message['content']}")

# Ejecutar la función principal en la aplicación de Streamlit
if __name__ == "__main__":
    run_chatbot()
