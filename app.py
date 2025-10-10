from flask import Flask, render_template, request, jsonify
import json

JOBS_PER_PAGE = 10

app = Flask(__name__)

@app.route("/")
def home():
    page = int(request.args.get("page", 1))
    try:
        with open("jobs.json", "r", encoding="utf-8") as f:
            jobs = json.load(f)

            jobs = sorted(jobs, key=lambda j: j['job_post_time'], reverse=True)
            start = (page - 1) * JOBS_PER_PAGE
            end =  start + JOBS_PER_PAGE
            jobs_page = jobs[start:end]
            total_pages = (len(jobs) + JOBS_PER_PAGE - 1) // JOBS_PER_PAGE


    except FileNotFoundError:
        jobs = []
    return render_template(
        "index.html", 
        jobs=jobs_page,
        page = page,
        total_pages = total_pages)

@app.route("/rawjson")
def deliverJSON():
    with open("jobs.json", "r", encoding = "utf-8") as f:
        jobs = json.load(f)
    return jsonify(jobs)

if __name__ == "__main__":
    app.run(debug=True, extra_files=["templates/index.html"])
