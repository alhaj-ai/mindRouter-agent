import streamlit as st
from main import graph
from langchain_core.messages import AIMessage, HumanMessage

st.set_page_config(page_title="MindRouter-Agent", page_icon="🤖", layout="centered")
st.title("🤖 MindRouter-Agent")
st.write("Smart LangGraph router that classifies messages as emotional or logical and responds with full conversation history.")

if "state" not in st.session_state:
    st.session_state.state = {"messages": [], "message_type": None}

user_input = st.text_input("Type your message here and press Enter:")

if user_input:
    st.session_state.state["messages"].append(HumanMessage(content=user_input))

    try:
        st.session_state.state = graph.invoke(st.session_state.state)

        last_reply = st.session_state.state.get("messages", [])[-1]
        if isinstance(last_reply, AIMessage):
            st.markdown(f"**Assistant ({st.session_state.state.get('message_type', 'routed')}):** {last_reply.content}")
        elif isinstance(last_reply, dict):
            role = last_reply.get("role", "")
            content = last_reply.get("content", "")
            if role == "assistant":
                st.markdown(f"**Assistant ({st.session_state.state.get('message_type', 'routed')}):** {content}")
    except Exception as e:
        st.error(f"Error: {e}")

if st.session_state.state.get("messages"):
    st.markdown("---")
    st.subheader("Conversation History")
    for msg in st.session_state.state["messages"]:
        if isinstance(msg, HumanMessage):
            st.markdown(f"**You:** {msg.content}")
        elif isinstance(msg, AIMessage):
            st.markdown(f"**Assistant:** {msg.content}")
        elif isinstance(msg, dict):
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                st.markdown(f"**You:** {content}")
            elif role == "assistant":
                st.markdown(f"**Assistant:** {content}")
