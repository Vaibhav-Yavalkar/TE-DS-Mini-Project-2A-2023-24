from flask import Flask, render_template, Response
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import time

app = Flask(__name__)

# Set the path to the models directory
models_dir = './models'

# Load the model and labels
model = load_model(models_dir + '/model.h5')
label = np.load(models_dir + '/labels.npy')

mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands
holistic = mp_holistic.Holistic(static_image_mode=False, model_complexity=0)
drawing = mp.solutions.drawing_utils

# Global variable to store the last recognized mood
last_recognized_label = ""

def update_last_mood(recognized_label):
    global last_recognized_label
    last_recognized_label = recognized_label

@app.route('/')
def index():
    return render_template('index.html', last_recognized_label=last_recognized_label)

def generate_frames():
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 7:
            break

        if elapsed_time > 1:  # Capture and process a frame every 1 seconds
            _, frm = cap.read()
            frm = cv2.flip(frm, 1)

            lst = []

            res = holistic.process(frm)

            if res.face_landmarks:
                for i in res.face_landmarks.landmark:
                    lst.append(i.x - res.face_landmarks.landmark[1].x)
                    lst.append(i.y - res.face_landmarks.landmark[1].y)
                if res.left_hand_landmarks:
                    for i in res.left_hand_landmarks.landmark:
                        lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                        lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
                else:
                    for i in range(42):
                        lst.append(0.0)
                if res.right_hand_landmarks:
                    for i in res.right_hand_landmarks.landmark:
                        lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                        lst.append(i.y - res.right_hand_handmarks.landmark[8].y)
                else:
                    for i in range(42):
                        lst.append(0.0)
                lst = np.array(lst).reshape(1, -1)
                recognized_label = label[np.argmax(model.predict(lst))]
                update_last_mood(recognized_label)
                cv2.putText(frm, recognized_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            drawing.draw_landmarks(frm, res.face_landmarks)
            drawing.draw_landmarks(frm, res.left_hand_landmarks, mp_hands.HAND_CONNECTIONS)
            drawing.draw_landmarks(frm, res.right_hand_landmarks, mp_hands.HAND_CONNECTIONS)

            frame = cv2.imencode('.jpg', frm)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
