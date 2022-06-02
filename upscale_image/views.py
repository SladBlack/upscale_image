from pathlib import Path

from fastapi import APIRouter, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from upscale_image.predict import Predict

BASE_PATH = Path(__file__).parent.parent.resolve()
router = APIRouter(prefix="")
templates = Jinja2Templates(directory=f'{BASE_PATH}/templates')


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # return templates.TemplateResponse("/upscale_image/result.html", {"request": request})
    return templates.TemplateResponse("/upscale_image/form.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    errors = []
    prd = Predict(file=file, base_path=BASE_PATH)
    try:
        prd.save_image()
    except ValueError as e:
        return templates.TemplateResponse("/upscale_image/form.html", {"request": request, 'error': e.args[0]})

    prd.save_predict()

    return templates.TemplateResponse("/upscale_image/result.html", {"request": request, "errors": errors})
