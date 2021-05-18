from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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

    def update_comparison(self, comparison_id: str, item_1_is_better: bool,
                    db: Session) -> Any:
        """ Update Comparison"""
        try:
            
            db_comparison = db.query(models.TextSampleComparison).filter(
                models.TextSampleComparison.id == comparison_id).first()



            db_comparison.item_1_is_better = item_1_is_better
            
            db.commit()
            db.refresh(db_comparison)
            return db_comparison
        except SQLAlchemyError as e:
            return None

        
    def update_comparison(self, comparison_id: str, item_1_is_better: bool,
                    db: Session) -> Any:
        """ Update Comparison"""
        try:
            
            db_comparison = db.query(models.TextSampleComparison).filter(
                models.TextSampleComparison.id == comparison_id).first()

            db_comparison.item_1_is_better = item_1_is_better

            db.commit()
            db.refresh(db_comparison)
            return db_comparison
        except SQLAlchemyError as e:
            return None


    def create_article(self, article: schemas.FilterSampleCreate,
                       db: Session) -> Any:
        """ Create New Article """
        try:
            uid = str(uuid.uuid4().hex)
            db_user = models.TextSampleComparison(id=uid,
                                     user_id=article.user_id,
                                     text_sample_id_1=article.text_sample_id_1,
                                     text_sample_id_2=article.text_sample_id_2)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            return None





crud_filter_comparisons = CRUDFilterComparisons()