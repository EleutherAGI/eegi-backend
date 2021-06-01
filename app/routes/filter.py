from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uuid

from util import deps, schemas, response_schemas
from crud import crud_filter_comparisons

router = APIRouter()


@router.get("/comparisons", responses=response_schemas.all_filter_comparison_responses)
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

@router.get("/comparisons/sample_pair", responses=response_schemas.create_filter_comparison)
def get_samples(db: Session = Depends(deps.get_db),
                  current_user: schemas.UserVerify = Depends(
                      deps.get_current_user)) -> JSONResponse:
    """ Generate new comparison Comparisons"""
    
    sample1, sample2 = crud_filter_comparisons.get_random_text_samples(num_samples = 2, db=db)

    return JSONResponse(status_code=200,
                        content={"text_sample_1": sample1.text,
                                 "text_sample_2": sample2.text,
                                 "text_id_1": sample1.id,
                                 "text_id_2": sample2.id})

@router.post("/comparisons", responses=response_schemas.general_responses)
def create_comparison(comparison_update: schemas.FilterComparisonCreate,
                  db: Session = Depends(deps.get_db),
                  current_user: schemas.UserVerify = Depends(
                      deps.get_current_user)) -> JSONResponse:
    """ Update A Comparison with preference"""
    
    comparison = schemas.FilterComparison(
        text_sample_id_1 = comparison_update.text_sample_id_1, 
        text_sample_id_2 = comparison_update.text_sample_id_2, 
        item_1_is_better = comparison_update.item_1_is_better,
        user_id = current_user.id,
        id = str(uuid.uuid4().hex)
        )


    data = crud_filter_comparisons.create_comparison(comparison=comparison, db=db)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})