import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import google.generativeai as genai

# Retrieve the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the API with the key
genai.configure(api_key=GEMINI_API_KEY)

# Function to query the Gemini API
def query_gemini(prompt):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit app configuration
st.set_page_config(page_title="Disaster Management and Relief", layout="wide")
st.title("Disaster Management and Relief")

# Sidebar menu
st.sidebar.title("Menu")
menu_options = ["Upload Data", "View Reports", "Emergency Q&A", "Logistics Coordination", "Affected Areas"]
selected_option = st.sidebar.selectbox("Select an option", menu_options)

# Upload Data and Preprocess
if selected_option == "Upload Data":
    st.header("Upload and Analyze Disaster Data")
    uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

    if uploaded_file:
        # Display the raw data
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:")
        st.dataframe(data)
        
        # Query API for data preprocessing
        if st.button("Preprocess Data"):
            prompt = f"Preprocess the following disaster management data and suggest improvements: {data.head().to_string()}"
            preprocessing_result = query_gemini(prompt)
            
            st.write("Preprocessing Result:")
            st.write(preprocessing_result)

# View Reports
elif selected_option == "View Reports":
    st.header("View Generated Reports")
    report_type = st.selectbox("Select report type", ["Summary", "Detailed"])
    
    if st.button("Generate Report"):
        prompt = f"Generate a {report_type.lower()} report for disaster management and relief efforts. Include sections on current situation, resources needed, and next steps."
        report = query_gemini(prompt)
        st.write(f"{report_type} Report:")
        st.write(report)

# Emergency Q&A
elif selected_option == "Emergency Q&A":
    st.header("Emergency Procedures Q&A")
    user_question = st.text_input("Ask a question about emergency procedures")

    if st.button("Get Answer"):
        prompt = f"Answer the following question about emergency procedures in disaster management: {user_question}"
        answer = query_gemini(prompt)
        st.write("Answer:")
        st.write(answer)

# Logistics Coordination
elif selected_option == "Logistics Coordination":
    st.header("Coordinate Logistics")
    location = st.text_input("Enter location")
    resources_needed = st.text_area("Enter resources needed")

    if st.button("Coordinate"):
        prompt = f"Create a logistics coordination plan for disaster relief in {location} with the following resources needed: {resources_needed}. Include transportation, storage, and distribution considerations."
        coordination_plan = query_gemini(prompt)
        st.write("Coordination Plan:")
        st.write(coordination_plan)

# Affected Areas Graphical Representation
elif selected_option == "Affected Areas":
    st.header("Graphical Representation of Affected and Safe Areas")
    
    affected_areas = np.random.rand(10) * 100
    safe_areas = np.random.rand(10) * 100

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(range(10), affected_areas, color='red', label='Affected Areas')
    ax.barh(range(10), safe_areas, left=affected_areas, color='green', label='Safe Areas')
    ax.set_xlabel('Area (sq. km)')
    ax.set_ylabel('Regions')
    ax.legend()
    st.pyplot(fig)
