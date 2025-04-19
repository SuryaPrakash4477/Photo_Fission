from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, EmailStr
from tasks import send_email_background
import os
app = FastAPI()

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SORTED_FOLDER = os.path.join(BASE_DIR, "Sorted_Images")
os.makedirs(SORTED_FOLDER, exist_ok=True)

@app.post("/team_name")
async def sortImage_based_teamName(files: list[UploadFile] = File(...)):
    """API to sort image according to the team name!!"""
    if files:
        for file in files:
            file_bytes = await file.read()
            file_path = os.path.join(SORTED_FOLDER, file.filename)
            with open(file_path, "wb") as f:
                f.write(file_bytes)
    return {"msg":"Got your photos and it is under process"}

@app.post("/send_msg")
async def send_contact_email(data: ContactForm):
    send_email_background.delay(data.name, data.email, data.message)
    return {"message": "Email is being sent in the background"}
