import PIL
import streamlit as st
from api_call import audio_transcription, note_generator, quiz_generator
from PIL import Image


st.title("Summary Generator of Handwritten Notes and Quiz Generator")
st.markdown("Upload upto 3 images of handwritten notes and get a summary of the content along with a quiz to test your understanding.")
st.divider()


with st.sidebar:
    st.header("Controls")
    images = st.file_uploader("Upload your notes",
                     type=["jpg","png","jpeg","heic"],
                     accept_multiple_files=True,)
    
    pil_images = []
    for img in images:
        pil_img = PIL.Image.open(img)
        pil_images.append(pil_img)


    if images:
        if len(images) > 3:
            st.error("Please upload a maximum of 3 images.")
        else:
            col = st.columns(len(images))

            st.subheader("Uploaded Images")

            for i, image in enumerate(images):
                with col[i]:
                    st.image(image)
    

    #Difficulty
    
    selected_option = st.selectbox("Select the difficulty of quiz",
                 ("Easy", "Medium", "Hard"),
                 index=None)
    
    if selected_option:
        st.markdown(f"You have selected: **{selected_option}**")
    else:
        st.error("Please select a difficulty level for the quiz.")

    pressed = st.button("Generate Summary and Quiz", type="primary")

if pressed:
    if not images:
        st.error("You must upload at least one image")
    if not selected_option:
        st.error("You must select a difficulty level")
    if images and selected_option:
        #note:

        with st.container(border=True):
            st.subheader("Summary of Notes")

            with st.spinner("Generating notes..."):

                summary = note_generator(pil_images)
                st.markdown(summary)



        #Audio Transcript:
        with st.container(border=True):
            st.subheader("Audio Transcript")

            with st.spinner("Generating audio transcript..."):

                #Clearing Markdowns
                summary = summary.replace("#", "")
                summary = summary.replace("*", "")
                summary = summary.replace("-", "")

                audio_transcript = audio_transcription(summary)
                st.audio(audio_transcript)


        #Quiz:
        with st.container(border=True):
            st.subheader(f"Quiz {selected_option} Difficulty")
            with st.spinner("Generating quiz..."):

                quizzes = quiz_generator(pil_images, selected_option)
                st.markdown(quizzes)
