from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/checkins")
def get_checkins():
    log_file = "logs/checkin_log.csv"
    checkins = []

    name_query = request.args.get('name', '').lower().strip()
    
    if os.path.exists(log_file):
        with open(log_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 3:
                    name, date, time = row
                    if name_query in name.lower() or not name_query:
                        checkins.append({"name": name, "date": date, "time": time})

    return jsonify(checkins)

if __name__ == "__main__":
    app.run(debug=True)
