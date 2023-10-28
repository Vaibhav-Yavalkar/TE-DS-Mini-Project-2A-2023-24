import os

current_file_path = "static/user uploaded/Healthy.JPG"
new_file_path = os.path.splitext(current_file_path)[0] + ".jpg"
os.rename(current_file_path, new_file_path)
print(f"File renamed to {new_file_path}")