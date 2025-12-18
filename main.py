from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DATA_FILE = "data/master_data.csv"

@app.get("/", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    df_new = pd.read_excel(file.file)

    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)

    if os.path.exists(DATA_FILE):
        df_old = pd.read_csv(DATA_FILE)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(DATA_FILE, index=False)
    return RedirectResponse("/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if not os.path.exists(DATA_FILE):
        return HTMLResponse("No data uploaded yet")

    df = pd.read_csv(DATA_FILE)

    summary = df.groupby("Profile")[["Total Video", "Total Views"]].sum().reset_index()
    dates = sorted(df["Date"].unique(), reverse=True)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tables": df.tail(50).to_html(index=False),
            "summary": summary.to_dict(orient="records"),
            "dates": dates
        }
    )
