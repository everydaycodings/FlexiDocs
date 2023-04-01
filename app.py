import streamlit as st
from helper import update_secondary_col, ConvertPdfToX, ConvertImageToPdf, ConvertImageToImage
from io import BytesIO


imagetopdf = ["jpg", "png", "jpeg"]
imagetoimage_primary = ["jpg", "png", "jpeg"]
imagetoimage_secondry = ["jpg", "png", "jpeg"]

st.header("Convert your files from one format to another: ")


col1, col2 = st.columns(2)

with col1:
    primary_format = st.selectbox("Select the format of your file: ", options=["jpg", "jpeg", "png", "pdf"])
with col2:
    secondary_format = st.selectbox("Select the format you want to convert your file: ", options=update_secondary_col(primary_col=primary_format))

if primary_format == "pdf":
    uploaded_files = st.file_uploader("Choose a file")
elif primary_format in imagetopdf and secondary_format in ["pdf"]:
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
elif primary_format in imagetoimage_primary and secondary_format in imagetoimage_secondry:
    uploaded_files = st.file_uploader("Choose a file")

submitted = st.button("Convert")


if submitted:

    if uploaded_files is not None:
        
        if primary_format == "pdf":
            with st.spinner("Converting..."):
                pdf_bytes = BytesIO(uploaded_files.read()).getvalue()
                file_name =  str(uploaded_files.name).split(".")[0]
                ConvertPdfToX().convert(secondary_format=secondary_format, pdf_bytes=pdf_bytes, pdf_filename=file_name)
            
        elif primary_format in imagetopdf and secondary_format in ["pdf"]:
            ConvertImageToPdf().convert(uploaded_files=uploaded_files)

        
        elif primary_format in imagetoimage_primary and secondary_format in imagetoimage_secondry:
            ConvertImageToImage().convert(secondary_format, uploaded_files)