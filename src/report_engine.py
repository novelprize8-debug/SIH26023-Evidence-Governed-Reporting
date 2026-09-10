"""Evidence-led answers. No language model or generated value is used as evidence."""
from decimal import Decimal
from .evidence_store import EvidenceStore
from .query_parser import parse_query
from .reconcile import Evidence, reconcile

def to_evidence(record):
    return Evidence(**{key: record.get(key) for key in Evidence.__dataclass_fields__})

def public_record(record):
    fields = ("evidence_id", "entity", "metric", "value", "unit", "period", "mining_method", "coal_type", "status", "source_document", "source_publisher", "publication_date", "page", "table", "source_location", "extraction_method", "notes")
    return {field: record.get(field) for field in fields}

class ReportEngine:
    def __init__(self, evidence_path=None): self.store = EvidenceStore(evidence_path) if evidence_path else EvidenceStore()

    def _derived_parliament_total(self, parsed):
        components = self.store.search(entity=parsed["entity"], period=parsed["period"], coal_type="Non-Coking", metric=parsed["metric"])
        oc = next((item for item in components if item.get("source_document", "").startswith("Lok Sabha") and item.get("mining_method") == "OC" and item.get("status") == "reported"), None)
        ug = next((item for item in components if item.get("source_document", "").startswith("Lok Sabha") and item.get("mining_method") == "UG" and item.get("status") == "reported"), None)
        if not oc or not ug or oc["unit"] != ug["unit"]: return None
        total = Decimal(str(oc["value"])) + Decimal(str(ug["value"]))
        return {"value": float(total), "unit": oc["unit"], "status": "derived", "coal_type": "Non-Coking", "source_document": oc["source_document"], "calculation": {"operation": "sum", "expression": f"{oc['value']} + {ug['value']} = {total}", "input_evidence_ids": [oc["evidence_id"], ug["evidence_id"]]}, "components": [public_record(oc), public_record(ug)]}

    def answer(self, question):
        parsed = parse_query(question)
        missing = [field for field in ("entity", "metric", "period") if parsed[field] is None]
        base = {"question": question, "query": parsed, "evidence": [], "reconciliation": [], "calculation": None}
        if missing: return {**base, "status": "needs_clarification", "message": f"The question cannot be interpreted reliably. Missing: {', '.join(missing)}."}
        results = self.store.search(entity=parsed["entity"], period=parsed["period"], coal_type=parsed["coal_type"], metric=parsed["metric"])
        derived = self._derived_parliament_total(parsed) if parsed["coal_type"] == "Total" else None
        if not results and not derived: return {**base, "status": "insufficient_evidence", "message": "Insufficient evidence to answer reliably. No matching verified evidence was found."}
        reconciliation = []
        if derived:
            directory = next((record for record in self.store.search(entity=parsed["entity"], period=parsed["period"], coal_type="Non-Coking", metric=parsed["metric"]) if "coal_directory" in record["source_document"].casefold()), None)
            if directory:
                comparison = reconcile(to_evidence(directory), Evidence(entity=parsed["entity"], metric=parsed["metric"], value=derived["value"], unit=derived["unit"], period=parsed["period"], coal_type="Non-Coking", status="derived", source_document=derived["source_document"]))
                reconciliation.append({"scope": "Non-Coking production", "left": public_record(directory), "right": {"value": derived["value"], "unit": derived["unit"], "status": "derived", "source_document": derived["source_document"]}, **comparison})
        reported = next((record for record in results if record.get("status") == "reported"), None)
        answer_text = f"{reported['value']} {reported['unit']} — directly reported in {reported['source_document']}." if reported else f"{derived['value']} {derived['unit']} — derived from verified component evidence; not directly reported as a total."
        return {**base, "status": "answered", "message": answer_text, "evidence": [public_record(record) for record in results], "reconciliation": reconciliation, "calculation": derived}
