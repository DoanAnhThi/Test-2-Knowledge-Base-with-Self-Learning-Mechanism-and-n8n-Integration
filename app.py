import streamlit as st
import requests


# Webhook URL API
webhook_url = "https://bincalam28499.app.n8n.cloud/webhook-test/post-to-Google-Drive"    #Test URL



def main():
    st.title("Hỏi đáp với AI")

    # Ô upload file
    uploaded_file = st.file_uploader("Tải lên tệp PDF, Word hoặc Text", type=["pdf", "docx", "txt"])
    response = requests.post(webhook_url, data={'filename':uploaded_file.name}, files ={'file': (uploaded_file.name, uploaded_file, uploaded_file.type)})
    # response = requests.post(webhook_url, json={'filename':uploaded_file.name})
   
    
    if uploaded_file:
        st.write("Bạn đã tải lên:", uploaded_file.name)
         
    

    
if __name__ == "__main__":
    main()

