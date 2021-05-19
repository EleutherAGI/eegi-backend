import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from ..dbconf import Base
from datetime import datetime

from .users import User

class BinaryComparisonBase:
    item_1_is_better = Column(Boolean)

    @hybrid_property
    def is_pending(self):
        return self.item_1_is_better == None

class TextSample(Base):
    __tablename__ = "text_samples"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    @property
    def text_sample_comparisons(self):
        return self.text_sample_comparisons_from_1 + self.text_sample_comparisons_from_2


class TextSampleComparison(Base, BinaryComparisonBase):
    __tablename__ = "text_sample_comparisons"

    id = Column(String, primary_key=True, index=True)
    text_sample_id_1 = Column(Integer, ForeignKey("text_samples.id"), nullable=False)
    text_sample_id_2 = Column(Integer, ForeignKey("text_samples.id"), nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"))

    text_sample_1 = relationship("TextSample", foreign_keys=[text_sample_id_1], backref="text_sample_comparisons_from_1")
    text_sample_2 = relationship("TextSample", foreign_keys=[text_sample_id_2], backref="text_sample_comparisons_from_2")
    user = relationship("User", backref="text_sample_comparisons")
    


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    text_sample_id = Column(Integer, ForeignKey("text_samples.id"), nullable=False)
    summary = Column(String, nullable=False)
    text_sample = relationship("TextSample", backref="summaries")

    @property
    def comparisons(self):
        return self.comparisons_from_1 + self.comparisons_from_2


class SummaryComparison(Base, BinaryComparisonBase):
    __tablename__ = "summary_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    text_id = Column(Integer, ForeignKey("text_samples.id"), nullable=False)
    summary_id_1 = Column(Integer, ForeignKey("summaries.id"), nullable=False)
    summary_id_2 = Column(Integer, ForeignKey("summaries.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"))

    text_sample = relationship("TextSample", backref="summary_comparisons")
    summary_1 = relationship("Summary", foreign_keys=[summary_id_1], backref="comparisons_from_1")
    summary_2 = relationship("Summary", foreign_keys=[summary_id_2], backref="comparisons_from_2")
    user = relationship("User", backref="summary_comparisons")
    created_timestamp = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)

    # TODO add validate that both summaries refer to the same text sample
    @validates("summary_1")
    def validate_summary_1(self, key, summary):
        self.validate_summaries(summary, self.summary_2)
        return summary

    @validates("summary_2")
    def validate_summary_2(self, key, summary):
        self.validate_summaries(summary, self.summary_1)
        return summary

    def validate_summaries(self, summary_1, summary_2):
        if (summary_1 is not None
                and summary_2 is not None
                and summary_1.text_sample_id != summary_2.text_sample_id):
            raise ValueError("Summaries don't refer to the same text sample")
