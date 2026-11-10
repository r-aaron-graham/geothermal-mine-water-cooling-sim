"""Compare FIFO dispatch with cooling-aware dispatch for synthetic batch jobs."""

from collections import deque
from dataclasses import dataclass
import json

from simulation import DENSITY_WATER, SPECIFIC_HEAT_WATER


@dataclass(frozen=True)
class Job:
    name: str
    arrival: int
    power_kw: int
    deadline: int  # Inclusive slot in which the job must finish.


# One-hour slots, one worker, and one slot per job.
JOBS = (
    Job("large-a", 0, 360, 2),
    Job("small-a", 0, 100, 0),
    Job("small-b", 1, 120, 1),
    Job("large-b", 2, 410, 4),
    Job("small-c", 2, 90, 3),
)
FLOW_LPS = (18, 22, 52, 24, 68)
INLET_C = (14, 14, 13, 14, 13)
OUTLET_LIMIT_C = 16
BACKUP_COP = 3


def simulate(jobs, flow_lps, inlet_c, cooling_aware, backup_cop):
    waiting = deque()
    finished = []
    trace = []
    compute_kwh = backup_kwh = 0.0

    for slot, (flow, inlet) in enumerate(zip(flow_lps, inlet_c, strict=True)):
        waiting.extend(job for job in jobs if job.arrival == slot)
        capacity_kw = max(0.0, OUTLET_LIMIT_C - inlet) * flow * DENSITY_WATER * SPECIFIC_HEAT_WATER
        if cooling_aware:
            candidates = [job for job in waiting if job.power_kw <= capacity_kw or job.deadline <= slot]
            selected = min(candidates, key=lambda job: job.deadline, default=None)
        else:
            selected = waiting[0] if waiting else None

        auxiliary = 0.0
        if selected is not None:
            waiting.remove(selected)
            finished.append((selected, slot))
            compute_kwh += selected.power_kw
            auxiliary = max(0.0, selected.power_kw - capacity_kw) / backup_cop
            backup_kwh += auxiliary
        trace.append({
            "slot": slot, "cooling_capacity_kw": round(capacity_kw, 2),
            "job": selected.name if selected else None, "backup_kwh": round(auxiliary, 2),
        })

    completed = len(finished)
    energy_kwh = compute_kwh + backup_kwh
    return {
        "completed": completed,
        "deadline_misses": len(jobs) - sum(slot <= job.deadline for job, slot in finished),
        "modeled_energy_kwh": round(energy_kwh, 2),
        "kwh_per_completed_job": round(energy_kwh / completed, 2) if completed else None,
        "trace": trace,
    }


if __name__ == "__main__":
    results = {
        f"backup_cop_{cop}": {
            label: simulate(JOBS, FLOW_LPS, INLET_C, aware, cop)
            for label, aware in (("fifo", False), ("cooling_aware", True))
        }
        for cop in (2, BACKUP_COP, 5)
    }
    print(json.dumps(results, indent=2))
