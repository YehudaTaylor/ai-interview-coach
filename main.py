from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    response = client.chat.completions.create(model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=300)

    return {"message": response.choices[0].message.content}

@app.post("/upload-cv")
def upload_cv(file: UploadFile = File(...)):
    contents = file.file.read().decode("utf-8")
    return {"cv_text": contents}

@app.post("/upload-jd")
def upload_jd(file: UploadFile = File(...)):
    contents = file.file.read().decode("utf-8")
    return {"job_description": contents}

