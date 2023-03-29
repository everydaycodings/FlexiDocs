import streamlit as st
from helper import update_secondary_col, ConvertPdfToX
from io import BytesIO

st.header("Convert your files from one format to another: ")

with st.form("format-chooser"):
    col1, col2 = st.columns(2)

    with col1:
        primary_format = st.selectbox("Select the format of your file: ", options=["pdf", "png"])
    with col2:
        secondary_format = st.selectbox("Select the format you want to convert your file: ", options=update_secondary_col(primary_col=primary_format))
    
    uploaded_file = st.file_uploader("Choose a file") 

    submitted = st.form_submit_button("Convert")


if uploaded_file is not None:

    with st.spinner("Converting..."):
        pdf_bytes = BytesIO(uploaded_file.read()).getvalue()
        file_name =  str(uploaded_file.name).split(".")[0]
        ConvertPdfToX().convert(secondary_format=secondary_format, pdf_bytes=pdf_bytes, pdf_filename=file_name)