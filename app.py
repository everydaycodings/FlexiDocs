import streamlit as st
from helper import update_secondary_col, ConvertPdfToX, ConvertImageToPdf, ConvertImageToImage, Resizer
from io import BytesIO


imagetopdf = ["jpg", "png", "jpeg"]
imagetoimage_primary = ["jpg", "png", "jpeg"]
imagetoimage_secondry = ["jpg", "png", "jpeg"]

st.header("Welcome To FlexiDocs")

worker_option = st.selectbox("Selet the Option: ", options=["Resizer", "Convertor"])


if worker_option == "Resizer":

    st.subheader("Resize your Image as your wish")
    
    resizer_option = st.selectbox("Select your Prefered Resizer: ", options=["Percentage", "Dimensions", "Image Size"])

    uploaded_files = st.file_uploader("Choose a file")

    if uploaded_files is not None:

        if resizer_option == "Percentage":

            percenatge_value = st.number_input("Enter the Percentage you want to reduce to: ", min_value=1, max_value=100, step=1, value=70)
            
            height, width = Resizer().percentage_resize_details(uploaded_file=uploaded_files, percentage_value=percenatge_value)
            st.warning("You want to set the new size to be {}% of the original size which is {}*{}".format(percenatge_value, width, height))

            if st.button("Resize The Image"):
                Resizer().percentage_resizing(percentage_value=percenatge_value, uploaded_file=uploaded_files)

        
        elif resizer_option == "Dimensions":

            img_width, img_height = Resizer().image_dimensions(uploaded_files)

            height = st.number_input("Enter the new Height of the image: ", min_value=1, max_value=img_height, step=1, value=int(img_height*50/100))
            width = st.number_input("Enter the new Width of the image: ", min_value=1, max_value=img_width, step=1, value=int(img_width*50/100))

            if st.button("Resize The Image"):
                Resizer().dimension_resizing(height=height, width=width, uploaded_file=uploaded_files)
    

        elif resizer_option == "Image Size":
            
            col1, col2 = st.columns(2)
            with col1:
                image_size = st.number_input("Enter the size of the image you want to resize to: ", min_value=1, step=1)
            with col2:
                image_size_format = st.selectbox("Enter the Image size type: ", options=["KB", "MB"])
            
            check = Resizer().image_size_resizing_check(uploaded_file=uploaded_files, image_size=image_size, size_format=image_size_format)

            if check:

                if st.button("Resize Image"):
                    Resizer().image_size_resizing(uploaded_file=uploaded_files, image_size=image_size, size_format=image_size_format)



elif worker_option == "Convertor":


    st.subheader("Convert your files from one format to another: ")


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