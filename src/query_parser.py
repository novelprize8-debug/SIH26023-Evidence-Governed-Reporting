"""Conservative rule-based query understanding for the MVP corpus."""
import re


ENTITY_ALIASES = {"mcl": "MCL", "mahanadi coalfields": "MCL", "mahanadi coalfields limited": "MCL"}
PERIOD_PATTERN = re.compile(r"\b(20\d{2})\s*[-–—]\s*(\d{2})\b")
MCL_2023_24_PERIOD_ALIASES = (
    re.compile(r"\b(?:fy|financial\s+year)\s*[-/]?\s*(?:24|2024)\b", re.IGNORECASE),
    re.compile(r"\b2023\s*(?:[-–—/]|to)\s*(?:24|2024)\b", re.IGNORECASE),
)


def _parse_period(query):
    """Resolve only unambiguous aliases for the seeded 2023-24 fiscal year."""
    if any(pattern.search(query) for pattern in MCL_2023_24_PERIOD_ALIASES):
        return "2023-24"
    period_match = PERIOD_PATTERN.search(query)
    return f"{period_match.group(1)}-{period_match.group(2)}" if period_match else None


def parse_query(query):
    text = query.casefold()
    entity = next((canonical for alias, canonical in ENTITY_ALIASES.items() if alias in text), None)
    period = _parse_period(query)
    coal_type = "Non-Coking" if re.search(r"non[ -]?coking", text) else "Coking" if "coking" in text else "Total"
    is_mcl_coal_output = entity == "MCL" and period is not None and re.search(r"\bcoal\s+output\b", text)
    metric = "Raw Coal Production" if is_mcl_coal_output or any(word in text for word in ("production", "produce", "produced", "raw coal")) else None
    return {"original_query": query, "entity": entity, "metric": metric, "period": period, "coal_type": coal_type}
