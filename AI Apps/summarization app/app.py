import streamlit as st
import openai
import docx
import PyPDF2
from fpdf import FPDF


def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text


def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def summarize_text(api_key, text):
    try:
        client = openai.Client(api_key=api_key)  # Initialize client
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                {"role": "user", "content": f"Summarize this text:\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

def generate_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    pdf_file = "summary_output.pdf"
    pdf.output(pdf_file)
    return pdf_file


def main():
    st.set_page_config(layout="wide")
    st.title("File Summarizer with OpenAI")
    
    col1, col2 = st.columns([1, 3])

    with col1:
        api_key = st.text_input("Enter your OpenAI API Key", type="password")

    with col2:
        uploaded_file = st.file_uploader("Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

        if uploaded_file and api_key:
            if uploaded_file.type == "application/pdf":
                text = read_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = read_docx(uploaded_file)
            elif uploaded_file.type == "text/plain":
                text = uploaded_file.read().decode("utf-8")
            else:
                st.error("Unsupported file format")
                return

            st.write("File uploaded successfully!")
            if st.button("Summarize"):
                summary = summarize_text(api_key, text)
                st.subheader("Summary")
                st.write(summary)

                pdf_file = generate_pdf(summary)
                with open(pdf_file, "rb") as f:
                    st.download_button("Download Summary as PDF", f, file_name="summary_output.pdf")
        elif not api_key:
            st.warning("Please enter your OpenAI API Key.")

if __name__ == '__main__':
    main()
