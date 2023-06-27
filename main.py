from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello hack-a-thletes</h1>"
