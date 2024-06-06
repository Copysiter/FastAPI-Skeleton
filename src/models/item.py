from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String  # noqa
from sqlalchemy.orm import relationship

from db.base_class import Base  # noqa

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='items', lazy='joined')
