import datetime
from typing import Any, Optional

from docbrown.models import Progress, Timings


class StorageBackend:
    def store_timings(self, ident, aggregator_key: str, timings: Timings) -> None:
        raise NotImplementedError()

    def store_progress(self, ident: str, aggregator_key: str, phase: str,
                       entered_at: datetime.datetime) -> None:
        raise NotImplementedError()

    def clear_progress(self, ident: str) -> None:
        raise NotImplementedError()

    def get_progress(self, ident: str, aggregator_func: Any) -> Optional[Progress]:
        raise NotImplementedError()
