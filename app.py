import os
import streamlit as st
import base64
from openai import OpenAI

# 🌸 CONFIG GIRLY 🌸
st.set_page_config(
    page_title="💖 Analisis Girly de Imagen 💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 💅 ESTILOS
st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#ffe6f0 0%,#ffd6ec 50%,#ffe0f5 100%);}
h1{text-align:center;color:#ff4da6;text-shadow:0px 0px 10px rgba(255,105,180,0.4);}
.stButton>button{background:linear-gradient(90deg,#ff66b2,#ff99cc);color:white;border-radius:15px;border:none;font-weight:bold;box-shadow:0 4px 10px rgba(255,105,180,0.3);}
.stButton>button:hover{background:linear-gradient(90deg,#ff3385,#ff80bf);transform:scale(1.05);}
textarea,input{border-radius:10px!important;border:1px solid #ffb3d9!important;}
[data-testid="stFileUploader"]{background:#fff0f6;border-radius:15px;padding:10px;border:1px solid #ffb3d9;}
[data-testid="stExpander"]{background:#fff0f6;border-radius:15px;border:1px solid #ffb3d9;}
</style>
""", unsafe_allow_html=True)

# 🌸 Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


# 💖 TITULO
st.title("💖 Análisis de Imagen Girly 🤖🏞️✨")

ke = st.text_input('🔑 Ingresa tu clave secreta (shhh 💅)')
os.environ['OPENAI_API_KEY'] = ke

# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("📸 Sube tu imagen bonita", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    with st.expander("💖 Vista previa de tu imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Toggle for showing additional details input
show_details = st.toggle("✨ Preguntar algo específico sobre la imagen", value=False)

if show_details:
    additional_details = st.text_area(
        "💭 Cuéntame más contexto:",
        disabled=not show_details
    )

# Button to trigger the analysis
analyze_button = st.button("💅 Analizar imagen", type="secondary")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("✨ Analizando con magia IA..."):
        # Encode the image
        base64_image = encode_image(uploaded_file)
    
        prompt_text = ("Describe lo que ves en la imagen en español de forma linda y clara 💖")
    
        if show_details and additional_details:
            prompt_text += (
                f"\n\nContexto adicional del usuario:\n{additional_details}"
            )
    
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]
    
        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown("💖 " + full_response + "▌")
            
            message_placeholder.markdown("💖 " + full_response)
    
        except Exception as e:
            st.error(f"💔 Ups ocurrió un error: {e}")

else:
    if not uploaded_file and analyze_button:
        st.warning("📸 Sube una imagen primero, bestie 💖")
    if not api_key:
        st.warning("🔑 No olvides tu API key 💅")
