import cv2
import face_recognition
import json
import os
DB_PATH ="data/face_data.json"
def load_database():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as file:
            return json.load(file)
        return {"people":[]}
    
def save_database(data):
    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=4)    

video_capture = cv2.VideoCapture(0)
print("Press 'q' to quit.")
while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.imshow("Hotel Check-In - Face Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
