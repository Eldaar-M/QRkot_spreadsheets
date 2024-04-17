from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.constants import INVESTED_AMOUNT_DEFAULT
from app.core.db import Base


class DonationProjectBaseModel(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            'full_amount >= invested_amount'
        ),
        CheckConstraint(
            'invested_amount >= 0'
        ),
        CheckConstraint('full_amount > 0'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=INVESTED_AMOUNT_DEFAULT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
