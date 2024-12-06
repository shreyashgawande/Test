import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pillow_heif  # Enable HEIC support in Pillow
from googletrans import Translator
import os
import warnings
warnings.filterwarnings("ignore")
# Ensure pillow-heif is registered
pillow_heif.register_heif_opener()

def convert_to_marathi(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='mr')
    return translation.text\
    
 #File uploader for HEIC image
# uploaded_file = st.file_uploader("Upload a HEIC image", type=["heic", "HEIC"])
def writing_part():
    uploaded_file = "IMG_2.HEIC"
    packet_file = "IMG_1.HEIC"
    if uploaded_file and  st.session_state.marathi_text :


        with st.spinner("Processing image..."):
            # Load the HEIC image
            img = Image.open(uploaded_file)
            img = img.convert("RGB")  # Convert HEIC to RGB for editing

            # Create a drawing object
            draw = ImageDraw.Draw(img)

            # Define font properties
            #font_path = r"C:\Users\SHREYASH\AppData\Local\Microsoft\Windows\Fonts\\NotoSansDevanagari-Black.ttf"
            font_path = r"NotoSansDevanagari-Black.ttf"
            font_size = 45
            position = (2400, 455)  # Adjust based on image dimensions
            text_color = (128, 65, 85)  # Color of the text

            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                st.error("Font file not found. Using default font.")
                font = ImageFont.load_default()
            
            print(st.session_state.marathi_text)
            # Add Marathi text to the image
            draw.text(position, st.session_state.marathi_text, font=font, fill=text_color)

            img1 = Image.open(packet_file)
            img1 = img1.convert("RGB")  # Convert HEIC to RGB for editing

            # Create a drawing object
            draw1 = ImageDraw.Draw(img1)
            packet_name_position = (1145, 2091)
            packet_villege_position = (1145, 2291)
            font1 = ImageFont.truetype(font_path, 80)

            draw1.text(packet_name_position, st.session_state.marathi_text, font=font1, fill=text_color)
            draw1.text(packet_villege_position, st.session_state.villege_text, font=font1, fill=text_color)

            # Display the resulting image
            st.image(img, caption="Image with Marathi Text", use_column_width=True)
            st.image(img1, caption="Image with Marathi Text", use_column_width=True)

            # Option to download the modified image
            if st.session_state.input_text:
                output_path = st.session_state.input_text+"_invitation.pdf"
            else :
                output_path = st.session_state.marathi_text+"_invitation.pdf"
            images = [img1, img]  # Replace img1 and img2 with your actual image objects

            images[0].save(
                output_path,
                "PDF",
                save_all=True,
                append_images=images[1:]  # Append all other images
            )
            # img.save(output_path,"PDF")
            # img.save("Output.pdf","PDF")
            with open(output_path, "rb") as file:
                btn = st.download_button(
                    label="Download invitation pdf",
                    data=file,
                    file_name=output_path,
                    mime="application/pdf"
                )
            
            os.remove(output_path)  # Clean up the saved file


# Streamlit app
st.title("Invitaion card writer.")
if "input_text" not in st.session_state  :
    st.session_state.input_text = ""
if "marathi_text" not in st.session_state  :
    st.session_state.marathi_text = ""
if "villege_text" not in st.session_state  :
    st.session_state.villege_text = ""
if "villege" not in st.session_state  :
    st.session_state.villege = ""
if "not_coorrect_filter" not in st.session_state  :
    st.session_state.not_coorrect_filter = True
# Input for text


# if st.session_state.input_text:
if  st.session_state.not_coorrect_filter:
    st.session_state.input_text = st.text_input("Enter Name :")
    st.session_state.villege = st.text_input("Enter Villege :",key="dfs")

    if st.session_state.input_text and st.session_state.villege:
        st.session_state.marathi_text = convert_to_marathi(st.session_state.input_text)
        if len(st.session_state.villege.strip()):
            st.session_state.villege_text = convert_to_marathi(st.session_state.villege)

        st.write(f"Translated Name Text: {st.session_state.marathi_text}")
        st.write(f"Translated Villege Text: {st.session_state.villege_text}")
# correct_btn = st.button("Correct")
# if correct_btn :
        writing_part()
        not_coorrect_btn = st.button("Not Correct")
        if not_coorrect_btn:
            st.session_state.not_coorrect_filter = False
if not st.session_state.not_coorrect_filter:
   
        st.session_state.marathi_text = st.text_input("Enter Name Manually.")
        st.session_state.villege_text = st.text_input("Enter Villege Manually:",key="dfsd")
       
        submit_btn = st.button("Submit")
        if submit_btn : 
            writing_part()
            



