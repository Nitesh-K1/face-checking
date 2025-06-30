from flask import Flask, render_template, request
import csv, os
import nepali_datetime
app = Flask(__name__)
@app.route("/")
def dashboard():
    log_file = os.path.join(app.root_path, "logs", "checkin_log.csv")
    checkins = []
    name_query = request.args.get('name', '').lower().strip()
    bs_year = request.args.get('bs_year')
    bs_month = request.args.get('bs_month')
    bs_day = request.args.get('bs_day')
    bs_date_query = ""
    try:
        if bs_year and bs_month and bs_day:
            bs_date = nepali_datetime.date(int(bs_year), int(bs_month), int(bs_day))
            bs_date_query = str(bs_date)
    except:
        bs_date_query = ""
    if os.path.exists(log_file):
        with open(log_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 3:
                    name, date, time = row
                    if name_query and name_query not in name.lower():
                        continue
                    if bs_date_query and bs_date_query != date:
                        continue
                    checkins.append({"name": name, "date": date, "time": time})
    return render_template("dashboard.html", checkins=checkins)
if __name__ == "__main__":
    app.run(debug=True)
