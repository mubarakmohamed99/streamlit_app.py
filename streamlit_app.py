import streamlit as st

st.set_page_config(page_title="Reinsurance Claim Assistant", layout="wide")

st.title("💬 Reinsurance Claim Assistant (Chat Demo)")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me about a claim, policy, or upload a file..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mock AI reply
    reply = f"🤖 This is a demo response to: **{prompt}**\n\n👉 Later, I’ll fetch from documents, rules, or email API."
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# File uploader inside chat
uploaded_files = st.file_uploader("📂 Upload supporting documents", type=["pdf", "docx", "txt"], accept_multiple_files=True)
if uploaded_files:
    for f in uploaded_files:
        st.success(f"✅ Uploaded file: {f.name} (not processed yet).")
