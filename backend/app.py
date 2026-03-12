from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate-plan', methods=['POST'])
def generate_plan():

    data = request.json
    subjects = data.get("subjects", [])
    daily_hours = int(data.get("dailyHours", 4))

    # Convert subject hours to integers
    subject_list = []
    for s in subjects:
        subject_list.append({
            "name": s["name"],
            "hours": int(s["hours"])
        })

    plan = {}

    for day in range(1, 8):

        hours_left = daily_hours
        tasks = []

        for subject in subject_list:

            if subject["hours"] > 0 and hours_left > 0:

                study_time = min(1, subject["hours"], hours_left)

                tasks.append({
                    "subject": subject["name"],
                    "duration": f"{study_time} hour"
                })

                subject["hours"] -= study_time
                hours_left -= study_time

        plan[f"day{day}"] = tasks

    return jsonify(plan)

if __name__ == "__main__":
    app.run(debug=True, port=5000)