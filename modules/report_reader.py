import pdfplumber
import pytesseract
import cv2
import numpy as np
from PIL import Image
import os
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_pdf(file):
    text=""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def read_image(file):
    image=Image.open(file)
    image=np.array(image)
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (5,5), 0)
    gray=cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    text=pytesseract.image_to_string(gray)
    return text

def extract_text(uploaded_file):
    file_type=uploaded_file.type
    if file_type=="application/pdf":
        return read_pdf(uploaded_file)
    elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
        return read_image(uploaded_file)
    else:
        return ""
