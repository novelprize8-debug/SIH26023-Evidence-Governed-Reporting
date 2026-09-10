"""Read-only access to normalized, provenance-bearing evidence records."""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = PROJECT_ROOT / "data" / "processed" / "evidence.jsonl"

class EvidenceStore:
    def __init__(self, evidence_path=EVIDENCE_PATH):
        self.evidence_path = Path(evidence_path)
        self.records = self._load()

    def _load(self):
        if not self.evidence_path.exists():
            raise FileNotFoundError(f"Evidence file not found: {self.evidence_path}")
        records = []
        with self.evidence_path.open(encoding="utf-8") as evidence_file:
            for line_number, line in enumerate(evidence_file, 1):
                if not line.strip(): continue
                try: record = json.loads(line)
                except json.JSONDecodeError as error: raise ValueError(f"Invalid evidence JSON on line {line_number}") from error
                required = {"evidence_id", "entity", "metric", "value", "unit", "period", "status", "source_document"}
                if missing := required - record.keys(): raise ValueError(f"Evidence {record.get('evidence_id', line_number)} missing: {', '.join(sorted(missing))}")
                records.append(record)
        return records

    @staticmethod
    def _equals(value, expected): return str(value or "").strip().casefold() == expected.strip().casefold()

    def search(self, entity=None, period=None, coal_type=None, metric=None, mining_method=None):
        results = self.records
        for field, expected in {"entity": entity, "period": period, "coal_type": coal_type, "metric": metric, "mining_method": mining_method}.items():
            if expected is not None: results = [record for record in results if self._equals(record.get(field), expected)]
        return results
