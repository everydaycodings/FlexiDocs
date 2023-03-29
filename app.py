import streamlit as st
from helper import update_secondary_col, ConvertPdfToX, ConvertImageToPdf
from io import BytesIO

st.header("Convert your files from one format to another: ")


col1, col2 = st.columns(2)

with col1:
    primary_format = st.selectbox("Select the format of your file: ", options=["jpg", "png", "pdf"])
with col2:
    secondary_format = st.selectbox("Select the format you want to convert your file: ", options=update_secondary_col(primary_col=primary_format))

if primary_format == "pdf":
    uploaded_files = st.file_uploader("Choose a file")
else:
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

submitted = st.button("Convert")


if submitted:

    if uploaded_files is not None:
        
        if primary_format == "pdf":
            with st.spinner("Converting..."):
                pdf_bytes = BytesIO(uploaded_files.read()).getvalue()
                file_name =  str(uploaded_files.name).split(".")[0]
                ConvertPdfToX().convert(secondary_format=secondary_format, pdf_bytes=pdf_bytes, pdf_filename=file_name)
            
        else:
            ConvertImageToPdf().convert(uploaded_files=uploaded_files)