import streamlit as st
from dotenv import load_dotenv

load_dotenv(".env.local")

from utils.orchestrator import Orchesterator


st.set_page_config(
    page_title="AURA AI",
    page_icon="🌱",
    layout="centered",
)

st.title("AURA AI")
st.caption("AI-powered crop diagnostics using rules, sensors, and knowledge base")


# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "farm_id" not in st.session_state:
    st.session_state.farm_id = None

# Fram connectivity 
with st.sidebar:
    st.header("Farm Connection")

    connect_farm = st.toggle("Connect farm sensors")

    if connect_farm:
        st.session_state.farm_id = st.selectbox(
            "Select Farm",
            [
                "farm_101",
                "farm_102",
                "farm_103",
                "farm_104",
                "farm_105",
                "farm_106",
                "farm_107",
                "farm_108",
            ],
        )
        st.success(f"Connected to {st.session_state.farm_id}")
    else:
        st.session_state.farm_id = None
        st.info("Using knowledge base only (Level 1)")


# Rendering chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask about your crops...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing crop conditions..."):
            try:
                if st.session_state.farm_id:
                    answer = Orchesterator.answer_level_2(
                        user_input,
                        farm_id=st.session_state.farm_id,
                    )
                else:
                    answer = Orchesterator.answer_level_1(user_input)

                st.markdown(answer)

            except Exception as e:
                st.error("Something went wrong while generating the response.")
                st.exception(e)
                answer = "Unable to generate response."

    st.session_state.messages.append({"role": "assistant", "content": answer})
