import streamlit as st
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

# Giao diện Streamlit
st.title("📄 File Upload & Convert to TXT")

uploaded_file = st.file_uploader("Tải lên file (.pdf, .doc, .docx, .txt)", type=["pdf", "doc", "docx", "txt"])

if uploaded_file:
    text_content = process_uploaded_file(uploaded_file)
    st.write( text_content)
    # if text_content:
    #     st.subheader("📜 Nội dung đã chuyển đổi:")
    #     st.text_area("Nội dung file:", text_content, height=300)

    #     # Tải file TXT đã chuyển đổi
    #     st.download_button(
    #         label="📥 Tải file TXT",
    #         data=text_content,
    #         file_name="converted.txt",
    #         mime="text/plain"
    #     )
    # else:
    #     st.error("❌ Không thể chuyển đổi file. Vui lòng thử lại.")
