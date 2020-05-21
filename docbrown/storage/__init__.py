import datetime
from typing import Any, Optional, Sequence

from docbrown.models import PassedPhase, Progress, Timings


def _calculate_progress(
        passed_phases: Sequence[PassedPhase],
        timings: Timings,
        now: datetime.datetime) -> Progress:
    expected_duration = sum(timings.values())
    duration = (now - passed_phases[-1].entered_at).total_seconds()
    return Progress(
        expected_duration=expected_duration,
        passed_phases=len(passed_phases),
        expected_phases=len(timings) - 1,
        current_phase=passed_phases[0].phase,
        duration=duration,
        progress=min(100, max(0, duration / expected_duration * 100)),
    )


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
