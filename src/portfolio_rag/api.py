"""Factory for integrating with an existing FastAPI process."""
import asyncio
from fastapi import FastAPI
from .public import install_public
def create_app(service):
    app=FastAPI(docs_url=None,redoc_url=None,openapi_url=None)
    install_public(app,service,asyncio.Semaphore(1))
    return app
