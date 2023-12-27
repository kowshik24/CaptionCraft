import streamlit as st
import sqlite3
import hashlib
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Database connection
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Create table
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, api_key TEXT)')

# Add user
def add_userdata(username, password, api_key):
    c.execute('INSERT INTO userstable(username, password, api_key) VALUES (?,?,?)', (username, password, api_key))
    conn.commit()

# Login user
def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

# Get API Key
def get_api_key(username):
    c.execute('SELECT api_key FROM userstable WHERE username =?', (username,))
    data = c.fetchone()
    return data[0] if data else None

# Hashing Passwords
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def main():
    """Simple Login App"""

    st.set_page_config(page_title="🎥CaptionCraft📱",
                       page_icon="✨", layout="centered", initial_sidebar_state="auto")

    #st.title("AI-powered Image Caption and Content Generator")

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("🎥CaptionCraft📱")
        st.info("🌟🎥CaptionCraft📱🌟 is an AI-powered Image Caption and Content Generator. It uses the power of Gemini to generate captions and content for your images. It can generate captions for images and also generate content for your social media posts. It can generate content for Facebook, Instagram, LinkedIn, Twitter and TikTok.")
        st.write("For more details of this repo please visit: https://github.com/kowshik24/CaptionCraft")
    elif choice == "Login":
        st.subheader("Login Section")
        st.info("🌟 CaptionCraft: Your AI-Powered Social Media Companion 📸🌈 Seamless Integration Across Platforms: Effortlessly generate platform-specific captions for Facebook 📘, Instagram 📸, LinkedIn 🔗, Twitter 🐦, and TikTok 🎵. Each caption is tailored to resonate with your audience, enhancing your social media presence.")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, hashed_pswd)
            if result:
                st.success("Hi! Welcome {} 🍃".format(username))
                
                # Load environment variables and configure the API
                api_key = get_api_key(username)
                genai.configure(api_key=api_key)

                # Rest of your Streamlit app goes here
                run_app()

            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        st.info("Don't have GOOGLE API KEY? Get one here: https://makersuite.google.com/app/apikey")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        new_api_key = st.text_input("Google API Key")

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password), new_api_key)
            st.success("You have successfully created an account")
            st.info("Go to Login Menu to login")

def run_app():
    # Function to load the model and get responses
    def get_gemini_response(input, image):
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input, image])
        return response.text

    # Streamlit app layout
    #st.set_page_config(page_title="🌟🎥CaptionCraft📱🌟",page_icon="✨", layout="centered", initial_sidebar_state="auto")
    
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
        "Facebook": ("📘", "Generate 5 different eye catchy a Facebook post use emojis and hastags for this image:"),
        "Instagram": ("📸", "Generate 5 different eye catchy a Instagram post use emojis and hastags for this image:"),
        "LinkedIn": ("🔗", "Generate 5 different eye catchy a LinkedIn post use emojis and hastags for this image:"),
        "Twitter": ("🐦", "#Trending #Tweet 📢 What should this image tweet say on Twitter?"),
        "TikTok": ("🎵", "#Fun #Viral 🎉 Generate 5 different catchy TikTok description for this image:")
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

if __name__ == '__main__':
    main()
