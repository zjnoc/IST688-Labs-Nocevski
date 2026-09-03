import streamlit as st
from openai import OpenAI
      

# Show title and description.
st.title("Document Summary")
st.write(
    "Upload a document below and select a summary type – GPT will summarize it for you! "
    
)

summary_type = st.sidebar.selectbox(
    "Summarize the document by:",
    ("in 100 words:", "in 2 connecting paragraphs", "in 5 bullet points")
)

use_advanced_model = st.sidebar.checkbox("Use advanced model")

model = "gpt-4.1" if use_advanced_model else "gpt-4.1-nano"



# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
OPENAI_API_KEY = st.secrets.OPEN_AI_KEY


    # Create an OpenAI client.
client = OpenAI(api_key=OPENAI_API_KEY)

    # Validate key
    # client.models.list()

    # Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )


if uploaded_file:

        # Process the uploaded file.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Summarize the following document {summary_type}: {document}",
            }
        ]



        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
