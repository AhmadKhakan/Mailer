from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allow CORS for your frontend (update this to your real frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["https://yourdomain.com"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Form data schema
class FormData(BaseModel):
    name: str
    email: str
    company: str
    message: str

@app.post("/send-email")
async def send_email(data: FormData):
    try:
        email_sender = os.environ["EMAIL_USER"]
        email_password = os.environ["EMAIL_PASS"]
        email_receiver = os.environ["RECEIVER_EMAIL"]


        subject = f"New message from {data.name} at {data.company}"
        body = f"""
        You received a message from your website contact form:

        Name: {data.name}
        Email: {data.email}
        Company: {data.company}
        Message:
        {data.message}
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)

        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"error": str(e)}
