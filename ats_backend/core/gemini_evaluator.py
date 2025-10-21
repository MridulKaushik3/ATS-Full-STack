# core/gemini_evaluator.py
import base64, io, os
import pdf2image
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def evaluate_resume(resume_file, job_description, prompt):
    images = pdf2image.convert_from_bytes(resume_file.read())
    img_byte_arr = io.BytesIO()
    images[0].save(img_byte_arr, format='JPEG')
    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()

    pdf_parts = [{
        "mime_type": "image/jpeg",
        "data": img_base64
    }]
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, pdf_parts[0], job_description])
    return response.text
