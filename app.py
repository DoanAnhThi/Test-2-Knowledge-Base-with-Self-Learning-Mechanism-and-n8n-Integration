import streamlit as st
import requests

# URL webhook của n8n (thay thế bằng webhook của bạn)
# N8N_WEBHOOK_URL = "https://bincalam28499.app.n8n.cloud/webhook/b403cf13-1468-4a6e-b412-c60eb47979a7" #publish
N8N_WEBHOOK_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/b403cf13-1468-4a6e-b412-c60eb47979a7" #test

# Cấu hình giao diện Streamlit
st.title("💬 Tuyết Hương xin đệp ")
st.write("Nhập câu hỏi của bạn vào bên dưới:")

# Lưu trạng thái chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử tin nhắn
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Hộp nhập văn bản từ người dùng
user_input = st.chat_input("Nhập câu hỏi...")
if user_input:
    # Lưu tin nhắn của người dùng
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Gửi yêu cầu đến webhook của n8n
    response = requests.post(N8N_WEBHOOK_URL, json={"question": user_input})
    
    if response.status_code == 200:
        bot_reply = response.json().get("answer", "Xin lỗi, tôi không hiểu câu hỏi của bạn.")
    else:
        bot_reply = response.json().get("output", "")
    
    # Hiển thị câu trả lời từ chatbot
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
