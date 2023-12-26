import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables and configure the API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the model and get responses
def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image])
    return response.text

# Streamlit app layout
st.set_page_config(page_title="🌟🎥CaptionCraft📱🌟",
                   page_icon="✨", layout="centered", initial_sidebar_state="auto")
st.header("🌈 AI-powered Image Caption and Content Generator 📸")

# Upload image
uploaded_file = st.file_uploader("🖼️ Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image 🌟", use_column_width=True)

# Custom user input
user_input = st.text_input("🔮 Custom Query (optional):", key="input")

# Platform-specific buttons with enhanced prompts
platforms = {
    "Facebook": ("📘", "Generate a eye catchy Facebook post use emojis and hastags for this image:"),
    "Instagram": ("📸", "Generate a eye catchy a Instagram post use emojis and hastags for this image:"),
    "LinkedIn": ("🔗", "Generate a eye catchy a LinkedIn post use emojis and hastags for this image:"),
    "Twitter": ("🐦", "#Trending #Tweet 📢 What should this image tweet say on Twitter?"),
    "TikTok": ("🎵", "#Fun #Viral 🎉 Generate a catchy TikTok description for this image:")
}

for platform_name, (icon, prompt) in platforms.items():
    if st.button(f"{icon} Generate for {platform_name}"):
        if image is not None:
            response = get_gemini_response(prompt, image)
            st.subheader(f"Response for {platform_name} 🚀")
            st.write(response)
        else:
            st.error("Please upload an image first 🚨")

# Custom input button
if st.button("🔍 Generate with Custom Query"):
    if image is not None and user_input:
        response = get_gemini_response(user_input, image)
        st.subheader("Response to Custom Query 🌐")
        st.write(response)
    else:
        st.error("Please upload an image and enter a custom query 🚨")


# Contact Form
with st.expander("Contact us"):
    with st.form(key='contact', clear_on_submit=True):
        
        email = st.text_input('Contact Email')
        st.text_area("Query",placeholder="Please fill in all the information or we may not be able to process your request")  
        
        submit_button = st.form_submit_button(label='Send Information')