import streamlit as st
import pandas as pd
import bcrypt
import os
from datetime import datetime
import base64
import re

# Streamlit page configuration
st.set_page_config(page_title="Infosys Dataset Analysis Application", page_icon="📊", layout="wide")

# Simulated user database
if "user_db" not in st.session_state:
    st.session_state.user_db = {}  # Store emails and hashed passwords

# Track the authenticated user
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

# Track the page view
if "page" not in st.session_state:
    st.session_state.page = "landing"

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Function to verify passwords
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)

# Function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Function to validate password strength
def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

# Function to handle signup
def signup(email, password, confirm_password):
    if email in st.session_state.user_db:
        st.error("Email already registered. Please log in.")
        return False
    if password != confirm_password:
        st.error("Passwords do not match.")
        return False
    st.session_state.user_db[email] = hash_password(password)
    st.success("Sign up successful! Please log in to continue.")
    return True

# Function to handle login
def login(email, password):
    if email in st.session_state.user_db:
        if verify_password(password, st.session_state.user_db[email]):
            st.session_state.authenticated_user = email
            st.success(f"Welcome, {email}!")
            st.session_state.page = "main"
            return True
        else:
            st.error("Incorrect password. Please try again.")
    else:
        st.error("Email not registered. Please sign up first.")
    return False

# Display app logo or images
def check_and_display_image(file_path, caption):
    if os.path.exists(file_path):
        st.image(file_path, caption=caption, use_column_width=True)
    else:
        st.warning(f"Image not found: {file_path}")

# Header with user info
def display_header():
    st.markdown(
        """
        <style>
        .header {
            background-color:rgb(231, 105, 26);
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            font-size: 24px;
            color:rgb(58, 197, 224);
            font-family: 'Roboto', helvetica;
        }
        </style>
        <div class="header">
            📊 <b>Infosys Dataset Analysis</b>
        </div>
        """,
        unsafe_allow_html=True
    )

# Apply background image using custom CSS
def add_background_image(image_file):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/png;base64,{image_file}) no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to encode image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Replace 'pexels.jpg' with your image file path
image_path = "pexels.jpg"
if os.path.exists(image_path):
    image_base64 = get_base64_image(image_path)
    add_background_image(image_base64)
else:
    st.warning("Background image not found.")

# Function to handle chatbot responses
def chatbot_response(user_input):
    responses = {
       "hey": "Hello! How can I assist you today?",
        "how are you": "I'm just a bot, but I'm here to help you!",
        "who are you": "I am a chatbot designed to assist you with Infosys Dataset Analysis.",
        "hello": "Hi there! How can I help you?",
        "help": "Sure! What do you need help with?",
        "what is your name": "I am called InfosysBot, your data analysis assistant!",
        "what can you do": "I can help you analyze datasets, answer questions, and provide insights related to Infosys.",
        "bye": "Goodbye! Have a great day ahead!",
        "thank you": "You're welcome! Let me know if you need anything else.",
        "what is infosys": "Infosys is a global leader in consulting, technology, and outsourcing solutions.",
        "tell me a joke": "Why don’t scientists trust atoms? Because they make up everything!",
        "how does this work": "Simply type in your question, and I'll do my best to assist you based on my knowledge!",
        "what is data analysis": "Data analysis is the process of inspecting, cleaning, and modeling data to discover useful information and support decision-making.",
        "what is ai": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn."
    
    }
    return responses.get(user_input.lower(), "I'm not sure how to respond to that.")

