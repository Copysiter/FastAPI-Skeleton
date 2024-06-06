from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Index  # noqa

from db.base_class import Base  # noqa


class Metric(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    prefix = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)
    key = Column(String, nullable=False, index=True)
    value = Column(Integer)
    host = Column(String, nullable=True, index=True)
    timestamp = Column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    idx_prefix_name_type = Index(
        'idx_multi_column',
        prefix, type, key, host, unique=True
    )
