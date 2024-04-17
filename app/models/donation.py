from sqlalchemy import Column, ForeignKey, Integer, Text

from app.constants import FOREIGN_KEY_USER_ID
from app.models.base import DonationProjectBaseModel


class Donation(DonationProjectBaseModel):
    user_id = Column(Integer, ForeignKey(FOREIGN_KEY_USER_ID))
    comment = Column(Text, nullable=True)
