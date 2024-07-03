import streamlit as st
import openai

def generate_central_text(topic, api_key, model):
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": "Eres un asistente que escribe textos en español."},
        {"role": "user", "content": f"Genera un texto de 300 palabras sobre el tema: {topic}"}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=600,
        temperature=0.5
    )
    central_text = response.choices[0].message['content'].strip()
    return central_text

def generate_instagram_post(text, api_key, prompt_template, model):
    openai.api_key = api_key
    prompt = prompt_template.format(text=text)
    
    messages = [
        {"role": "system", "content": "Eres un asistente que escribe publicaciones para Instagram en español de 100 palabras."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=300,
        temperature=0.5
    )
    post = response.choices[0].message['content'].strip()
    return post

def generate_linkedin_post(text, api_key, prompt_template, model):
    openai.api_key = api_key
    prompt = prompt_template.format(text=text)
    
    messages = [
        {"role": "system", "content": "Eres un asistente que escribe publicaciones para LinkedIn en español de 300 palabras."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=600,
        temperature=0.5
    )
    post = response.choices[0].message['content'].strip()
    return post

def generate_image(prompt, api_key):
    openai.api_key = api_key
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

st.set_page_config(
    page_title="Generador de textos y publicaciones"
)
st.title("Genera un texto y publicaciones")

# Variables de estado
if 'central_text' not in st.session_state:
    st.session_state.central_text = ""
if 'topic_input' not in st.session_state:
    st.session_state.topic_input = ""
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""
if 'model' not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"
if 'instagram_prompt_template' not in st.session_state:
    st.session_state.instagram_prompt_template = (
        "Usa el siguiente texto para crear una publicación atractiva para Instagram. "
        "El texto debe acabar con una pregunta para generar interacción. "
        "Debe enfatizar algún aspecto de la foto y usar emoticonos. "
        "Incluye al menos 10 hashtags: 5 específicos del nicho y 5 generales para viralizar.\n\n{text}\n\n"
    )
if 'linkedin_prompt_template' not in st.session_state:
    st.session_state.linkedin_prompt_template = (
        "Usa el siguiente texto para crear una publicación profesional para LinkedIn de 300 palabras. "
        "Redacción sencilla. Haz un breve resumen del post y luego incluye un bullet list de 3 elementos "
        "resumiendo los puntos clave del post, con salto de línea. El tema es:\n\n{text}\n\n"
    )

# Navegación por pestañas
tab1, tab2 = st.tabs(["Generador de Publicaciones", "Configuración"])

with tab1:
    # Paso 1: Generar texto central
    if st.session_state.step == 1:
        topic_input = st.text_input("Introduce el tema para generar el texto central")

        if topic_input:
            with st.form("text_generation_form", clear_on_submit=True):
                submitted = st.form_submit_button("Generar Texto")
                if submitted and st.session_state.openai_api_key.startswith("sk-"):
                    st.session_state.topic_input = topic_input
                    central_text = generate_central_text(topic_input, st.session_state.openai_api_key, st.session_state.model)
                    st.session_state.central_text = central_text
                    st.session_state.step = 2

    # Paso 2: Mostrar texto central y opciones para generar publicación
    if st.session_state.step == 2:
        st.write("### Texto Central Generado")
        st.write(st.session_state.central_text)
        continue_option = st.button("Continuar")
        if continue_option:
            st.session_state.step = 3

    # Paso 3: Generar publicación para la plataforma seleccionada
    if st.session_state.step == 3:
        st.write("### Texto Central Generado")
        st.write(st.session_state.central_text)
        with st.form("post_generation_form", clear_on_submit=True):
            platforms = st.multiselect("Selecciona la(s) plataforma(s) para la publicación", ["Instagram", "LinkedIn"])
            generate_post_button = st.form_submit_button("Generar Publicación")
            if generate_post_button and platforms:
                for platform in platforms:
                    if platform == "Instagram":
                        post_text = generate_instagram_post(
                            st.session_state.central_text, 
                            st.session_state.openai_api_key, 
                            st.session_state.instagram_prompt_template, 
                            st.session_state.model
                        )
                    elif platform == "LinkedIn":
                        post_text = generate_linkedin_post(
                            st.session_state.central_text, 
                            st.session_state.openai_api_key, 
                            st.session_state.linkedin_prompt_template, 
                            st.session_state.model
                        )
                    st.success(f"Publicación para {platform}:")
                    st.write(post_text)

        # Opción para generar imagen
        st.write("### Generar Imagen")
        image_prompt_option = st.radio("Seleccione cómo desea generar la imagen", ("Usar el tema inicial", "Ingresar un prompt personalizado"))
        
        if image_prompt_option == "Usar el tema inicial":
            image_prompt = st.session_state.topic_input
        else:
            image_prompt = st.text_input("Introduce el prompt para la imagen")

        generate_image_button = st.button("Generar Imagen")
        if generate_image_button and image_prompt:
            image_url = generate_image(image_prompt, st.session_state.openai_api_key)
            st.image(image_url, caption="Imagen Generada por DALL-E")

with tab2:
    st.write("### Configuración de Templates y Modelo")
    st.session_state.openai_api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.openai_api_key)
    st.session_state.model = st.selectbox("Selecciona el modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"], index=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"].index(st.session_state.model))
    
    st.session_state.instagram_prompt_template = st.text_area(
        "Template para Instagram",
        st.session_state.instagram_prompt_template,
        height=200
    )
    st.session_state.linkedin_prompt_template = st.text_area(
        "Template para LinkedIn",
        st.session_state.linkedin_prompt_template,
        height=200
    )
