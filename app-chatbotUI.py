import streamlit as st
# from PyPDF2 import PdfReader
# from docx import Document

st.set_page_config(page_title="Tuyết Hương xin đẹp", layout="wide")

# Sidebar để tải file lên
with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Chọn file (doc, docx, pdf, txt)", type=["doc", "docx", "pdf", "txt"])
    if uploaded_file:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        
        # # Đọc nội dung file
        # if uploaded_file.type == "text/plain":
        #     text = str(uploaded_file.read(), "utf-8")
        # elif uploaded_file.type == "application/pdf":
        #     pdf_reader = PdfReader(uploaded_file)
        #     text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        # elif uploaded_file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        #     doc = Document(uploaded_file)
        #     text = "\n".join([para.text for para in doc.paragraphs])
        # else:
        #     text = "Không thể đọc file này."
        # st.text_area("Nội dung file:", text, height=200)

# Tiêu đề luôn hiển thị
# st.markdown("<h1 style='text-align: center;'>💬 Tuyết Hương xin đẹp</h1>", unsafe_allow_html=True)

title_container = st.empty()
with title_container:
    st.markdown("<h1 style='text-align: center;'>💬 Tuyết Hương xin đẹp</h1>", unsafe_allow_html=True)


# Vùng chat cố định
chat_container = st.container()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Hiển thị lịch sử chat
with chat_container:
    for message in st.session_state["messages"]:
        st.chat_message("user" if message["role"] == "user" else "assistant").write(message["content"])

# Ô nhập tin nhắn
user_input = st.text_input("Nhập câu hỏi...", key="user_input")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with chat_container:
        st.chat_message("user").write(user_input)
    
    # Giả lập phản hồi từ chatbot
    response = "Xin lỗi, tôi không hiểu câu hỏi của bạn."  # Thay bằng chatbot thực tế của bạn
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with chat_container:
        st.chat_message("assistant").write(response)
