import streamlit as st
import pandas as pd 
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper",layout="wide")

#custom css
st.markdown(
"""
<style>
.stApp{
    background-color:white;
    color:black;
    }
</style>
""",
unsafe_allow_html=True
)
#title and description
st.title("✨Data Sweeper🌟")
st.write("Data Sweeper transform your files between CSV and Excel format with built in data cleaning.")

#file uploader
uploaded_files = st.file_uploader("Upload a file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:

        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format. Please upload a CSV or Excel file: {file_ext}")
            continue

#file details
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())

        #data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"clean data for {file.name}, key=f"viz_{file.name}"): 
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from the file {file.name}"): 
                    df.drop_duplicates(inplace=True)
                    st.write(f"Duplicate rows removed from {file.name}")

            with col2:
                if st.button(f"Fill missing values from the file {file.name}"): 
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write(f"Missing values filled from {file.name}") 

            st.subheader("Select Columns to keep")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]           
#data visualisation
st.subheader("Data Visualisation")
if st.checkbox(f"show visualization for {file.name}"):
    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

    # Conversion options

    st.subheader("Conversion Options")
    conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
    if st.button(f"Convert{file.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file.name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

        elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file.name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"Download {file.name} as {conversion_type}", 
                    data=buffer, 
                    file_name=file.name, 
                    mime=mime_type
                    )
                
                st.success("All files processed successfully")
