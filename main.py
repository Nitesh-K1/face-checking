import cv2
import face_recognition
import json
import os
import numpy as np
import datetime
import sqlite3
from nepali_datetime import date as nep_date
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_DB_PATH = os.path.join(LOG_DIR, "checkin_log.db")
FACES_DIR = os.path.join("static", "faces")
os.makedirs(FACES_DIR, exist_ok=True)
DB_PATH = "data/face_data.json"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
def load_database():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as file:
            data = json.load(file)
            if "next_id" not in data:
                data["next_id"] = 1
            return data
    return {"people": [], "next_id": 1}
def save_database(data):
    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=4)
def log_checkin_db(name, image_path=""):
    now_ad = datetime.datetime.now()
    now_bs = nep_date.from_datetime_date(now_ad.date())
    conn = sqlite3.connect(LOG_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_bs TEXT NOT NULL,
            time_12hr TEXT NOT NULL,
            image_path TEXT NOT NULL DEFAULT ''
        )
    ''')
    cursor.execute('''
        INSERT INTO checkins (name, date_bs, time_12hr, image_path) VALUES (?, ?, ?, ?)
    ''', (name, now_bs.strftime("%Y-%m-%d"), now_ad.strftime("%I:%M:%S %p"), image_path))
    conn.commit()
    conn.close()
db = load_database()
video_capture = cv2.VideoCapture(0)
recognized_names = set()
print("Press 'q' to quit.")
while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    original_frame = frame.copy()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        match_found = False
        person_name = "Unknown"
        person_image_path = ""
        min_distance = 0.5
        for person in db["people"]:
            known_encoding = np.array(person["encoding"])
            distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
            if distance < min_distance:
                min_distance = distance
                match_found = True
                person_name = person["name"]
                person_image_path = person.get("image_path", "")
        if match_found and person_name not in recognized_names:
            print(f"Recognized: {person_name}")
            log_checkin_db(person_name, person_image_path)
            recognized_names.add(person_name)
        elif not match_found:
            print("New face detected (not in database)")
            name = f"Person{db['next_id']}"
            db["next_id"] += 1
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%I%M%S%p")
            relative_img_path = os.path.join("faces", f"{name}_{timestamp}.jpg").replace("\\"    , "/")
            img_path = os.path.join("static", relative_img_path)
            cv2.imwrite(img_path, original_frame)
            db["people"].append({
                "name": name,
                "encoding": list(face_encoding),
                "image_path": relative_img_path
            })
            save_database(db)
            print(f"Registered and saved: {name}")
            log_checkin_db(name, relative_img_path)
            video_capture.release()
            cv2.destroyAllWindows()
            video_capture = cv2.VideoCapture(0)
            recognized_names = set()
            break
        color = (0, 255, 0) if match_found else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, person_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
    cv2.imshow("face check", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break
video_capture.release()
cv2.destroyAllWindows()
