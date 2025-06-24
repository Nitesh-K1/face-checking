from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    log_file = os.path.join(app.root_path, "logs", "checkin_log.csv")
    checkins = []
    name_query = request.args.get('name', '').lower().strip()

    if os.path.exists(log_file):
        with open(log_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 3:
                    name, date, time = row
                    if name_query and name_query not in name.lower():
                        continue
                    checkins.append({"name": name, "date": date, "time": time})

    return render_template("dashboard.html", checkins=checkins)

if __name__ == "__main__":
    app.run(debug=True)
