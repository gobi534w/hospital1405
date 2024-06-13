import streamlit as st
import pandas as pd
import altair as alt

# Title and description
st.title("ANUSHA'S POSTINGS DETAILS")
st.write("HISTORY OF PATIENTS.")

# Hospital details (you can customize these fields as needed)
st.header("PATIENT Details")
st.write("Name: Dhanalakshmi srinivasan Hospital")
st.write("Location: Samayapuram tollplaza, Trichy, India")
st.write("Contact: 7200077663")

# File upload
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("Uploaded Data:")
    st.write(df)
    
    # Ensure the Excel file has the necessary columns
    required_columns = ["sno", "name", "details", "disease", "contact", "date", "increasing"]
    if all(column in df.columns for column in required_columns):
        st.write("Excel file contains the required columns.")
        
        # Convert 'date' column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculate percentage increase or decrease in health
        df['change'] = df.groupby(['name', 'disease'])['increasing'].transform(lambda x: x.diff().fillna(0))
        df['percentage_change'] = df['change'] * 100
        
        # Group by patient and disease to track the progression
        patient_disease_progression = df.groupby(['name', 'disease', 'date']).agg({'percentage_change': 'sum'}).reset_index()
        
        # Select patient name
        patient_name = st.selectbox("Select Patient Name", df['name'].unique())
        
        # Filter data for selected patient
        patient_data = patient_disease_progression[patient_disease_progression['name'] == patient_name]
        
        if not patient_data.empty:
            # Create a chart using Altair for the selected patient
            chart = alt.Chart(patient_data).mark_line().encode(
                x='date:T',
                y='percentage_change:Q',
                color='disease:N',
                tooltip=['name', 'disease', 'date', 'percentage_change']
            ).interactive().properties(
                title=f'Health Progression for {patient_name} Over Time',
                width=800,
                height=400
            )
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No data available for the selected patient.")
        
    else:
        st.error(f"The Excel file must contain the following columns: {', '.join(required_columns)}")
