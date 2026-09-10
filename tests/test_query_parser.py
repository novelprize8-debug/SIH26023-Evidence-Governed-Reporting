import pytest

from src.query_parser import parse_query
from src.report_engine import ReportEngine


@pytest.mark.parametrize(
    "period_alias",
    (
        "FY24",
        "FY 24",
        "FY-24",
        "FY2024",
        "financial year 2024",
        "2023/24",
        "2023 / 2024",
        "2023–24",
        "2023 to 2024",
    ),
)
def test_mcl_2023_24_period_aliases_are_normalized(period_alias):
    parsed = parse_query(f"How much raw coal did MCL produce in {period_alias}?")

    assert parsed["period"] == "2023-24"


def test_mcl_coal_output_alias_for_supported_production_period():
    parsed = parse_query("Tell me MCL's coal output for FY 2023-24.")

    assert parsed["metric"] == "Raw Coal Production"


def test_ambiguous_period_keeps_needs_clarification_behavior():
    response = ReportEngine().answer("How much raw coal did MCL produce in FY?")

    assert response["status"] == "needs_clarification"
    assert "period" in response["message"]
