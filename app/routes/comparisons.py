from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.post("/")
def get_comparison():
    pass

@router.post("/{comparison_id}")
def submit_comparison():
    pass