import uvicorn
from fastapi import FastAPI

from routes.note_route import n_router

app = FastAPI()

app.include_router(n_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8007)