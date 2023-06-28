from flask import Flask, render_template, request
import magic
import gpt4all
import PyPDF2
from docx import Document

""" SET UP GPT4ALL """
app = Flask(__name__)
gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")


class FilePath:
    Response = "templates/response.html"

class Prompt:
    Delimiter = "****"
    Text = f"""
    """

""" FILETYPE DEPENDENT  """
def read_text(file):
    return file.read().decode('utf-8')


def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def read_docx(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def get_file_content(file):
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    content = ""
    if mime_type == "text/plain":
        content = read_text(file)
    elif mime_type == "application/pdf":
        content = read_pdf(file)
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        content = read_docx(file)
    else:
        return ""
    return content

""" DISPLAY """
@app.route("/", methods=["GET", "POST"])
def prompt():
    if request.method != "POST": 
        return render_template("index.html", user_prompt="")

    # Add user question to messages
    user_prompt = str(request.form.get('user-question'))
    messages = [
        {"role": "system", "content": Prompt.Text},
        {"role": "user", "content": user_prompt},
    ]

    # Gather file contents
    file_contents = ""
    if 'files' in request.files:
        files = request.files.getlist('files')
        for file in files:
            content = get_file_content(file)
            if content:
                file_contents += content + "\n"

    # Write file content with wrapped delimiters to messages content
    if file_contents:
        #messages[0]["content"] += "\n" + Prompt.Delimiter + file_contents + Prompt.Delimiter
        messages[0]["content"] += "\n" + file_contents

    # Get response
    response = ""
    if len(messages) > 0:
        result = gptj.chat_completion(messages)
        response = result.get('choices')[0].get('message').get('content')

    if len(response) == 0:
        lst = ""
        print("No response")
    else:
        lst = response
        print(lst)

    return render_template("index.html", user_prompt=lst)

if __name__ == "__main__":
    app.run(debug=True)
