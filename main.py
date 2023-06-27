#Working Code
from flask import Flask, render_template, request
import gpt4all

app = Flask(__name__)
gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")


""" File path directions """
class FilePath:
    Response = "templates/response.html"

@app.route("/", methods=["GET", "POST"])
def hello_world():

    # generate response from user input
    if request.method == "POST":
        user_prompt = request.form.get('user-question')
        messages = [{"role": "user", "content": user_prompt}]
        result = gptj.chat_completion(messages)
        return render_template("index.html", user_prompt=result)
    

    return render_template("index.html", user_prompt="")

