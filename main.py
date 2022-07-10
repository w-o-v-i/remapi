from twilio.rest import Client
from fastapi import FastAPI
import uvicorn
import datetime, time, multiprocessing
import os


# FastAPI Instance
app = FastAPI()


# Twilio Configuration
account_sid = "AC88603386194b4e37bbdfa4d1fb3f746d"
auth_token = "8c7c3797d16e387370d8121cb0149760"
client = Client(account_sid, auth_token)


def send_whatsapp_message(message, phone_number):
    message = client.messages.create(
        from_="whatsapp:+14155238886", body=message, to="whatsapp:" + phone_number
    )
    return message.sid


# Set Reminder Endpoint
@app.get("/reminder/{phone_number}/{message}/{time}")
def set_reminder(phone_number: str, message: str, time: str):
    dirName = f"{time}_{phone_number}_{message}"
    print("...Creating Folder...")
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("...Folder Created...")


def check_reminder():
    while True:
        for folder in os.listdir():
            if folder.startswith(
                datetime.datetime.now().strftime("%H:%M").replace(":", "")
            ):
                phone_number = folder.split("_")[1]
                message = folder.split("_")[2]
                send_whatsapp_message(message, phone_number)
                os.rmdir(folder)
        time.sleep(1)


if __name__ == "__main__":

    p = multiprocessing.Process(target=check_reminder)
    p.start()

    uvicorn.run(app, host="0.0.0.0", port=80)
