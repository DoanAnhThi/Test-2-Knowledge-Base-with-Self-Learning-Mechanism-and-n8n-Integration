import streamlit as st
import requests


# Webhook URL API - Test
question_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/viACT-agent"    # query param URL
feedback__API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/feedback-to-improve-knowledgebase"   
upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/post-to-Google-Drive"
# question_start_coversation=                                      #Sinh ra doan ma ngau nhien   

# Webhook URL API - Publish
# question_API_URL = "https://bincalam28499.app.n8n.cloud/webhook/viACT-agent"     
# feedback__API_URL = "https://bincalam28499.app.n8n.cloud/webhook/feedback-to-improve-knowledgebase"     
# upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook/post-to-Google-Drive"     


# GIAO DIỆN TRANG WEB
# def main():
st.title("Hỏi đáp với AI")


# Ô upload file
uploaded_file = st.file_uploader("Tải lên tệp PDF, Word hoặc Text", type=["pdf", "docx", "txt"])
if uploaded_file:
    # Tải file lên google drive
    response = requests.post(upload_API_URL, data={'filename':uploaded_file.name}, files ={'file': (uploaded_file.name, uploaded_file, uploaded_file.type)})
    st.write("Bạn đã tải lên:", uploaded_file.name, "vui lòng chờ vài giây để kiến thức được cập nhật")


question = st.text_input("Đặt câu hỏi của bạn:")
st.write(question)
if question:
    # Gửi question lên Webhook
    response = requests.post(question_API_URL, json={'question':question})
    
    # Lấy về câu trả lời
    ai_response = response.json()
    output_text = ai_response.get("output", "Không có dữ liệu")

    st.write("Câu trả lời:",output_text)  # Xem câu trả lời của AI Agent

    # Ô feedback 
    feedback = st.text_input("Bạn có hài hong với câu trả lời này không")
    # Đẩy dữ liệu lên vector DB
if feedback:
    feedback_prompt = f"Câu hỏi:' {question} ' không hề khó như bạn nghĩ '{question}' được trả lời như sau:' {feedback}'"

    # Gửi feedback lên Webhook
    response = requests.post(feedback__API_URL, json={'feedback_prompt':feedback_prompt})
    # st.write('Cảm ơn bạn đã gửi phản hồi')
    st.write(feedback_prompt)


    
# if __name__ == "__main__":
#     main()

