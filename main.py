import streamlit as st
from gtts import gTTS
from docx import Document
import base64
import os

def text_to_speech(text, filename):
    tts = gTTS(text)
    tts.save(filename)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">Download {file_label}</a>'
    return href

def read_file(file_path):
    try:
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                return f.read()
        elif file_path.endswith('.doc') or file_path.endswith('.docx'):
            doc = Document(file_path)
            return ' '.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_path.endswith('.pdf'):  
            from pdfreader import SimplePDFViewer
            fd = open(file_path, 'rb')
            viewer = SimplePDFViewer(fd)
            text = ''
            for canvas in viewer:
                viewer.render()
                text += ' '.join(viewer.canvas.strings)
            fd.close()
            return text
            
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return None

st.title('Text to Speech Converter')
uploaded_file = st.file_uploader("Choose a text file...", type=["txt", "doc", "docx", "pdf"])

if uploaded_file is not None:
    st.write("Processing...")
    # Save the temporary file with the original extension
    file_extension = os.path.splitext(uploaded_file.name)[1]
    temp_file = f'temp{file_extension}'
    with open(temp_file, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    text = read_file(temp_file)
    if text is not None:
        text_to_speech(text, 'output_audio.mp3')
        st.markdown(get_binary_file_downloader_html('output_audio.mp3', 'Audio'), unsafe_allow_html=True)
    else:
        st.error("Uploaded file is not a valid text file.")
    # Clean up the temporary file
    os.remove(temp_file)
}
