from kafka import KafkaConsumer
import json
# from app.notify import send_email_background
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

import asyncio
from typing import Dict

consumer = KafkaConsumer(
    "send_notification",
    bootstrap_servers="localhost:9093",
    api_version=(0, 10, 2),
    # auto_offset_reset="earliest",  # or "latest"
    enable_auto_commit=True,
    group_id="my-python-consumer-groups",
    key_deserializer=lambda k: json.loads(k.decode("utf-8")) if k else None,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)
conf = ConnectionConfig(
    MAIL_USERNAME="shrushtikale5@gmail.com",
    MAIL_PASSWORD="znuh ibfj iqil lzjv",
    MAIL_FROM="shrushtikale5@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    # MAIL_SSL=False,
    USE_CREDENTIALS=True
)

location_emails: Dict[str, str] = {
    "newyork": ["shrushtikale5@gmail.com","hiteshkale1@gmail.com"],
    "manhattan": ["hiteshkale1@gmail.com"]

}


print("⏳ Waiting for messages...")

async def send_email_background(area:str):
    if area.lower() in location_emails:
        recipients =location_emails[area]
        message = MessageSchema(
            subject= "downtown alert",
            recipients=recipients,
            body= f"Notification for {area}",
            subtype="plain"

        )
        fm = FastMail(conf)
        print("email sent")
        await fm.send_message(message)


async def process_message(message):
    try:
        area = message.value.get('area')
        if area:
            await send_email_background(area)
        else:
            print("mising fields")
    except Exception as e:
        print(e)


for message in consumer:
    # send_email()
    asyncio.run(process_message(message))
    print(f"✅ New message | Key: {message.key}, Value: {message.value}, Partition: {message.partition}")