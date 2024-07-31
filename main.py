import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

appENV = os.getenv("APP_ENV", "local")

if appENV != "local":
    prefix = "/get-ai-service"
else:
    prefix = "/get-ai"

title = f"get-ai API for {appENV} Environment"
description = f"get-ai api for {appENV} Documentation"


tags_metadata = [
    {
        "name": "get AI",
        "description": "Endpoints to power get-ai",
    }
]

app = FastAPI(
    docs_url= prefix + "/dev/documentation",
    openapi_url=prefix + "/openapi.json",
    title=title,
    description=description,
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(f"{prefix}/")
def root():
    return "Hello World - Welcome to get-ai service"