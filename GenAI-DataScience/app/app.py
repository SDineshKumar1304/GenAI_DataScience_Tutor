import streamlit as st
import google.generativeai as genai
import base64

st.title("GenAI DataScience Tutor🤖💕")

@st.cache_data(persist=True)
def getImageAsBase64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = getImageAsBase64("C:\\Users\\veluk\\Downloads\\GenAI-DataScience\\download.png")
st.markdown(f"""
  <style>
    [data-testid="stAppViewContainer"]{{
      background-image: url("data: image/png;base64,{img}");
      background-size: cover;
    }}
    .stApp h1, .stApp div[data-baseweb="card"] > div > div > div > div > div > div, .stApp div[class^="main"] > div > div > div > div > div > div > div {{
      color: #000000 !important;
    }}
  </style>""",unsafe_allow_html=True)

with open("C:\\Users\\veluk\\Downloads\\GenAI-DataScience\\app\\keys\\instructions.txt") as f:
    instructions = f.read()

with open("C:\\Users\\veluk\\Downloads\\GenAI-DataScience\\app\\keys\\geminiapikey.txt") as f:
    api_key = f.read()

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=instructions
)

if "memory" not in st.session_state:
    st.session_state["memory"] = []

chat = model.start_chat(history=st.session_state["memory"])

def show_chat_history(chat):
    for message in chat.history:
        sender = "AI" if message.role == "model" else "You"
        st.write(f"{sender}: {message.parts[0].text}")

st.write("Hi there! How can I assist you today?", unsafe_allow_html=True)
show_chat_history(chat)

user_input = st.text_input("You: ")

if st.button("Clear Chat"):
    st.session_state["memory"] = []
    st.experimental_rerun()

if user_input:
    st.write("You:", user_input)
    try:
        response = chat.send_message(user_input)
        for bot in response:
            st.write("AI:", bot.parts[0].text)
        st.session_state["memory"] = chat.history
    except genai.generation_types.StopCandidateException:
        st.write("AI: I'm sorry, I couldn't understand that. Can you please provide more specific information?")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
