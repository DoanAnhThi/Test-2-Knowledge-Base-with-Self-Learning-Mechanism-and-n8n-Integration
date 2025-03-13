import streamlit as st
import random
import requests

# Webhook URL API - Test
question_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/chat-input-v2"     
feedback__API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/feedback-v2"     
upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/upload-document-v2" 

# # Webhook URL API - Publish
# question_API_URL = "https://bincalam28499.app.n8n.cloud/webhook/chat-input-v2"     
# feedback__API_URL = "https://bincalam28499.app.n8n.cloud/webhook/feedback-v2"     
# upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook/upload-document-v2" 

st.set_page_config(page_title="viACT Agent", layout="wide")


if "messages" not in st.session_state:
    st.session_state["messages"] = []

#GOM CUỘC HỒI THOẠI LẠI
# Tạo biến text chứa toàn bộ cuộc hội thoại
full_conversation = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])

# Sidebar để tải file lên
with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Upload your files (TXT, PDF, DOC or DOCX)", type=["doc", "docx", "pdf", "txt"])
    if uploaded_file:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        response = requests.post(upload_API_URL, data={'filename':uploaded_file.name,'filetype':uploaded_file.type,}, files ={'file': (uploaded_file.name, uploaded_file, uploaded_file.type)})
        st.write(file_details)
    # Nút reset lịch sử chat
    if st.button("New Chat"):
        response = requests.post(feedback__API_URL, json={'feedback_prompt':full_conversation})
        # full_conversation = 1 #đẩy đoạn đoạn này lên vectordatabase để mô hình học
        st.session_state["messages"] = []

# Tiêu đề luôn hiển thị
st.markdown("<h1 style='text-align: center;'>💬 viACT Agent</h1>", unsafe_allow_html=True)


# Vùng chat cố định
chat_container = st.container()



icon_user = "./icon/man1.png"
icon_bot="./icon/bot.png"
# Hiển thị lịch sử chat
with chat_container:
    for message in st.session_state["messages"]:
        st.chat_message(message["role"], avatar= icon_user if message["role"] == "user" else icon_bot).write(message["content"])
        # st.chat_message("user" if message["role"] == "user" else "ai").write(message["content"])

#debug
a = 1
# Ô nhập tin nhắn
user_input = st.chat_input("Your message...", key=f"feedback_{a}'")
if user_input:
    # Gửi question lên Webhook
    response = requests.post(question_API_URL, json={'question':user_input})
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with chat_container:
        st.chat_message("user",avatar= icon_user ).write(user_input)
    
    # Giả lập phản hồi từ chatbot
    # Lấy về câu trả lời
    ai_response = response.json()
    response = ai_response.get("output", "Không có dữ liệu")
    st.session_state["messages"].append({"role": "ai", "content": response})
    with chat_container:
        st.chat_message("ai", avatar= icon_bot).write(response)
    
    st.write (a) 



# Hiển thị nội dung hội thoại sau khi chat
st.text_area("Tóm tắt cuộc hội thoại:", full_conversation, height=200)