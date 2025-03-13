import streamlit as st
import requests


# Thêm các hàm để convert file có định dạng PDF, DOC, DOCX, TXT về TXT hêt
import os
import tempfile
from docx import Document
from PyPDF2 import PdfReader

# Hàm chuyển file PDF sang text
def convert_pdf_to_txt(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Hàm chuyển file DOCX sang text
def convert_docx_to_txt(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Hàm chuyển file DOC sang text (Chỉ hỗ trợ Windows)
def convert_doc_to_txt(file_path):
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(file_path))
        txt_path = file_path.replace(".doc", ".txt")
        doc.SaveAs(txt_path, FileFormat=2)  # wdFormatText = 2
        doc.Close()
        word.Quit()
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
        os.remove(txt_path)
        return text
    except ImportError:
        return "Chuyển đổi .doc chỉ hỗ trợ trên Windows với MS Word."

# Hàm xử lý upload file và chuyển đổi về TXT
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Lưu file tạm thời
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        # Chuyển đổi về text
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension == "txt":
            with open(temp_path, "r", encoding="utf-8") as f:
                text = f.read()
        elif file_extension == "pdf":
            text = convert_pdf_to_txt(temp_path)
        elif file_extension == "docx":
            text = convert_docx_to_txt(temp_path)
        elif file_extension == "doc":
            text = convert_doc_to_txt(temp_path)
        else:
            text = "Định dạng file không được hỗ trợ."

        # Xóa file tạm
        os.remove(temp_path)

        return text

    return None


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
    # # Tải file lên google drive
    # response = requests.post(upload_API_URL, data={'filename':uploaded_file.name,'filetype':uploaded_file.type,}, files ={'file': (uploaded_file.name, uploaded_file, uploaded_file.type)})
    # # st.write("Bạn đã tải lên:", uploaded_file.name, "vui lòng chờ vài giây để kiến thức được cập nhật")
    #------------------------------
    # Phương án 2
    text_content = process_uploaded_file(uploaded_file)
    response = requests.post(feedback__API_URL, json={'feedback_prompt':text_content})



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

