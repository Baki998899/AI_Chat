import streamlit as st
import fitz  # For PDFs
from PIL import Image
import io
import pytesseract
from pdf2image import convert_from_path
from ollama import Client
from docx import Document  # For Word files

# PDF extraction function
def extract_pdf_data(pdf_path):
    doc = fitz.open(pdf_path)
    text_data = ""
    images = []
    image_text = ""
    for page in doc:
        text_data += page.get_text() + "\n"
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    doc.close()
    for img in images:
        text = pytesseract.image_to_string(img)
        image_text += text + "\n"
    pdf_images = convert_from_path(pdf_path)
    for pdf_img in pdf_images:
        ocr_text = pytesseract.image_to_string(pdf_img)
        image_text += ocr_text + "\n"
    return text_data, image_text, images

# Word file extraction function
def extract_docx_data(docx_path):
    doc = Document(docx_path)
    text_data = ""
    images = []
    image_text = ""
    for para in doc.paragraphs:
        text_data += para.text + "\n"
    return text_data, image_text, images  # Images omitted for simplicity

# LLaVA query function
def query_llava(text_data, image_text, question):
    client = Client(host='http://localhost:11434')
    prompt = (
        f"Based on this document content:\n"
        f"Text: {text_data}\n"
        f"Image/Chart Text: {image_text}\n"
        f"Question: {question}\n"
        f"If asked for Mermaid syntax, format it as ```mermaid\n...```"
    )
    try:
        response = client.chat(
            model="llava:7b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error querying LLaVA: {str(e)}"

# Streamlit app
def main():
    st.title("Document Chat with LLaVA")
    st.write("Upload a PDF or Word file and ask questions about its content!")

    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'doc_data' not in st.session_state:
        st.session_state.doc_data = None

    # Process uploaded file
    if uploaded_file is not None and st.session_state.doc_data is None:
        with st.spinner("Extracting document data..."):
            file_extension = uploaded_file.name.split(".")[-1].lower()
            temp_file = f"temp.{file_extension}"
            with open(temp_file, "wb") as f:
                f.write(uploaded_file.read())
            
            if file_extension == "pdf":
                text, img_text, imgs = extract_pdf_data(temp_file)
            elif file_extension == "docx":
                text, img_text, imgs = extract_docx_data(temp_file)
            
            st.session_state.doc_data = (text, img_text, imgs)
            st.success("Document processed! Start chatting.")

    # Chat interface
    if st.session_state.doc_data:
        text_data, image_text, _ = st.session_state.doc_data
        
        # Display chat history with custom font sizes
        chat_container = st.container()
        with chat_container:
            for question, answer in st.session_state.chat_history:
                # Question in larger font
                st.markdown(f"<p style='font-size: 20px;'><b>You:</b> {question}</p>", unsafe_allow_html=True)
                # Answer in standard font
                st.markdown(f"<p style='font-size: 16px;'><b>LLaVA:</b> {answer}</p>", unsafe_allow_html=True)

        # Chat input with form
        with st.form(key="chat_form", clear_on_submit=True):
            question = st.text_input("Ask a question about the document:", key="question_input")
            submit_button = st.form_submit_button(label="Send")

            # Process question on form submission
            if submit_button and question:
                with st.spinner("Getting answer..."):
                    answer = query_llava(text_data, image_text, question)
                    st.session_state.chat_history.append((question, answer))
                    st.rerun()

if __name__ == "__main__":
    main()