from crud.base import CRUDBase  # noqa
from models import Metric  # noqa
from schemas.metric import MetricCreate, MetricUpdate  # noqa


class CRUDMetric(CRUDBase[Metric, MetricCreate, MetricUpdate]):
    pass


metric = CRUDMetric(Metric)
