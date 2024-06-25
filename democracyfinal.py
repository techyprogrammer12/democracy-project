#Imports modules
import openai
import streamlit as st
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator    

api_key = "Your API key here"

st.title("👨‍💻Hey there!💭James here mate")
st.write("""My name is James-the-Bot!💻 I can give you all the insights on the topic democracy!""")

#Checks if the keyword message is not present
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a perfect democrat and possess all the knowledge related to democracy. You are jovial and respond to all these complex democracy or political-related questions in a fun and engaging way so that a 14 or 15-year-old can understand the concepts. You are also a fantastic storyteller and can tell students engaging stories on democracy which should explain the student's basic concepts of elections, democracy, voting, and civic responsibility. Between the stories, you provide the user with at least 2 options to choose from, and the user's choice from those two options would change the outcome of the story. You love doing this, asking questions between stories and getting the user's reply and then according to their reply, you like to continue the left part of the story."}
    ]

#Creates a sidebar for the language selection
selected_user_language = st.sidebar.selectbox("Select Bot Language", options=["English", "French", "Hindi", "Japanese", "Arabic"])
if selected_user_language:
    #Function for translating text
    def new_translate_text(text, target_language):
        try:
            translated_text = GoogleTranslator(source='auto', target=target_language[:2].lower()).translate(text)
            return translated_text
        except Exception as e:
            return f"Translation error: {e}"
    
    #Function for adding speech to the bot according to the required speed

    def adjust_speed(text, speed=1.0):
        new_speed = gTTS(text, lang=selected_user_language[:2].lower())
        audio_bytes = BytesIO() #Creates a file format for storing the audio data
        new_speed.speed = speed
        new_speed.write_to_fp(audio_bytes)
        audio_bytes.seek(0) #Restarts the audio file from the starting
        return audio_bytes

    # Checks if the user has input any query
    if prompt := st.text_input("You:", key="user_input"):
        openai.api_key = api_key
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages + [{"role": "user", "content": prompt}]
        )

        #Gets the first response by the story bot.
        new_message = response.choices[0].message
        #Translates that response in the desiresd user language
        story_segment = new_translate_text(new_message.content, selected_user_language)
        #Creates a text box for the story bot's response
        st.text_area("James:", value=story_segment, key="assistant_response")

        speed = st.slider("Speech Speed", min_value=0.5, max_value=2.0, step=0.1, value=1.0)
        adjusted_audio_bytes = adjust_speed(story_segment, speed)

        #Displays the adjusted audio in a mp3 or audio format for the users to listen
        st.audio(adjusted_audio_bytes, format="audio/mp3")

