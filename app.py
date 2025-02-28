import streamlit as st
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pypdf import PdfReader

# Load model SBERT
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Tạo làm chuyển Text thành vector rồi lưu và vector database FAISS
def vectorize(context):
    if context !="":

        vectors = np.array([model.encode(text) for text in context], dtype=np.float32)

        # Tạo FAISS index (L2 - Euclidean Distance)
        dimension = vectors.shape[1]  # 384 chiều (MiniLM-L6-v2)
        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)  # Lưu vector vào FAISS
        # st.write("Đã lưu vector vào FAISS!")

# """Trích xuất văn bản từ file PDF."""
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

# GIAO DIỆN TRANG WEB
def main():
    st.title("Hỏi đáp với AI")

    # Ô upload file
    uploaded_file = st.file_uploader("Tải lên tệp PDF, Word hoặc Text", type=["pdf", "docx", "txt"])
    
    # Tiền xử lý dữ liệu
    if uploaded_file is not None:
        file_type = uploaded_file.type
        # Tiền xử lý dữ liệu file PDF
        if file_type == "application/pdf":
            with st.spinner("Đang trích xuất nội dung từ PDF..."):
                text = extract_text_from_pdf(uploaded_file)
        # Tiền xử lý dữ liệu file doc    
        elif file_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            st.write("Bạn đã upload một file DOC hoặc DOCX.")

        # Tiền xử lý dữ liệu file txt
        elif file_type == "text/plain":
            st.write("Bạn đã upload một file TXT.")
        
        # Báo file không hợp lệ
        else:
            st.write("Định dạng file không hợp lệ.")
    #Xử lý dữ liệu (chuyển file pdf, docx về file text)
    #Chia các tài liệu thành các phần nhỏ



    #Vectorize các tài liệu text đã được chia nhỏ này và đẩy lên vector database





    # Ô nhập câu hỏi
    question = st.text_input("Đặt câu hỏi của bạn:")
    
    if question:
        # Tra trong vectorDB các dữ liệu nào gần giống với question nhất

        # Tạo prompt từ {context} là các vector vừa query được từ vectorDB + {question}

        # câu prompt để cho vào LLM {context}
        data = {
            "chatInput": f"""Bạn là một trợ lý AI. Sử dụng thông tin sau để trả lời câu hỏi:
            {text}
                        
            Câu hỏi: {question}"""
            }
        # Gửi request POST
        webhook_url = "https://bincalam28499.app.n8n.cloud/webhook-test/process-prompt"
        response = requests.post(webhook_url, json=data)
        
        # Lấy về câu trả lời
        ai_response = response.json()
        output_text = ai_response.get("output", "Không có dữ liệu")

        st.write("Câu trả lời:",output_text)  # Xem câu trả lời của AI Agent

        # Ô feedback 
        feedback = st.text_input("Bạn có hài hong với câu trả lời này không")
        # Đẩy dữ liệu lên vector DB
        if feedback:
            vectorize(feedback)
            st.write('Cảm ơn bạn đã gửi phản hồi')
    
    if uploaded_file:
        # st.write("Bạn đã tải lên:", uploaded_file.name)
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post("https://bincalam28499.app.n8n.cloud/webhook-test/PDF-to-text", files=files)  
    

    
if __name__ == "__main__":
    main()

