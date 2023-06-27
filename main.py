from flask import Flask, render_template, request
import magic
import io
import gpt4all

app = Flask(__name__)
gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")


class FilePath:
    Response = "templates/response.html"


def read_text(file):
    return file.read().decode('utf-8')


def read_pdf(file):
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def read_docx(file):
    from docx import Document
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


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        user_prompt = request.form.get('user-question')
        messages = [{"role": "user", "content": user_prompt}]

        file_contents = ""
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                content = get_file_content(file)
                if content:
                    file_contents += content + "\n"

        if file_contents:
            messages[0]["content"] += "\n" + file_contents

        response = ""
        if len(messages) > 0:
            result = gptj.chat_completion(messages)
            response = result.get('choices')[0].get('message').get('content')

        if len(response) == 0:
            print("No response")
            lst = ""
        else:
            lst = response
            print(lst)

        return render_template("index.html", user_prompt=lst)

    return render_template("index.html", user_prompt="")


if __name__ == "__main__":
    app.run(debug=True)
