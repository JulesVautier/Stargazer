"""
V1 of cresus API
"""

from fastapi import APIRouter

from . import api

api_router = APIRouter()

api_router.include_router(api.router)
