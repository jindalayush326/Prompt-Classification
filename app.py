import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found. Please add it to the .env file.")
else:
    st.set_page_config(page_title="Define Category")
    st.header("Find the category")

    chat = ChatOpenAI(temperature=0.5, openai_api_key=openai_api_key)

    if 'flowmessages' not in st.session_state:
        st.session_state['flowmessages'] = [
            SystemMessage(content="You are an AI assistant that classifies user prompts into categories.")
        ]

    def get_chatmodel_response(question):
        st.session_state['flowmessages'].append(HumanMessage(content=question))
        answer = chat(st.session_state['flowmessages'])
        st.session_state['flowmessages'].append(AIMessage(content=answer.content))
        return answer.content

    input = st.text_input("Input: ", key="input")

    submit = st.button("Ask the question")

    if submit:
        response = get_chatmodel_response(input)
        st.subheader("The Response is")
        st.write(response)
