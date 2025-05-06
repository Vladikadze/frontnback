from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.post("/submit")
async def handle_form(name: str = Form(...), age: int = Form(...), color: str = Form(...)):
    file_exists = os.path.isfile("answers.csv")

    with open("answers.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Name", "Age", "Favorite Color"])
        writer.writerow([name, age, color])

    return RedirectResponse("/submitted", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/submitted", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("submitted.html", {"request": request})
