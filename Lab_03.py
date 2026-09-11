import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Chad the Chatbot")
st.write("Ask me anything and we can chat!")

OPENAI_API_KEY = st.secrets.OPEN_AI_KEY

# Create an OpenAI client.
client = OpenAI(api_key=OPENAI_API_KEY)



system_prompt = {
    "role": "system",
    "content": "Explain things simply, like to a 10 year old. Answer the "
                "question, then ask 'Do you want more info?' If they say yes, "
                "give more detail and ask again. If they say no, ask what else "
                "you can help with."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Keep the whole conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Get user input.
if prompt := st.chat_input("What would you like to ask?"):
    # Add user's message to chat history.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    # Generate an answer using the OpenAI API.
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
        model="gpt-4.1",
        messages=[system_prompt] + st.session_state.messages[-4:],
        stream=True,
    )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})