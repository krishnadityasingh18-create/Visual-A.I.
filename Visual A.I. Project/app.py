import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="Flux Vision AI", page_icon="🎨")

# 1. Accessing the Free Model
# You will get this API URL from Hugging Face
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

def generate_image(prompt, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=120)
    return response.content

# 2. Building the Interface
st.title("🎨 Flux.1 High-Res Generator")
st.write("Generate professional-grade images for free.")

# Sidebar for API Key and Settings
with st.sidebar:
    st.header("Setup")
    hf_token = st.text_input("Hugging Face Token", type="password", help="Get it free at hf.co/settings/tokens")

# Main Prompt Area
prompt = st.text_area("What do you want to see?", placeholder="A futuristic city in the style of cyberpunk, 8k, cinematic...")

if st.button("🚀 Generate Image"):
    if not hf_token:
        st.error("Please enter your Hugging Face Token in the sidebar!")
    elif not prompt:
        st.warning("Please enter a description.")
    else:
        with st.spinner("The AI is thinking..."):
            try:
                image_raw = generate_image(prompt, hf_token)
            except requests.RequestException:
                st.error("Could not reach Hugging Face. Check your internet connection and try again.")
                st.stop()
            try:
                img = Image.open(io.BytesIO(image_raw))
                st.image(img, use_container_width=True)
                
                # Download logic
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 Download Image", buf.getvalue(), "generated.png", "image/png")
            except:
                st.error("The API is busy or the token is incorrect. Try again in 30 seconds.")