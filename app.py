import os
import openai
import streamlit as st
from dotenv import load_dotenv
# from render import bot_msg_container_html_template, user_msg_container_html_template
from render import *
# from utils import semantic_search
from utils import *
import prompts
from pinecone import Pinecone
# import pinecone

load_dotenv()



# --- SET PAGE CONFIG --- # 
st.set_page_config(page_title="MarcLouGPT", page_icon=":zap:")



# Set up OpenAI API key
# openai.api_key = st.secrets["OPENAI_API_KEY"]
# pinecone.init(api_key=st.secrets["PINECONE_API_KEY"], environment=st.secrets["PINECONE_ENVIRONMENT"])
# index = pinecone.Index(st.secrets["PINECONE_INDEX_NAME"])

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))

# pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


# index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

col1, col2 = st.columns([1,3])

col1.write("")
col1.image(
            "assets/Marc_Louvion.png",
            # Manually Adjust the width of the image as per requirement
        )
col2.header("⚡ MarcLouGPT")
# col2.write("Bonjour, je suis MarcLouGPT, une IA entraînée sur la doc' de ShipFa.st & les derniers articles de ma Newsletter dédiée à mon quotidien d'IndieDev. Posez-moi vos questions, et je ferai de mon mieux pour y répondre en vous fournissant les liens de resources pertinentes pour approfondir le sujet.")

with col2:
    col1, col2 = st.columns([1,100])
    col2.write("Hey there ! I'm MarcLouGPT, your go-to AI buddy trained on ShipFast docs and the latest insights from my IndieDev newsletter. Got a burning question? Fire away, and I'll do my best to give you answers while hooking you up with relevant resources to dive deeper into the topic ;) !")

st.caption("---")


# Define chat history storage
if "history" not in st.session_state:
    st.session_state.history = []

# Construct messages from chat history
def construct_messages(history):
    messages = [{"role": "system", "content": prompts.system_message}]
    
    for entry in history:
        role = "user" if entry["is_user"] else "assistant"
        messages.append({"role": role, "content": entry["message"]})
    
    return messages

# Generate response to user prompt
def generate_response():
    st.session_state.history.append({
        "message": st.session_state.prompt,
        "is_user": True,
    })
    

    print(f"Query: {st.session_state.prompt}")
    # sources = []  # New list to store source titles
    unique_sources = set()  # Use a set to store unique source titles

    # Perform semantic search and format results
    search_results = semantic_search(st.session_state.prompt, index, top_k=3)

    print(f"Results: {search_results}")

    context = ""
    for i, (title, transcript, source) in enumerate(search_results):
        context += f"Snippet from: {title}\n {transcript}\n\n"
        # sources.append(source)  # Store source titles in the list
        unique_sources.add(source)  # Add unique source urls to the set

    # Generate human prompt template and convert to API message format
    query_with_context = prompts.human_template.format(query=st.session_state.prompt, context=context)

    # Convert chat history to a list of messages
    messages = construct_messages(st.session_state.history)
    messages.append({"role": "user", "content": query_with_context})

    # Run the LLMChain
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    print(messages)

    # Parse response
    bot_response = response["choices"][0]["message"]["content"]

    # Add source titles to the bot response
    sources_text = "Source(s): " + ", <br>".join(unique_sources)
    bot_response_with_sources = bot_response + "\n\n <br>" + sources_text

    st.session_state.history.append({
        "message": bot_response_with_sources,
        "is_user": False
    })

    st.session_state.prompt = ''


# Display chat history
for message in st.session_state.history:
    if message["is_user"]:
        st.write(user_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
    else:
        st.write(bot_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)

# User input prompt
# st.write("")
user_prompt = st.text_input("",
                            # ":orange[Écrivez votre message :]",
                            key="prompt",
                            placeholder="Write your message...",
                            on_change=generate_response,
                            
                            )

# col1, col2 = st.columns([0.52, 0.5])
# col2.caption(":gray[©️ 2024 Copyright [Mathieu Bekkaye](https://mathieubk-personalwebsite.streamlit.app) - All rights reserved.]")

st.markdown("<div style='text-align: right; color: #83858C; font-size:14px;'>&copy; 2024 Copyright <a href='https://mathieubk-personalwebsite.streamlit.app'>Mathieu Bekkaye</a> - All rights reserved.</div>", unsafe_allow_html=True)


with open('./styles/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


