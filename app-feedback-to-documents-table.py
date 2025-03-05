import streamlit as st
import requests


# Webhook URL API - Test
# question_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/viACT-agent"    # query param URL
# feedback__API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/feedback-to-improve-knowledgebase"   
# upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/post-to-Google-Drive"
# question_start_coversation=                                      #Sinh ra doan ma ngau nhien   

# Webhook URL API - Publish
question_API_URL = "https://bincalam28499.app.n8n.cloud/webhook/fc658211-7838-48a4-a6df-2f6897c9fc6c"     
feedback__API_URL = "https://bincalam28499.app.n8n.cloud/webhook/55d36bf9-57ee-40a1-94ce-7af23ae3313c"     
upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook/1ece05d1-7e3c-4bd3-b974-2febcbfb61a3"     


# GIAO DIỆN TRANG WEB
# def main():
st.title("viACT Agent")


# Ô upload file
uploaded_file = st.file_uploader("Upload your files (PDF, Word or Text)", type=["pdf", "docx", "doc", "txt"])
if uploaded_file:
    # Tải file lên google drive
    response = requests.post(upload_API_URL, data={'filename':uploaded_file.name,'filetype':uploaded_file.type,}, files ={'file': (uploaded_file.name, uploaded_file, uploaded_file.type)})
    # st.write("Bạn đã tải lên:", uploaded_file.name, "vui lòng chờ vài giây để kiến thức được cập nhật")



question = st.text_input("What can I help with?")

if question:
    # Gửi question lên Webhook
    response = requests.post(question_API_URL, json={'question':question})
    
    # Lấy về câu trả lời
    ai_response = response.json()
    output_text = ai_response.get("output", "Không có dữ liệu")

    st.write("viACT Agent:",output_text)  # Xem câu trả lời của AI Agent

# Ô feedback 
feedback_key = f"feedback_{question}'"
feedback = st.text_input("Are you satisfied with this answer?", key=feedback_key)
# Đẩy dữ liệu lên vector DB
if feedback:
    feedback_prompt = f"""
    The answer to question ' {question} ' is very easy. In the future, if similar questions to ' {question} ' are asked, you must respond as follows: '{feedback}'. The answer must be '{feedback}' for the response to be correct.

    The answer to question ' {question} ' is very easy. In the future, if similar questions to ' {question} ' are asked, you must respond as follows: '{feedback}'. The answer must be '{feedback}' for the response to be correct.

    """


    # Gửi feedback lên Webhook
    response = requests.post(feedback__API_URL, json={'feedback_prompt':feedback_prompt})

    # st.write(feedback_prompt)


    
# if __name__ == "__main__":
#     main()

