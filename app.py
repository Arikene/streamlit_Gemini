import streamlit as st
from api_calling import note_generator #importing func/method from api_calling.py file 
from api_calling import audio_transcription, quiz_generator
from PIL import Image
from gtts import gTTS
import re

st.title("Note Summary and Quiz Generator", anchor=False)
st.markdown("Upload upto 3 images to generate Note summury and Quizzes")

st.divider()

with st.sidebar:
    st.header('Controls')
    images = st.file_uploader(
        "Upload photos of your notes (up to 3)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
pil_images = []
if images:
    # pil_image = Image.open(images) #This is only for single image, we will need to loop through the images if we want to use multiple images
    for image in images:
        pil_image = Image.open(image)
        pil_images.append(pil_image)

if pil_images:
    if len(pil_images) > 3:
            st.warning("Please upload a maximum of 3 images.")
    else:
            st.subheader("Uploaded Images") 

            col = st.columns(len(pil_images))   

            

            for i, image in enumerate(pil_images):
                with col[i]:
                    st.image(image, caption=f"Uploaded Image {i+1}")

    #difficulty
    selected = st.selectbox(
        "Enter the difficulty level of the quiz",
        options=["Easy", "Medium", "Hard"], index = None

    )                    
       
#Cleaning Text for speech

def clean_text_for_audio(text):
    text = re.sub(r'#+' , '', text)
    text = re.sub(r'(\*|_)+' , '', text)
    text = re.sub(r'`+' , '', text)

    # Convert bullet points to pauses
    text = re.sub(r'- ', '. ', text)

    # Normalize spacing
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

button = st.button("Generate Note Summary and Quiz",type="primary")


if button:
    if not pil_images:
        st.warning("Please upload at least one image to generate the note summary and quiz.")
    if not selected:
        st.warning("Please select a difficulty level for the quiz.")
    if pil_images and selected:

        #note
        with st.container(border=True): #using with, so that st.container contains what we write afterwards (like making a bracketless parameter)
            st.subheader("Your note",anchor=False)
            #the portion will be replaced by API Call

            with st.spinner("Generating note summary..."):

                generated_note = note_generator(pil_images)
                st.markdown(generated_note)


        #audio transcript
        with st.container(border=True): #using with, so that st.container contains what we write afterwards (like making a bracketless parameter)
            st.subheader("Your note",anchor=False)
            #the portion will be replaced by API Call
            with st.spinner("Generating audio transcription..."):
                cleaned_note = clean_text_for_audio(generated_note)
                audio_buffer = audio_transcription(cleaned_note)
                st.audio(audio_buffer)

        #Quiz
        with st.container(border=True): #using with, so that st.container contains what we write afterwards (like making a bracketless parameter)
            st.subheader("Your note",anchor=False)
            #the portion will be replaced by API Call
            with st.spinner("Generating quiz..."):
             quizzes = quiz_generator(pil_images[0], selected)
             st.markdown(quizzes)
            



    

