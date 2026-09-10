from dataclasses import dataclass
from itertools import combinations
from typing import Optional

@dataclass(frozen=True)
class Evidence:
    entity: str; metric: str; value: float; unit: str; period: str
    mining_method: Optional[str] = None; coal_type: Optional[str] = None; status: Optional[str] = None
    source_document: str = ""; page: Optional[int] = None; table: Optional[str] = None

def comparable_key(e):
    return tuple((value or "").strip().casefold() for value in (e.entity, e.metric, e.period, e.unit, e.mining_method, e.coal_type))

def reconcile(a, b):
    if comparable_key(a) != comparable_key(b): return {"status": "not_comparable", "reason": "Entity, metric, period, unit, mining method, or coal type differs."}
    if a.value == b.value:
        if (a.status or "").casefold() == (b.status or "").casefold(): return {"status": "consistent", "reason": "Comparable values and reporting status agree."}
        return {"status": "consistent", "reason": "Comparable values agree; reporting status differs and is retained.", "reporting_status_difference": True}
    if (a.status or "").casefold() != (b.status or "").casefold(): return {"status": "potentially_explainable_difference", "reason": "Comparable values differ and reporting status differs.", "values": [a.value, b.value], "statuses": [a.status, b.status]}
    return {"status": "unresolved_conflict", "reason": "Comparable records have different values with the same reporting status.", "values": [a.value, b.value]}

def reconcile_all(records):
    return [{"left_source": left.source_document, "right_source": right.source_document, **reconcile(left, right)} for left, right in combinations(records, 2)]
