import streamlit as st
import requests

st.title("Example with dynamic key")

upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/post-to-Google-Drive" #Test
# upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/post-to-Google-Drive" # Publish

uploaded_file = st.file_uploader("Upload your files (PDF, Word or Text)", type=["pdf", "docx", "doc", "txt"])
if uploaded_file:
    # Tải file lên google drive
    response = requests.post(upload_API_URL, data={'filename':uploaded_file.name,'filetype':uploaded_file.type,}, files ={'file': (uploaded_file.name, uploaded_file, uploaded_file.type)})
    st.write("Bạn đã tải lên:", uploaded_file.name, "vui lòng chờ vài giây để kiến thức được cập nhật")