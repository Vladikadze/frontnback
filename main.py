from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
EMAIL_ADDRESS = "vledbogomazov@gmail.com"  
EMAIL_PASSWORD = "password"          
SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 587  

app = FastAPI()

@app.post("/submit")
async def handle_form(name: str = Form(...), age: int = Form(...), color: str = Form(...)):
    file_exists = os.path.isfile("answers.csv")
    with open("answers.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Name", "Age", "Favorite Color"])
        writer.writerow([name, age, color])
     try: 
        subject = "New Form Submission"
        body = f"Name: {name}\nAge {age}\nFavorite Color: {color}"
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
        return {"message": "Form submitted, but failed to send email."}
    
    return {"message": "Submitted successfully"}  # Changed from RedirectResponse to JSON
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/submitted")
def submission_status():
    return {"message": "Form submitted successfully!"}
