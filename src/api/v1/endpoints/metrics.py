from typing import Any, List, Dict, Optional  # noqa

from fastapi import APIRouter, Depends, Body, HTTPException, status  # noqa
from sqlalchemy.ext.asyncio import AsyncSession

from api import deps  # noqa

import crud, models, schemas  # noqa


router = APIRouter()


@router.get('/metrics', response_model=schemas.MetricRows)
async def get_metrics(
    db: AsyncSession = Depends(deps.get_db), *,
    key: str, type: str,
) -> Any:
    """
    Retrieve metrics.
    """
    filters = [
        {'field': 'type', 'operator': 'eq', 'value': type},
        {'field': 'key', 'operator': 'eq', 'value': key}
    ]
    metrics = await crud.metric.get_rows(
        db, filters=filters
    )
    if not metrics:
        raise HTTPException(status_code=404, detail='Metrics not found')
    if type == 'timer':
        value = sum([m.value for m in metrics]) / len(metrics)
    else:
        value = sum([m.value for m in metrics])
    timestamp = max([m.timestamp for m in metrics])

    return {
        'key': key, 'type': type, 'value': value,
        'timestamp': timestamp, 'metrics': metrics
    }
