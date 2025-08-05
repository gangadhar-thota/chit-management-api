from fastapi import APIRouter, Depends
from app.utils.auth import get_current_user

def get_authenticated_router(*args, **kwargs):
    router = APIRouter(*args, dependencies=[Depends(get_current_user)], **kwargs)
    return router
