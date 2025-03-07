import streamlit as st
import random

st.set_page_config(page_title="Tuyết Hương xin đẹp", layout="wide")

# Sidebar để tải file lên
with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Chọn file (doc, docx, pdf, txt)", type=["doc", "docx", "pdf", "txt"])
    if uploaded_file:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
    # Nút reset lịch sử chat
    if st.button("Reset Chat"):
        st.session_state["messages"] = []

# Tiêu đề luôn hiển thị
st.markdown("<h1 style='text-align: center;'>💬 Tuyết Hương xin đẹp</h1>", unsafe_allow_html=True)


# Vùng chat cố định
chat_container = st.container()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Hiển thị lịch sử chat
with chat_container:
    for message in st.session_state["messages"]:
        st.chat_message("user" if message["role"] == "user" else "assistant").write(message["content"])

#debug
a = 1
# Ô nhập tin nhắn
user_input = st.text_input("Nhập câu hỏi...", key=f"feedback_{a}'")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with chat_container:
        st.chat_message("user").write(user_input)
    
    # Giả lập phản hồi từ chatbot
    response = "Xin lỗi, tôi không hiểu câu hỏi của bạn."  # Thay bằng chatbot thực tế của bạn
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with chat_container:
        st.chat_message("assistant").write(response)
    
    st.write (a) 
