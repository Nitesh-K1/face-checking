from flask import Flask, render_template, request, redirect, url_for
import nepali_datetime
import sqlite3
import os
app = Flask(__name__)
DB_PATH = os.path.join(app.root_path, "logs", "checkin_log.db")
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_bs TEXT NOT NULL,
            time_12hr TEXT NOT NULL,
            image_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
def get_checkins(name_query="", date_query=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT id, name, date_bs, time_12hr, image_path FROM checkins WHERE 1=1"
    params = []
    if name_query:
        query += " AND LOWER(name) LIKE ?"
        params.append(f"%{name_query.lower()}%")
    if date_query:
        query += " AND date_bs = ?"
        params.append(date_query)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "date": r[2], "time": r[3], "image_path": r[4]} for r in rows]
def delete_checkin(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM checkins WHERE id = ?", (id,))
    conn.commit()
    conn.close()
@app.route("/")
def dashboard():
    name_query = request.args.get('name', '').strip()
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

    checkins = get_checkins(name_query, bs_date_query)
    return render_template("dashboard.html", checkins=checkins)
@app.route("/delete/<int:id>")
def delete(id):
    delete_checkin(id)
    return redirect(url_for('dashboard'))
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
