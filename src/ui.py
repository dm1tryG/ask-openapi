import streamlit as st

from chat import chat_with_model

st.title("Ask your API.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    if (len(st.session_state.messages)):
        r = chat_with_model(st.session_state.messages[-1]["content"])
        response = st.write(r)
        st.session_state.messages.append({"role": "assistant", "content": response})