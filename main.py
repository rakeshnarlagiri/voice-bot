from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv


load_dotenv()
host = "127.0.0.1"
port = 8000

app = FastAPI()


templates = Jinja2Templates(directory="templates")


# Load Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

# Your Twilio Function URL
TWILIO_FUNCTION_URL = "https://lion-dragonfly-4688.twil.io/voice"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/call/start")
async def start_call(to: str = Form(...)):
    """
    Initiates outbound call using your Twilio Function as webhook
    """
    call = client.calls.create(
        to=to,
        from_=twilio_number,
        url=TWILIO_FUNCTION_URL   # <-- THIS triggers your Twilio voice function
    )

    return JSONResponse({"message": "Call initiated", "call_sid": call.sid})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=port)

    
