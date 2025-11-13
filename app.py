# app.py  (versión mínima para probar que todo funciona)
import streamlit as st

# Config básica de la página
st.set_page_config(
    page_title="Smart Form",
    page_icon="🧪",
    layout="wide",
)

st.title("Smart Form — primer test")
st.write("Si ves este mensaje, tu app Streamlit está funcionando correctamente. 🎉")

st.markdown("---")
st.subheader("¿Qué sigue?")
st.write(
    "- En la barra lateral pondremos configuraciones (tolerancia, n° de preguntas, API key...).\n"
    "- Aquí en el cuerpo vamos a crear las pestañas de Matemáticas, Física, Química y Pruebate.\n"
    "- Después conectamos todo con tu motor de Formulator en Python."
)
