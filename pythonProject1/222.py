import cv2
import numpy as np
from face_database import FaceDateBase

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_db = FaceDateBase('face')

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

for name, metadata in face_db.metadata_dict.items():
    for face_image_path in metadata['face_image']:
        face_image = cv2.imread(face_image_path, cv2.IMREAD_GRAYSCALE)
        if face_image is not None:
            print("я работаю")
            print(f"Обрабатывается изображение:  {face_image_path}")
            faces.append(face_image)
            labels.append(metadata['id'])
print(f"Всего обработано {len(faces)} изображений")
face_recognizer.train(faces, np.array(labels))

cap = cv2.VideoCapture('video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face_image = gray[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face_image)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, str(label), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(labels)
cap.release()
cv2.destroyWindow()