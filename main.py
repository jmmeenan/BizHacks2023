from flask import Flask, render_template, request
import gpt4all

app = Flask(__name__)
gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")

class FilePath:
    Response = "templates/response.html"

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        user_prompt = request.form.get('user-question')
        messages = [{"role": "user", "content": user_prompt}]

        if 'files' in request.files:
            files = request.files.getlist('files')
            file_contents = [file.read().decode('latin-1') for file in files]
            file_messages = [{"role": "system", "content": content} for content in file_contents]
            messages += file_messages

            result = gptj.chat_completion(messages)
        else:
            result = gptj.chat_completion(messages)

        if len(result) == 0:
            print("No response")
        else:
            lst = result.get('choices')[0].get('message').get('content')
            print(lst.encode('utf-8', errors='replace').decode('utf-8'))

        return render_template("index.html", user_prompt=lst)

    return render_template("index.html", user_prompt="")

if __name__ == "__main__":
    app.run(debug=True)
