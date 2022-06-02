from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from upscale_image import views

BASE_PATH = Path(__file__).parent.resolve()

app = FastAPI()
app.include_router(views.router)
app.mount("/static", StaticFiles(directory=f"{BASE_PATH}/static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, debug=True)
