from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import PyPDF2
from docx import Document
import io

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_file(file: UploadFile) -> str:
    content = file.file.read()
    
    if file.filename.endswith('.pdf'):
        # Handle PDF files
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    elif file.filename.endswith(('.docx', '.doc')):
        # Handle DOCX files
        doc = Document(io.BytesIO(content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    else:
        # Handle text files
        return content.decode("utf-8")

class InterviewInput(BaseModel):
    cv_text: str
    job_description: str
    user_response: str

@app.post("/start-interview")
def start_interview(data: InterviewInput):
    prompt = f"""
    You are a recruiter conducting a mock interview. 
    The candidate's CV:
    {data.cv_text}

    The job description:
    {data.job_description}

    Based on the job and the CV, ask a relevant interview question. 
    If the user already responded, provide feedback and ask a follow-up question.

    User's last response: {data.user_response}
    """

    # TODO: Use GPT-4o  
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=300)

    return {"message": response.choices[0].message.content}

@app.post("/upload-cv")
def upload_cv(file: UploadFile = File(...)):
    contents = extract_text_from_file(file)
    return {"cv_text": contents}

@app.post("/upload-jd")
def upload_jd(file: UploadFile = File(...)):
    contents = extract_text_from_file(file)
    return {"job_description": contents}

