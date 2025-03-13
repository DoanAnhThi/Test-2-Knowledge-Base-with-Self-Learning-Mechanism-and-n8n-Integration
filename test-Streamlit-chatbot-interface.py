import streamlit as st
import requests

# # Webhook URL API - Test
# question_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/chat-input-v2"     
# feedback__API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/feedback-v2"     
# upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook-test/upload-document-v2" 

# Webhook URL API - Publish
question_API_URL = "https://bincalam28499.app.n8n.cloud/webhook/chat-input-v2"     
feedback__API_URL = "https://bincalam28499.app.n8n.cloud/webhook/feedback-v2"     
upload_API_URL = "https://bincalam28499.app.n8n.cloud/webhook/upload-document-v2" 

# Tiêu đề luôn hiển thị
st.set_page_config(page_title="viACT Agent", layout="wide")
st.title("💬 viACT Agent")
# st.caption("🚀 A viACT chatbot powered by Google Gemini")

if "messages" not in st.session_state:
    # st.session_state["messages"] = []
    st.session_state["messages"] = [{"role": "ai", "content": "How can I help you?"}]

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = False  # Biến cờ để kiểm tra file đã gửi chưa
if "last_uploaded_filename" not in st.session_state:
    st.session_state["last_uploaded_filename"] = None  # Lưu tên file đã gửi trước đó


#GOM CUỘC HỒI THOẠI LẠI
# Tạo biến text chứa toàn bộ cuộc hội thoại
full_conversation = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
# # Hiển thị nội dung hội thoại sau khi chat
# st.text_area("Tóm tắt cuộc hội thoại:", full_conversation, height=200)

# Sidebar để tải file lên
with st.sidebar:
    st.header("Upload your file here")
    uploaded_file = st.file_uploader("", type=["doc", "docx", "pdf", "txt"])
    # if uploaded_file:
    #     st.session_state["uploaded_file"] = uploaded_file
    #     file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    #     response = requests.post(upload_API_URL, data={'filename':uploaded_file.name,'filetype':uploaded_file.type,}, files ={'file': (uploaded_file.name, uploaded_file, uploaded_file.type)})
    #     # st.write(file_details)
    
    # Xử lý khi có file được upload
    if uploaded_file:
        # Kiểm tra xem file mới có khác file cũ không
        is_new_file = uploaded_file.name != st.session_state["last_uploaded_filename"]
        
        if is_new_file or not st.session_state["file_uploaded"]:
            st.session_state["uploaded_file"] = uploaded_file
            file_details = {
                "Filename": uploaded_file.name,
                "FileType": uploaded_file.type,
                "FileSize": uploaded_file.size
            }
            # st.write("File details:", file_details)
            
            # Gửi file đến API
            response = requests.post(
                upload_API_URL,
                data={"filename": uploaded_file.name, "filetype": uploaded_file.type},
                files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            )
            
            # Kiểm tra phản hồi từ API
            if response.status_code == 200:
                st.success("File uploaded successfully!")
                st.session_state["file_uploaded"] = True  # Đánh dấu file đã được gửi
                st.session_state["last_uploaded_filename"] = uploaded_file.name  # Lưu tên file đã gửi
            else:
                st.error(f"Failed to upload file. Status code: {response.status_code}")
    
    
    
    # Nút reset lịch sử chat
    # if st.button("New Chat"):
    #     response = requests.post(feedback__API_URL, json={'feedback_prompt':full_conversation})
    #     # full_conversation = 1 #đẩy đoạn đoạn này lên vectordatabase để mô hình học
    #     st.session_state["messages"] = []
#----------------------------------------------------------------------------------
    if st.button("New Chat"):
        response = requests.post(feedback__API_URL, json={'feedback_prompt': full_conversation})
        st.session_state["messages"] = []
        st.session_state["uploaded_file"] = None
        st.session_state["file_uploaded"] = False  # Reset để cho phép gửi file mới
        st.session_state["last_uploaded_filename"] = None  # Xóa thông tin file cũ
        st.rerun()  # Làm mới giao diện


# Vùng chat cố định
chat_container = st.container()



icon_user = "./icon/man1.png"
icon_bot="./icon/bot.png"
# Hiển thị lịch sử chat
with chat_container:
    for message in st.session_state["messages"]:
        st.chat_message(message["role"], avatar= icon_user if message["role"] == "user" else icon_bot).write(message["content"])
        # st.chat_message("user" if message["role"] == "user" else "ai").write(message["content"])


# Ô nhập tin nhắn
user_input = st.chat_input("Your message...")
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
    
    # # Xóa file sau khi gửi tin nhắn và reset giao diện
    # if st.session_state["uploaded_file"]:
    #     st.session_state["uploaded_file"] = None
    #     st.experimental_rerun()  # Làm mới giao diện để reset file upload