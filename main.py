from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import subprocess


from app.prompts import print_prompt, digital_prompt
from app.rules import clean_hindi_text


app = FastAPI(title="Hindi News AI Desk")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
return templates.TemplateResponse("index.html", {"request": request})


@app.post("/rewrite")
async def rewrite_news(
content: str = Form(...),
location: str = Form(...),
mode: str = Form(...)
):
content = clean_hindi_text(content)


if mode == "print":
prompt = print_prompt(content, location)
else:
prompt = digital_prompt(content, location)


# Ollama local model call (no API)
result = subprocess.run(
["ollama", "run", "mistral"],
input=prompt,
text=True,
capture_output=True
)


output = result.stdout.strip()
return JSONResponse({"output": output})
