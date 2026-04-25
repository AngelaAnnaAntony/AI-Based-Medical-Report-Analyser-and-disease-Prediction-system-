import streamlit as st
import re
import base64
from modules.database import create_tables
from modules.authenticate import signup_user, login_user, reset_password, get_user_by_email
from modules.report_reader import extract_text
from modules.data_extraction import extract_medical_values, detect_report_type
from modules.disease_detection import detect_diseases, extract_patient_details
from modules.ai_disease_detection import detect_diseases_ai
from modules.pdf_generator import generate_pdf
from modules.Whatsapp_share import generate_whatsapp_link
from streamlit_folium import st_folium
import folium
import urllib.parse
import pandas as pd
create_tables()

# BACKGROUND IMAGE
def add_bg():
    with open("background.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        /* remove default padding */
        .block-container {{
            padding-top: 10rem;
        }}
        /* background image */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        /* main title */
        .main-title {{
            text-align:center;
            font-size:28px;
            font-weight:bold;
            color:#0b5394;
            margin-bottom:10px;
        }}
        .title {{
            text-align:center;
            color:#0b5394;
            margin-bottom:20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# VALIDATIONS 
def valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.(com|in|org)$'
    return re.match(pattern, email)
def strong_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_#^])[A-Za-z\d@$!%*?&_#^]{6,15}$'
    return re.match(pattern, password)

# SESSION
if "page" not in st.session_state:
    st.session_state.page = "login"

# LOGIN PAGE 
def login_page():
    add_bg()
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-title'>AI-Based Medical Report Analyser and Disease Prediction System</div>",
        unsafe_allow_html=True
    )
    st.markdown("<h3 class='title'>Login Page</h3>", unsafe_allow_html=True)
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if not user:
            existing_user = get_user_by_email(email)
            if existing_user and not login_user(email, password):
                st.error("Invalid password")
            elif not existing_user:
                st.error("You are not registered! sign up first.")
            else:
                st.error("Invalid Email ID or Password.")
        else:
            st.success("You have logged in successfully.")
            st.session_state.username = user[3]
            st.session_state.fullname = user[1]
            st.session_state.page = "home"
            st.rerun()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()
    with col2:
        if st.button("Forgot Password"):
            st.session_state.page = "reset"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# SIGNUP PAGE 
def signup_page():
    add_bg()
    st.markdown(
    "<div class='main-title'>AI-Based Medical Report Analyser and Disease Prediction System</div>",
    unsafe_allow_html=True
    )
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='title'>Sign Up</h2>", unsafe_allow_html=True)
    name = st.text_input("Full Name")
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if not valid_email(email):
            st.error("Enter the correct email ID according to the correct email format (eg., abcd@gmail.com)")
        elif not strong_password(password):
            st.error("Enter strong password (eg., Ac3%_wT34^)")
        elif password != confirm:
            st.error("The password entered does not match with the confirm password")
        else:
            success = signup_user(name, email, email, password)
            if success:
                st.success("You are registered successfully")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("This Email ID already exists.")
    if st.button("Login Page"):
        st.session_state.page = "login"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# RESET PASSWORD
def reset_page():
    add_bg()
    st.markdown(
    "<div class='main-title'>AI-Based Medical Report Analyser and Disease Prediction System</div>",
    unsafe_allow_html=True
    )
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='title'>Forgot Password</h2>", unsafe_allow_html=True)
    email = st.text_input("Email ID")
    new_pass = st.text_input("New Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    if st.button("Update Password"):
        user = get_user_by_email(email)
        if not user:
            st.error("You are not registered! sign up first.")
        elif not strong_password(new_pass):
            st.error("Enter strong password (eg., Ac3%_wT34^)")
        elif new_pass != confirm:
            st.error("The new password entered does not match with the confirm password")
        else:
            updated = reset_password(email, new_pass)
            if updated:
                st.success("Updated password successfully.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Not able to update the password.")
    st.markdown("</div>", unsafe_allow_html=True)

# HOME PAGE 
def home_page():
    add_bg()
    st.markdown(
    "<div class='main-title'>AI-Based Medical Report Analyser and Disease Prediction System</div>",
    unsafe_allow_html=True
    )
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 class='title'>Welcome {st.session_state.fullname}</h3>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Medical Report",
        type=["pdf","png","jpg","jpeg"]
    )
    if uploaded_file:
        if uploaded_file.type not in [
            "application/pdf",
            "image/png",
            "image/jpeg"
        ]:
            st.error("Add PDF, JPEG or PNG reports only.")
        else:
            st.success("File uploaded successfully.")
            text=extract_text(uploaded_file)
            name, age, gender = extract_patient_details(text)
            if isinstance(name, tuple):
                name = name[0]
            patient_name = name if name else st.session_state.fullname            
            age=age if age else "N/A"
            gender= gender if gender else "N/A"
            tab1, tab2, tab3=st.tabs(["Data Extraction", "Analysis & Recommendations", "Doctors near me"])
            with tab1:
              st.subheader("Extracted Text")
              st.text(text)
              values= extract_medical_values(text)
              report_types=detect_report_type(text)
              st.subheader("Detected Report Type")
              st.write(report_types)
              st.subheader("Extracted Medical Values")
              st.write(values)

            with tab2:
              from modules.ai_disease_detection import detect_diseases_ai
              rule_results = detect_diseases(values, report_types)
              ai_results = detect_diseases_ai(values)
              results = rule_results + ai_results
              st.subheader("Disease Detection Result")
              df=pd.DataFrame(results)
              st.table(df)
              st.write("---")
              st.subheader("📍 Find a Doctor Near You")
            with tab3:
            # 1. Ask for the user's location
              user_city = st.text_input("Enter your City/Area to find specialists:", placeholder="e.g., Ghaziabad, Delhi, Mumbai")

              if user_city:
             # 2. Get the unique doctor types from our results
             # Example: If results show "Jaundice", doctor_types will have "Gastroenterologist"
                doctor_types = list(set([res['Doctor'] for res in results]))

                for doctor in doctor_types:
                    st.write(f"### Finding {doctor}s in {user_city}...")
        
                    # 3. Create a Google Maps Search Link
                    search_query = f"{doctor} near {user_city}"
                    encoded_query = urllib.parse.quote(search_query)
                    google_maps_url = f"https://www.google.com/maps/search/{encoded_query}"
                    
                    # 4. Display a simple map placeholder (centered roughly)
                    # In a real app, we'd use GPS, but for now, we show a helpful link!
                    st.markdown(f"""
                        <div style="padding:10px; border-radius:10px; background-color:#e1f5fe; border-left: 5px solid #0288d1;">
                            <strong>Action Required:</strong> Click the button below to see the best-rated <b>{doctor}s</b> in <b>{user_city}</b>.
                        </div>
                        <br>
                        <a href="{google_maps_url}" target="_blank">
                            <button style="background-color:#4285F4; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">
                                📍 Open Google Maps for {doctor}
                            </button>
                        </a>
                    """, unsafe_allow_html=True)
                    st.write("")   
        st.warning("""
            ⚠️ Medical Disclaimer:

            This system is an AI-based medical report analyzer designed for educational purposes only. 
            The results provided are not a medical diagnosis and should not be considered as professional medical advice. 

            Please consult a qualified doctor or healthcare professional for accurate diagnosis and treatment.
            """)
        pdf_file=generate_pdf(
                results, 
                patient_name=patient_name,
                age=age,
                gender=gender,
                report_types=report_types
            )
        with open(pdf_file, "rb")as file:
                st.download_button(
                label="Download Result as PDF", data=file, file_name="medical_result.pdf", mime="application/pdf"
                )

        whatsapp_link = generate_whatsapp_link()
        st.markdown(
        f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="
            background-color:#25D366;
            color:white;
            padding:10px;
            border:none;
            border-radius:5px;
            font-size:16px;
            cursor:pointer;">
            Share via WhatsApp
            </button>
        </a>
        """,unsafe_allow_html=True)

    if st.button("Logout"):
       st.session_state.page = "login"
       st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

#  NAVIGATION 
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "reset":
    reset_page()
elif st.session_state.page == "home":
    home_page()