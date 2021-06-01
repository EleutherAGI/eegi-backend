from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func, select
from datetime import datetime
from typing import Any
import uuid

from db import models, pagination
from util import passutil, schemas

class CRUDFilterComparisons:
    def get_comparison(self, comparison_id: str, db: Session):
        """ Get A Single Comparison """
        try:
            data = db.query(models.TextSampleComparison).filter(
                models.TextSampleComparison.id == comparison_id).first()
            return data
        except SQLAlchemyError as e:
            return None

    def get_all_comparisons(self, page_num: int, db: Session) -> Any:
        """ Get All Comparisons"""
        try:
            # data = db.query(models.User).options(defer('password')).all()
            query = db.query(models.TextSampleComparison).order_by(
                models.TextSampleComparison.created_timestamp.desc())
            data = pagination.paginate(query=query, page=page_num,
                                       page_size=100)
            return data
        except SQLAlchemyError as e:
            return None


    def create_comparison(self, comparison: schemas.FilterComparison,
                       db: Session) -> Any:
        """ Create New Comparison """
        try:
            db_comparison = models.TextSampleComparison(id=comparison.id,
                                     user_id=comparison.user_id,
                                     text_sample_id_1=comparison.text_sample_id_1,
                                     text_sample_id_2=comparison.text_sample_id_2,
                                     item_1_is_better=comparison.item_1_is_better)
            db.add(db_comparison)
            db.commit()
            db.refresh(db_comparison)
            return db_comparison
        except SQLAlchemyError as e:
            print(e)
            return None

    def get_random_text_samples(self, num_samples: int, db: Session):
        try:
                        # data = db.query(models.User).options(defer('password')).all()
            data = db.query(models.TextSample).order_by(func.random()).limit(num_samples).all()
            return data
        except SQLAlchemyError as e:
            print(e)




crud_filter_comparisons = CRUDFilterComparisons()