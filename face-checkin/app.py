from flask import Flask, render_template
import csv
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    log_file = "logs/checkin_log.csv"
    checkins = []

    if os.path.exists(log_file):
        with open(log_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 3:
                    name, date, time = row
                    checkins.append({"name": name, "date": date, "time": time})

    return render_template("dashboard.html", checkins=checkins)

if __name__ == "__main__":
    app.run(debug=True)
