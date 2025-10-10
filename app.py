from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open("jobs.json", "r", encoding="utf-8") as f:
            jobs = json.load(f)
    except FileNotFoundError:
        jobs = []
    return render_template("index.html", jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True, extra_files=["templates/index.html"])
