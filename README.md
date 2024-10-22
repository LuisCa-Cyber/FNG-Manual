# 🧠 Chatbot de Asistente Comercial - FNG
Este proyecto es una aplicación de chatbot diseñada para asistir al equipo comercial del Fondo Nacional de Garantías (FNG), utilizando la API de OpenAI. La aplicación está construida en Streamlit y tiene como objetivo proporcionar respuestas concisas y claras sobre temas específicos relacionados con el reglamento de garantías y otros textos predefinidos.

## Características

**Procesamiento de documentos PDF**: Utiliza la biblioteca PyMuPDF (fitz) para extraer texto de archivos PDF. El texto extraído puede ser limpiado y preprocesado, eliminando stopwords y líneas redundantes.

**Modelo GPT-3.5 de OpenAI**: El chatbot utiliza el modelo gpt-3.5-turbo de OpenAI para generar respuestas inteligentes a partir de un historial de conversación proporcionado por el usuario.

**Preprocesamiento de texto**: El proyecto incluye funciones para limpiar y preprocesar texto, eliminando palabras vacías (stopwords) utilizando NLTK.

**Integración con OpenAI**: Carga la clave de la API de OpenAI desde un archivo .env para interactuar con el modelo de lenguaje.

**Interfaz de usuario con Streamlit**: Ofrece una interfaz interactiva y amigable, donde los usuarios pueden enviar preguntas y obtener respuestas del chatbot. Se utiliza st.chat_input() para la entrada del usuario y st.chat_message() para mostrar los mensajes, con avatares personalizados para el usuario y el chatbot.

**Manejo de múltiples documentos**: Los textos utilizados por el chatbot son leídos desde archivos locales (DOCUMENTOS/RESUMEN MANUAL GARANTIAS.txt y DOCUMENTOS/Resumen GPT.txt), procesados y usados para generar respuestas relevantes.
