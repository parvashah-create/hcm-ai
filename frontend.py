from openai import OpenAI
import streamlit as st

# Sidebar for API key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Title of the Streamlit app
st.title("🥦⚕️ Health and Wellness Chatbot") 

# Initialize messages in session state if not already present
if "messages" not in st.session_state:
    system_prompt = {
        "role": "system",
        "content": (
            "You are a health and wellness advisor with expertise in nutrition, exercise, stress management, and chronic condition management. "
            "Your goal is to provide helpful, accurate, and supportive advice to individuals seeking to improve their overall health and wellness. "
            "Always ensure your responses are clear, concise, and tailored to the user's specific needs and preferences. "
            "The user is a vegetarian who avoids high sodium and high sugar foods, regularly consumes fruits, vegetables, and whole grains, "
            "and exercises regularly. They are managing hypertension and prediabetes. Tailor your advice accordingly."
        )
    }
    st.session_state["messages"] = [system_prompt, {"role": "assistant", "content": "How can I help you?"}]

# Display messages in the chat
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    # Append user's message to session state
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"]
    )
    
    msg = response.choices[0].message

    # Append assistant's response to session state
    st.session_state["messages"].append({"role": msg.role, "content": msg.content})
    st.chat_message(msg.role).write(msg.content)
