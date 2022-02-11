from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .routers import root, auth, label, category, subcategory, transaction
from .config.env import environment_variables

app = FastAPI()

allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware, secret_key=environment_variables.SESSION_SECRET_KEY
)

app.include_router(root.router)
app.include_router(auth.router)
app.include_router(label.router)
app.include_router(category.router)
app.include_router(subcategory.router)
app.include_router(transaction.router)
