import cv2
import face_recognition
import json
import os
import numpy as np

DB_PATH = "data/face_data.json"

def load_database():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as file:
            return json.load(file)
    return {"people": []}

def save_database(data):
    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=4)

db = load_database()
video_capture = cv2.VideoCapture(0)

print("Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        match_found = False
        person_name = "Unknown"

        for person in db["people"]:
            known_encoding = np.array(person["encoding"])
            result = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.45)

            if result[0]:
                match_found = True
                person_name = person["name"]
                break

        color = (0, 255, 0) if match_found else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, person_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

        if match_found:
            print(f"✅ Recognized: {person_name}")
        else:
            print("🆕 New face detected (not in database)")

            video_capture.release()
            cv2.destroyAllWindows()

            name = input("Enter name for new guest: ")

            db["people"].append({
                "name": name,
                "encoding": list(face_encoding)
            })
            save_database(db)
            print(f"✅ Registered and saved: {name}")

            video_capture = cv2.VideoCapture(0)

    cv2.imshow("Hotel Check-In - Face Detector", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

video_capture.release()
cv2.destroyAllWindows()
