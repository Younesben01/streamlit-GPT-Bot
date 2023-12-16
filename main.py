import os
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from textblob import TextBlob

def init():
    load_dotenv()
    st.set_page_config(
        page_title="Your own ChatGPT",
    )

def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "":
        st.error("OPENAI_API_KEY is not set. Please set it in your environment variables.")
        st.stop()
    return api_key

def initialize_chat():
    return ChatOpenAI(temperature=0)

def get_user_input():
    return st.text_input("Your message: ", key="user_input", placeholder="How are you feeling today?")

def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    if sentiment_score > 0:
        return "positive"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"

def enhance_response(response, sentiment):
    # Modify this function to enhance the AI responses based on sentiment or context
    # For simplicity, let's just capitalize the response if it's a positive sentiment
    if sentiment == "positive":
        return response.upper()
    else:
        return response

def provide_resource():
    # Example function to provide a resource
    resource = "Here's a relaxation exercise you might find helpful: [Link to exercise]"
    st.session_state.messages.append(AIMessage(content=resource))

def handle_user_input(chat, user_input):
    if user_input:
        # Analyze sentiment
        sentiment = analyze_sentiment(user_input)

        # Get AI response
        response = chat(st.session_state.messages)

        # Enhance the AI response based on sentiment
        enhanced_response = enhance_response(response.content, sentiment)

        # Concatenate user input and enhanced AI response
        combined_response = f"{user_input} {enhanced_response}"

        # Add combined message to the session state
        st.session_state.messages.append(HumanMessage(content=combined_response))

        # Example: Provide a resource if the user expresses a need for support
        if sentiment == "negative":
            provide_resource()


def display_messages(messages):
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=f"{i}_user")
        else:
            message(msg.content, is_user=False, key=f"{i}_ai")

def main():
    init()

    chat = initialize_chat()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="Hello! I'm your AI therapist. How can I help you today?")
        ]

    st.header("Your AI Therapist")

    with st.sidebar:
        user_input = get_user_input()
        handle_user_input(chat, user_input)

    display_messages(st.session_state.get("messages", []))

if __name__ == "__main__":
    main()







