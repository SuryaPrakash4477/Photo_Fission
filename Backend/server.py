from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, EmailStr
from tasks import send_email_background, sort_images
import os
from celery.result import AsyncResult
app = FastAPI()

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.post("/team_name")
async def sortImage_based_teamName(files: list[UploadFile] = File(...)):
    """API to sort image according to the team name!!"""
    image_data = []
    for file in files:
        content = await file.read()
        image_data.append({
            "filename": file.filename,
            "content": content
        })
    task = sort_images.delay(image_data)
    res = AsyncResult(task.id, app=sort_images)
    # if res.ready():

    return {"task_id": task.id, "msg": "Resizing in Progress"}


@app.post("/jersey_number")
async def sortImage_based_jerseyNumber(files: list[UploadFile] = File(...)):
    """API to sort image according to the jersey number!!"""
    task = sort_images.delay([await f.read() for f in files], [f.filename for f in files])
    return {"task_id": task.id, "msg": "Resizing in Progress"}

@app.post("/send_msg")
async def send_contact_email(data: ContactForm):
    send_email_background.delay(data.name, data.email, data.message)
    return {"message": "Email is being sent in the background"}


@app.get("/get_images/{task_id}")
def get_task_result(task_id: str):
    res = AsyncResult(task_id, app=sort_images)
    if res.ready():
        return {"status": "done", "images": res.result}
    return {"status": "processing"}
