import cv2
import numpy as np
import sqlite3
import subprocess
import sys

# Connect to an SQLite database (or create a new one)
conn = sqlite3.connect('colours.db')

# Create a table to store the skin tone data
conn.execute('''
    CREATE TABLE IF NOT EXISTS skin_tone (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tone TEXT
    )
''')


def calculate_skin_tone(image):
    # ... (the rest of your skin tone calculation code)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([0, 48, 80], dtype=np.uint8)
    upper_bound = np.array([20, 255, 255], dtype=np.uint8)

    skin_mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    num_skin_pixels = np.sum(skin_mask == 255)

    if num_skin_pixels > 0:
        average_v_value = np.sum(hsv_image[skin_mask == 255][:, 2]) / num_skin_pixels
        if average_v_value > 200:
            return 'Light'
        elif average_v_value > 100:
            return 'Medium'
        else:
            return 'Dark'
    else:
        return 'No skin detected'


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video device.")
    sys.exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Store the skin tone in the database
    skin_tone = calculate_skin_tone(frame)
    conn.execute("INSERT INTO skin_tone (tone) VALUES (?)", (skin_tone,))
    conn.commit()
    break  # Break after the first frame is processed

# Close the database connection when done
conn.close()

print('The skin tone of the frame is:', skin_tone)  # Display the final skin tone

