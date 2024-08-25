from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import appENV
from app.routes import product_routes, user_routes, common_routes  # Import routes


## Define API prefix based on environment
if appENV != "local":
    prefix = "/get-ai-service"
else:
    prefix = "/get-ai"

## Set API documentation details
title = f"get-ai API for {appENV} Environment"
description = f"get-ai API for {appENV} Documentation"

tags_metadata = [
    {
        "name": "get AI",
        "description": "Endpoints to power get-ai",
    }
]

## Initialize FastAPI app
app = FastAPI(
    docs_url=prefix + "/dev/documentation",
    openapi_url=prefix + "/openapi.json",
    title=title,
    description=description,
    openapi_tags=tags_metadata,
)

## Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(product_routes.router, prefix=prefix+"/products", tags=["Products"])
app.include_router(user_routes.router, prefix=prefix+"/users", tags=["Users"])
app.include_router(common_routes.router, prefix=prefix+"/common", tags=["common"])