# Custom CSS for futuristic style
st.markdown(
    """
    <style>
    .main {
        background-color: rgba(34, 47, 62, 0.9); /* Dark bluish-gray */
        color: rgb(255, 255, 255); /* White text for contrast */
        font-family: 'Roboto', helvetica;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    .stButton button {
        background: linear-gradient(135deg, rgb(33, 147, 176), rgb(109, 213, 237)); /* Gradient background */
        color: white; /* White text */
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: transform 0.2s ease, background-color 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, rgb(109, 213, 237), rgb(33, 147, 176)); /* Reversed gradient on hover */
        transform: scale(1.05); /* Slight zoom on hover */
    }
    .stTextInput > div > input {
        border: 1px solid rgb(109, 213, 237); /* Light blue border */
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        color: rgb(255, 255, 255); /* White text */
        background-color: rgba(34, 47, 62, 0.8); /* Semi-transparent dark background */
        transition: border 0.3s ease, box-shadow 0.3s ease;
    }
    .stTextInput > div > input:focus {
        border: 1px solid rgb(33, 147, 176); /* Brighter blue on focus */
        box-shadow: 0 0 5px rgb(109, 213, 237); /* Glow effect on focus */
    }
    .stSidebar {
        background: linear-gradient(135deg, rgb(72, 61, 139), rgb(33, 147, 176)); /* Sidebar gradient */
        color: rgb(255, 255, 255); /* White text */
    }
    .stSidebar .stButton button {
        background: linear-gradient(135deg, rgb(109, 213, 237), rgb(33, 147, 176)); /* Button gradient in sidebar */
        color: white; /* White text */
    }
    .stSidebar .stButton button:hover {
        background: linear-gradient(135deg, rgb(33, 147, 176), rgb(109, 213, 237)); /* Reversed gradient on hover */
    }
    .start-button {
        display: flex;
        justify-content: center;
    }
    .start-button button {
        background: linear-gradient(135deg, rgb(144, 238, 144), rgb(72, 209, 204)); /* Fresh green to teal gradient */
        color: white !important;
        font-size: 18px !important;
        padding: 15px 30px !important;
        border-radius: 10px !important;
        border: none;
        cursor: pointer;
        transition: transform 0.2s ease, background-color 0.3s ease;
    }
    .start-button button:hover {
        background: linear-gradient(135deg, rgb(72, 209, 204), rgb(144, 238, 144)); /* Reversed gradient on hover */
        transform: scale(1.05); /* Slight zoom on hover */
    }
    .auth-bar {
        background-color: rgb(33, 147, 176);
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        font-size: 24px;
        color: white;
        font-family: 'Roboto', helvetica;
        margin-bottom: 20px;
    }
    .auth-button {
        background: linear-gradient(135deg, rgb(33, 147, 176), rgb(109, 213, 237)); /* Gradient background */
        color: white;
        border-radius: 10px;
        border: none;
        padding: 15px 30px;
        font-size: 16px;
        cursor: pointer;
        transition: transform 0.2s ease, background-color 0.3s ease;
        display: block;
        width: 100%;
        margin-bottom: 10px;
    }
    .auth-button:hover {
        background: linear-gradient(135deg, rgb(109, 213, 237), rgb(33, 147, 176)); /* Reversed gradient on hover */
        transform: scale(1.05); /* Slight zoom on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to show the landing page
def show_landing_page():
    st.markdown(
        """
        <div style='text-align:center; padding: 50px; background-color: rgb(0, 0, 0, 0.7); border-radius: 10px; margin: 100px auto; width: 50%;'>
            <h1 style='color: #00d4ff;'>Welcome to Infosys Dataset AQI Analysis Application</h1>
            <p style='color: #00d4ff;'>Analyze Infosys AQI datasets with interactive visualizations and filters.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="start-button">', unsafe_allow_html=True)
    if st.button("Start"):
        st.session_state.page = "auth"
    st.markdown('</div>', unsafe_allow_html=True)

# Function to show the authentication page
def show_auth_page():
    st.markdown('<div class="auth-bar">Authentication</div>', unsafe_allow_html=True)
    st.markdown('<div class="main">', unsafe_allow_html=True)
    auth_choice = st.radio("Choose Action", ["Sign Up", "Login"])

    if auth_choice == "Sign Up":
        email = st.text_input("Enter your email", key="signup_email")
        password = st.text_input("Choose a password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm your password", type="password", key="signup_confirm_password")
        if st.button("Sign Up", key="signup_button", help="Click to Sign Up"):
            if email and password and confirm_password:
                signup(email, password, confirm_password)
            else:
                st.warning("Please fill out all fields.")
    elif auth_choice == "Login":
        email = st.text_input("Enter your email", key="login_email")
        password = st.text_input("Enter your password", type="password", key="login_password")
        if st.button("Login", key="login_button", help="Click to Login"):
            if email and password:
                login(email, password)
            else:
                st.warning("Please fill out all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

# Main Application
def show_main_app():
    display_header()

    with st.expander("About the Application"):
     st.write("""
**Infosys Dataset Analysis App**

This Infosys Dataset Analysis App is a Streamlit-based web application designed for interactive analysis and visualization of Infosys datasets. The app includes user authentication, dataset filtering, and data visualization features, along with a chatbot and feedback system to enhance the user experience.

### Key Features:

#### Landing Page:
- Welcomes the user with a styled landing interface.
- Provides an option to start the application.

#### Authentication System:
- **Sign Up**: Users can create accounts with email and password.  
    - Password validation includes length, alphanumeric content, and special character requirements.
- **Login**: Users log in using their registered email and password.
- **Session Management**: Tracks user authentication status in the session.

#### Main Dashboard:
- **Header and Styling**: Features a visually appealing header and background with custom CSS.
- **About Section**: Describes the app's purpose and functionality.
- **Power BI Integration**: Embeds an interactive Power BI dashboard for air pollution data visualization.
- **Dataset Overview**:
    - Displays dataset columns and sample data.
- **Filtering**:
    - Filter data by StationId, Date, and AQI values.
    - Interactive sidebar sliders and multiselect for filtering.
- **Filtered Data Display**:
    - Shows the filtered dataset in a tabular format.

#### Chatbot:
- Offers predefined responses to user queries.
- Enhances interactivity and engagement.

#### Feedback Mechanism:
- Allows users to provide feedback or suggestions.
- Displays a confirmation message upon submission.

#### Footer Section:
- Displays contact information and app attribution.
- Encourages user support and feedback.

#### Logout:
- Logs out the authenticated user and returns them to the landing page.
""")
   

    st.title("Air Pollution Dashboard")

    # Embed URL from Power BI
    embed_url = "https://app.powerbi.com/view?r=eyJrIjoiMGM3OWQxZTYtNTQxZS00YjM3LWFiZDktMzQwNWE3NDljZmIxIiwidCI6Ijg0MzlkMTkyLWY0NjQtNDFiYi05NDNiLWMzOTYzODI0NThiNCJ9"
    iframe = f"""
    <iframe 
        src="{embed_url}" 
        width="100%" 
        height="600" 
        frameborder="0" 
        allowFullScreen="true">
    </iframe>
    """
    st.markdown(iframe, unsafe_allow_html=True)

    # Load Excel dataset
    excel_file = "InfosysDataset-NEW.xlsx"
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)

        # Dataset Overview
        with st.expander("Dataset Overview"):
            st.subheader("Columns in the Dataset")
            st.write(df.columns.tolist())

            st.subheader("Sample Data")
            st.dataframe(df.head())

        # Filters
        st.sidebar.header("Filter the Data")

        # Station ID Filter
        all_station_ids = df['StationId'].unique().tolist()
        all_station_ids.insert(0, "Selectall")  # Add "Select All" option at the beginning

        selected_station_ids = st.sidebar.multiselect(
        "Select StationId(s)", 
         options=all_station_ids, 
         default="Selectall"
        )

# Filter the dataframe based on the selected StationId(s)
        if "Selectall" in selected_station_ids:
         filtered_station_df = df
        else:
         filtered_station_df = df[df['StationId'].isin(selected_station_ids)]


        # Date Filter
        start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime(df['Date'].min()))
        end_date = st.sidebar.date_input("End Date", value=pd.to_datetime(df['Date'].max()))

        # AQI Filter
        min_aqi = st.sidebar.slider("Minimum AQI", min_value=int(df['AQI'].min()), max_value=int(df['AQI'].max()), value=int(df['AQI'].min()))
        max_aqi = st.sidebar.slider("Maximum AQI", min_value=int(df['AQI'].min()), max_value=int(df['AQI'].max()), value=int(df['AQI'].max()))

        # Apply Filters
        filtered_df = df[
            
            (df['Date'] >= pd.to_datetime(start_date)) &
            (df['Date'] <= pd.to_datetime(end_date)) &
            (df['AQI'] >= min_aqi) &
            (df['AQI'] <= max_aqi)
        ]

        # Display Filtered Data
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

    else:
        st.error(f"Excel file not found: {excel_file}")

    # Chatbot Section
    st.markdown("---")
    st.header("Chatbot")
    user_input = st.text_input("Ask me anything:")
    if st.button("Send"):
        response = chatbot_response(user_input)
        st.write(response)


    st.markdown(
    """
    <div style="background-color: #2c3e50; color: white; text-align: center; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <p style="margin: 0; font-size: 18px; font-weight: bold;">We value your feedback!</p>
    </div>
    """,
    unsafe_allow_html=True
    ) 
    feedback = st.text_area("Your Feedback", placeholder="Let us know your thoughts or suggestions...")
    if st.button("Submit Feedback"):
     st.success("Thank you for your feedback!")
    
    
    st.write("If you need further assistance, please reach out to us at:")
    # Footer Section
    st.markdown(
    """
    <div style="background-color: #16a085; color: white; text-align: center; padding: 20px; border-radius: 10px; margin-top: 30px;">
        <p style="margin: 0; font-size: 16px; font-weight: bold;">Powered by Infosys Dataset Analysis App</p>
        <p style="margin: 0; font-size: 14px;">Contact us at 📧 <a href="mailto:support@example.com" style="color: #ecf0f1;">support@example.com</a></p>
    </div>
    """,
    unsafe_allow_html=True
    )

    # Logout Button
    if st.button("Logout"):
     logout()

  

# Authentication Workflow
# Function to logout
def logout():
    st.session_state.authenticated_user = None
# Authentication Workflow
if st.session_state.page == "landing":
    show_landing_page()
elif st.session_state.page == "auth":
    show_auth_page()
else:
    show_main_app()
