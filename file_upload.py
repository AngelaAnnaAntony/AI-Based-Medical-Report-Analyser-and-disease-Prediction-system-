import os 
UPLOAD_FOLDER="uploads"
def save_file(file):
    filepath=os.path.join(UPLOAD_FOLDER, file.name)
    with open(filepath, "wb") as f:
        f.write(file.getbuffer())
    return filepath