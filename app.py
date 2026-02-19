import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
from google import genai
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()
client = genai.Client(api_key=API_KEY)
def get_gemini_response(user_text, image: Image.Image):
    prompt = f"""
You are a professional civil engineer.
Analyze the given image and explain:
1. Type of structure
2. Structural system
3. Materials used
4. Construction technique
5. Engineering purpose
6. Safety or design features
User notes: {user_text if user_text else "Not provided"}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=[prompt, image]
    )
    return response.text
st.set_page_config(
    page_title="Civil Engineering Insight Studio",
    page_icon="🏗️",
    layout="wide"
)
st.title("🏗️ Civil Engineering Insight Studio")
st.write("Upload a civil engineering structure image to get AI-powered insights.")
user_text = st.text_input(
    "📝 Optional description",
    placeholder="Example: Bridge, building, dam, road..."
)
uploaded_file = st.file_uploader(
    "📷 Upload an image",
    type=["jpg", "jpeg", "png"]
)
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=700)
if st.button("Describe Structure"):
    try:
        if image is None:
            st.warning("⚠️ Please upload an image first.")
        else:
            with st.spinner("🔍 Analyzing structure..."):
                result = get_gemini_response(user_text, image)

            st.subheader("📊 Civil Engineering Analysis")
            st.markdown(result)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")