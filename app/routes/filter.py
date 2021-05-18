from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from enum import Enum

from util import deps, schemas, response_schemas
from crud import crud_filter_comparisons

router = APIRouter()


@router.get("/comparisons", responses=response_schemas.general_responses)
def get_comparisons(comparison_id: int = None, page_num: int = 1,
                  db: Session = Depends(deps.get_db),
                  current_user: schemas.UserVerify = Depends(
                      deps.get_current_user)) -> JSONResponse:
                      
    """ Return All Comparisons"""
    if comparison_id is not None:
        db_comparison = crud_filter_comparisons.get_comparison(id=comparison_id, db=db)
        if db_comparison is None:
            return JSONResponse(status_code=500,
                                content={"message": "No Comparison Found"})
        json_compatible_item_data = jsonable_encoder(db_comparison)
        return JSONResponse(status_code=200,
                            content=json_compatible_item_data)
    else:
        db_comparison = crud_filter_comparisons.get_all_comparisons(page_num=page_num, db=db)
        if db_comparison is None:
            return JSONResponse(status_code=500,
                                content={"message": "No Comparisons Found"})
        json_compatible_item_data = jsonable_encoder(db_comparison)
        return JSONResponse(status_code=200,
                            content={"total_pages": db_comparison.pages,
                                     "total_items": db_comparison.total_items,
                                     "page_data": {"page_num": page_num,
                                                   "item_count": db_comparison.page_size,
                                                   "items":
                                                       json_compatible_item_data}})

@router.post("/comparisons", responses=response_schemas.general_responses)
def generate_comparison(user: schemas.UserCreate,
                  db: Session = Depends(deps.get_db),
                  current_user: schemas.UserVerify = Depends(
                      deps.get_current_user)) -> JSONResponse:
    """ Generate new comparison Comparisons"""

    # TODO: implement way to load dummy data into the database
    # So we can start generating comparisons

    pass

@router.put("/comparisons", responses=response_schemas.general_responses)
def update_comparison(item_1_is_better: bool, comparison_id: str,
                  db: Session = Depends(deps.get_db),
                  current_user: schemas.UserVerify = Depends(
                      deps.get_current_user)) -> JSONResponse:
    """ Update A Comparison with preference"""

    data = crud_filter_comparisons.update_comparison(comparison_id=comparison_id, 
                                                     item_1_is_better=item_1_is_better, 
                                                     db=db)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})