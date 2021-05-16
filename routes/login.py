from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.post("/getToken")
def authenticate_user():
    pass