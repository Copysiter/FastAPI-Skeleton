from typing import List, Optional, Literal  # noqa
from datetime import datetime

from pydantic import BaseModel


class MetricBase(BaseModel):
    id: int
    prefix: str
    type: Literal['time', 'count', 'gauge']
    key: str
    value: int
    host: Optional[str] = None
    timestamp: datetime


class MetricCreate(MetricBase):
    pass


class MetricUpdate(MetricBase):
    pass


class Metric(MetricBase):
    pass


class MetricRows(BaseModel):
    key: str
    type: str
    value: int
    timestamp: datetime
    metrics: List[Metric]
