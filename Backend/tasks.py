from celery import Celery
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os
from dotenv import load_dotenv
from datetime import datetime
import base64
from PIL import Image, ImageOps
from io import BytesIO

load_dotenv()

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Redis should be running
    backend="redis://localhost:6379/0"
)

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Photo Fission",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

@celery.task
def send_email_background(name, email, message):
    fm = FastMail(conf)

    admin_html = f"""
    <h3>📨 New Contact Form Submission</h3>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong><br>{message}</p>
    <p><strong>TimeStamp:</strong><br>{datetime.now().strftime("%H:%M:%S")}</p>
    """

    admin_message = MessageSchema(
        subject="📩 New message from Photo Fission",
        recipients=[os.getenv("ADMIN_EMAIL")],
        body=admin_html,
        subtype=MessageType.html
    )

    user_html = f"""
    <p>Hi <b>{name}</b>,</p>
    <p>Thank you for contacting <b>Photo Fission</b>! 👋</p>
    <p>We've received your message and will get back to you shortly.</p>
    <p><i>Here's what you sent us:</i></p>
    <blockquote>{message}</blockquote>
    <p><strong>TimeStamp:</strong><br>{datetime.now().strftime("%H:%M:%S")}</p>
    <p>Best regards,<br>Photo Fission Team</p>
    """

    user_message = MessageSchema(
        subject="📬 Your message has been received!",
        recipients=[email],
        body=user_html,
        subtype=MessageType.html
    )

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fm.send_message(admin_message))
    loop.run_until_complete(fm.send_message(user_message))


@celery.task
def resize_image(image_data_list):
    counter = 0
    fixed_size = (224, 224)
    results = {
                "Team_A": {},
                "Team_B": {}
            }

    for img_data in image_data_list:
        counter += 1
        filename = img_data["filename"]
        content = img_data["content"]
        
        image = Image.open(BytesIO(content))

        # Convert to RGB if image has alpha channel (RGBA)
        if image.mode == "RGBA":
            image = image.convert("RGB")
        elif image.mode != "RGB":
            image = image.convert("RGB")

        image = ImageOps.fit(image, fixed_size)

        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        b64_img = base64.b64encode(buffer.read()).decode("utf-8")
        if counter >= 4:
            results["Team_B"][filename] = b64_img
        else:
            results["Team_A"][filename] = b64_img

    print(results)

    return results