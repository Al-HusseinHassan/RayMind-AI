import config
import streamlit as st
import tempfile
import os
from chatbot.agents.llm_response_generator.generator import final_generation

os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

st.set_page_config(
    page_title="RayMind AI",
    page_icon="🫁",
    layout="centered"
)

st.title("🫁 RayMind AI")
st.caption("Your AI assistant for respiratory health information.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "Hussein"

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input with integrated image attachment
prompt = st.chat_input(
    "Ask RayMind AI...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
    key="raymind_chat"
)

if prompt:

    user_query = prompt.text
    uploaded_files = prompt.files
    uploaded_image = uploaded_files[0] if uploaded_files else None

    if not user_query:
        st.warning("Please enter your question.")

    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)

            if uploaded_image:
                st.image(uploaded_image, width=250)

        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        image_path = None

        # Save uploaded image temporarily
        if uploaded_image:
            suffix = os.path.splitext(uploaded_image.name)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:
                temp_file.write(uploaded_image.getvalue())
                image_path = temp_file.name

        try:
            with st.chat_message("assistant"):

                response = final_generation(
                    image_path=image_path,
                    query=user_query,
                    thread_id=st.session_state.thread_id
                )

                full_response = st.write_stream(response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        finally:
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
