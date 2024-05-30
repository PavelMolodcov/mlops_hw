import os
from datetime import datetime

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from src.scorer import make_pred

app = FastAPI()
templates = Jinja2Templates(directory="templates")
input_directory = "input"
output_directory = "output"


@app.get("/upload", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_location = os.path.join(input_directory, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    print(file_location)
    submission, json_path, jpg_path = make_pred(file_location)

    # Генерация имени файла с текущей датой и временем
    timestamp = datetime.now().strftime("%Y.%m.%d_%H:%M")
    output_filename = f"{timestamp}_submit.csv"
    output_file = os.path.join(output_directory, output_filename)

    submission.to_csv(output_file, index=False)
    os.remove(file_location)

    # Получение базовых названий файлов без директорий
    json_filename = os.path.basename(json_path)
    jpg_filename = os.path.basename(jpg_path)

    return templates.TemplateResponse(
        "download.html",
        {
            "request": request,
            "files": [output_filename],
            "json_file": json_filename,
            "jpg_file": jpg_filename,
        },
    )


@app.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str):
    file_path = os.path.join(output_directory, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    else:
        return {"error": "File not found"}
