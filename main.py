from flask import Flask, render_template, request, send_file

app = Flask(__name__)

""" File path directions """
class FilePath:
    Response = "templates/response.html"

@app.route("/", methods=["GET", "POST"])
def hello_world():
    
    # generate response from user input
    if request.method == "POST":
        user_prompt = request.form.get('userQuestion')
        return render_template("index.html", user_prompt=user_prompt)
    
    return render_template("index.html", user_prompt="")

