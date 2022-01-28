from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import root

app = FastAPI()

allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
