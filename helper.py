import os
import zipfile
import tempfile
from pdf2image import convert_from_bytes
import streamlit as st
import base64
from datetime import datetime
import img2pdf
from PIL import Image

def update_secondary_col(primary_col):

    secondary_format_list = ["jpg", "jpeg", "png", "pdf"]

    secondary_format_list.remove(primary_col)

    return secondary_format_list



class ConvertPdfToX:

    def __init__(self):
        pass


    def convert(self, secondary_format, pdf_bytes, pdf_filename):

        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_bytes(pdf_bytes, output_folder=path,output_file="{}".format(pdf_filename), fmt=secondary_format)

            zip_path = os.path.join(path, "images.zip")
            with zipfile.ZipFile(zip_path, "w") as zip:
                for filename in os.listdir(path):
                    if filename.endswith(".{}".format(secondary_format)):
                        zip.write(os.path.join(path, filename), filename)
            
            with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            now = datetime.now()
            formatted_date_time = now.strftime("%Y-%m-%d_%H_%M_%S")

            st.markdown(
                    f"""
                    <a href="data:application/zip;base64,{encoded}" download="images_{formatted_date_time}.zip">
                        <h3>Download Images</h3>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )


class ConvertImageToPdf:

    def __init__(self) -> None:
        pass

    def convert(self, uploaded_files):

        with tempfile.TemporaryDirectory() as temp_dir:

            for uploaded_file in uploaded_files:
                with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            img_list = os.listdir(temp_dir)
            img_list = ["{}/".format(temp_dir) + x for x in img_list]

            with open("{}/output.pdf".format(temp_dir),"wb") as f:
                f.write(img2pdf.convert(img_list))


            zip_path = os.path.join(temp_dir, "pdf.zip")
            with zipfile.ZipFile(zip_path, "w") as zip:
                zip.write("{}/output.pdf".format(temp_dir))
            
            with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            now = datetime.now()
            formatted_date_time = now.strftime("%Y-%m-%d_%H_%M_%S")

            st.markdown(
                    f"""
                    <a href="data:application/zip;base64,{encoded}" download="pdf_{formatted_date_time}.zip">
                        <h3>Download PDF</h3>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )


class ConvertImageToImage:

    def __init__(self) -> None:
        pass

    def convert(self, secondary_format, uploaded_file):

        if secondary_format == "jpg":
            secondary_format = "jpeg"

        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            img_path = os.path.join(temp_dir, uploaded_file.name)
            save_image_path = "{}/{}.{}".format(temp_dir, str(uploaded_file.name).split(".")[0], secondary_format)

            img = Image.open(img_path)
            rgb_img = img.convert("RGB")
            rgb_img.save(save_image_path, str(secondary_format).upper())

            zip_path = os.path.join(temp_dir, "images.zip")
            with zipfile.ZipFile(zip_path, "w") as zip:
                zip.write(save_image_path,  "{}.{}".format(str(uploaded_file.name).split(".")[0], secondary_format))
            
            with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            now = datetime.now()
            formatted_date_time = now.strftime("%Y-%m-%d_%H_%M_%S")

            st.markdown(
                    f"""
                    <a href="data:application/zip;base64,{encoded}" download="converted_images_{formatted_date_time}.zip">
                        <h3>Download Images</h3>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )
                