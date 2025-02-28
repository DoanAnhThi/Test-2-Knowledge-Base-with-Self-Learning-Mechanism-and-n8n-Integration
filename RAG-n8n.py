import streamlit as st
import requests


# Webhook URL API
webhook_url = "https://bincalam28499.app.n8n.cloud/webhook-test/viACT-agent"    #Test URL
# webhook_url = "https://bincalam28499.app.n8n.cloud/webhook/viACT-agent"         # Publish URL


# GIAO DIỆN TRANG WEB
def main():
    st.title("Hỏi đáp với AI")

    # Ô upload file
    uploaded_file = st.file_uploader("Tải lên tệp PDF, Word hoặc Text", type=["pdf", "docx", "txt"])

    question = st.text_input("Đặt câu hỏi của bạn:")
    
    if question:
        # Gửi question lên Webhook
        response = requests.post(webhook_url, json={'question':question})
        
        # Lấy về câu trả lời
        ai_response = response.json()
        output_text = ai_response.get("output", "Không có dữ liệu")

        st.write("Câu trả lời:",output_text)  # Xem câu trả lời của AI Agent

    # Ô feedback 
    feedback = st.text_input("Bạn có hài hong với câu trả lời này không")
    # Đẩy dữ liệu lên vector DB
    if feedback:
        # Gửi feedback lên Webhook
        response = requests.post(webhook_url, json={'feedback':feedback})
        st.write('Cảm ơn bạn đã gửi phản hồi')
    
    # if uploaded_file:
    #     # Tải file lên google drive

    
if __name__ == "__main__":
    main()

