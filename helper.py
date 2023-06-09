import os
import zipfile
import tempfile
from pdf2image import convert_from_bytes
import streamlit as st
import base64
from datetime import datetime
import img2pdf
from PIL import Image
from moviepy.editor import VideoFileClip



def update_secondary_col(primary_col):
    video_format = ["mp4", "mov", "mkv", "gif"]

    if primary_col in video_format:
        video_format.remove(primary_col)
        return video_format

    else:
        secondary_format_list = ["jpg", "jpeg", "png", "pdf"]

        secondary_format_list.remove(primary_col)

        return secondary_format_list


def download_button(encoded, file_name):

    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d_%H_%M_%S")

    st.markdown(
                    f"""
                    <a href="data:application/zip;base64,{encoded}" download="{file_name}_{formatted_date_time}.zip">
                        <h3>Download</h3>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )


def video_to_video(uploaded_files, secondary_format):

    with tempfile.TemporaryDirectory() as temp_dir:

        for uploaded_file in uploaded_files:
            asset_path = os.path.join(temp_dir, str(uploaded_file.name).split(".")[0])

            with open(asset_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

                videoClip = VideoFileClip(asset_path)

                if secondary_format == "gif":
                    videoClip.write_gif("{}/{}.{}".format(temp_dir, str(uploaded_file.name).split(".")[0], secondary_format))
                else:
                    videoClip.write_videofile("{}/{}.{}".format(temp_dir, str(uploaded_file.name).split(".")[0], secondary_format), codec='libx264')
        
        gif_list = [file for file in os.listdir(temp_dir) if file.endswith('.{}'.format(secondary_format))]
        zip_path = os.path.join(temp_dir, "gif_files.zip")

        with zipfile.ZipFile(zip_path, 'w') as zip:
            for gif_file in gif_list:
                if gif_file.endswith('.{}'.format(secondary_format)):
                    zip.write(os.path.join(temp_dir, gif_file))
        
        with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

        download_button(encoded=encoded, file_name="gif_images")




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

            download_button(encoded=encoded, file_name="images")


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

            download_button(encoded=encoded, file_name="pdf")


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

            download_button(encoded=encoded, file_name="converted_images")


class Resizer:

    def __init__(self) -> None:
        pass
    
    def percentage_resize_details(self, percentage_value, uploaded_file):

        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            img_path = os.path.join(temp_dir, uploaded_file.name)

            img = Image.open(img_path)

            width, height = img.size

            new_width = int(width * (percentage_value/100))
            new_height = int(height * (percentage_value/100))

            return new_height, new_width
        

    def percentage_resizing(self, percentage_value, uploaded_file):

        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            img_path = os.path.join(temp_dir, uploaded_file.name)

            img = Image.open(img_path)

            width, height = img.size

            new_width = int(width * (percentage_value/100))
            new_height = int(height * (percentage_value/100))

            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img_format = str(uploaded_file.name).split(".")[-1]
            img.save("{}/resized.{}".format(temp_dir, img_format))

            zip_path = os.path.join(temp_dir, "images.zip")
            image_path = os.path.join(temp_dir, "resized.{}".format(img_format))
            with zipfile.ZipFile(zip_path, "w") as zip:
                zip.write(image_path,  "resized.{}".format(img_format))
            
            with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            download_button(encoded=encoded, file_name="resizedimages")
    

    def image_dimensions(self, uploaded_file):

        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            img_path = os.path.join(temp_dir, uploaded_file.name)

            img = Image.open(img_path)

            width, height = img.size

            return width, height
        

    def dimension_resizing(self, height, width, uploaded_file):

        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            img_path = os.path.join(temp_dir, uploaded_file.name)

            img = Image.open(img_path)

            new_width = width
            new_height = height

            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img_format = str(uploaded_file.name).split(".")[-1]
            img.save("{}/resized.{}".format(temp_dir, img_format))

            zip_path = os.path.join(temp_dir, "images.zip")
            image_path = os.path.join(temp_dir, "resized.{}".format(img_format))
            with zipfile.ZipFile(zip_path, "w") as zip:
                zip.write(image_path,  "resized.{}".format(img_format))
            
            with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            download_button(encoded=encoded, file_name="resizedimages")

    
    def image_size_resizing_check(self, uploaded_file, image_size, size_format):

        mb_threshold = 1024 * 1024 

        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            file_size = os.path.getsize("{}/{}".format(temp_dir, uploaded_file.name))
            size_kb = int(file_size / 1024)

            if size_format == "MB":
                kb = int(image_size * 1024)
            else:
                kb = int(image_size)
            
            if kb > size_kb:
                st.error("Your Original image size is {}kb so you cannot resize the image to {}kb.".format(size_kb, kb))

                return False
            else:
                return True


    def image_size_resizing(self, uploaded_file, image_size, size_format):

        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            img = Image.open("{}/{}".format(temp_dir, uploaded_file.name))

            # Define the target file size in bytes (50KB)
            if size_format == "KB":
                target_size = image_size * 1024
            else:
                target_size = image_size * 1024 * 1024

            # Loop until the target size is reached
            while True:
                # Resize the image to half of its original size
                width, height = img.size
                img = img.resize((width // 2, height // 2), Image.ANTIALIAS)
                
                # Compress the image to a PNG file
                image_path = "{}/output.{}".format(temp_dir, str(uploaded_file.name).split(".")[-1])
                img.save(image_path, optimize=True)
                
                # Check the file size
                if os.path.getsize(image_path) <= target_size:
                    break

            # Save the final image
            img_format = str(uploaded_file.name).split(".")[-1]
            img.save("{}/resized.{}".format(temp_dir,img_format ))

            zip_path = os.path.join(temp_dir, "images.zip")
            image_path = os.path.join(temp_dir, "resized.{}".format(img_format))
            with zipfile.ZipFile(zip_path, "w") as zip:
                zip.write(image_path,  "resized.{}".format(img_format))
            
            with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            download_button(encoded=encoded, file_name="resizedimages")