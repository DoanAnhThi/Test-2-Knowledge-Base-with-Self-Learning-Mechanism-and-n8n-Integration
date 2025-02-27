import streamlit as st
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load model SBERT
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


# GIAO DIỆN TRANG WEB
def main():
    st.title("Hỏi đáp với AI")
    
    # Ô nhập câu hỏi
    question = st.text_input("Đặt câu hỏi của bạn:")
    
    # Chuyển câu hỏi thành vector bằng model SBERT
    vectors = np.array([model.encode(text) for text in question], dtype=np.float32)
    
    # Tạo FAISS index (L2 - Euclidean Distance)
    dimension = vectors.shape[1]  # 384 chiều (MiniLM-L6-v2)
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)  # Lưu vector vào FAISS
    st.write("Đã lưu vector vào FAISS!")
    
    if question:
        st.write("Bạn đã hỏi:", question)
        st.write("Câu trả lời:", "Tôi chưa có dữ liệu để trả lời câu hỏi này.")


    # Ô upload file
    uploaded_file = st.file_uploader("Tải lên tệp PDF, Word hoặc Text", type=["pdf", "docx", "txt"])

    # Ô feedback 
    feedback = st.text_input("Bạn có hài hong với câu trả lời này không")
    
    if uploaded_file:
        st.write("Bạn đã tải lên:", uploaded_file.name)
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post("https://bincalam28499.app.n8n.cloud/webhook-test/fed3dad1-f15d-4f2a-9b1d-7a4f4af1f4b1", files=files)  
    
    # Xử lý câu hỏi (Ở đây chỉ phản hồi đơn giản, có thể tích hợp AI sau)
    
if __name__ == "__main__":
    main()

