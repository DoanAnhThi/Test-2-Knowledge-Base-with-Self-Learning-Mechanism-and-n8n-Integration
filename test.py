import streamlit as st

st.title("Example with dynamic key")

question = st.text_input("Enter your question:")

# Tạo key động cho feedback dựa vào giá trị của question
feedback_key = f"feedback_{question}"
feedback = st.text_input("Enter your feedback:", key=feedback_key)

st.write(f"Question: {question}")
st.write(f"Feedback: {feedback}")
