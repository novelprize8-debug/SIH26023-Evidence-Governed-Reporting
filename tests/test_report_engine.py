from src.report_engine import ReportEngine

def test_mcl_2023_answer_keeps_reported_and_derived_separate():
    response = ReportEngine().answer("How much raw coal did MCL produce in 2023-24?")
    assert response["status"] == "answered"
    assert response["evidence"][0]["value"] == 206.099 and response["evidence"][0]["status"] == "reported"
    assert response["calculation"]["status"] == "derived"
    assert response["calculation"]["calculation"]["expression"] == "205.643 + 0.456 = 206.099"
    assert response["reconciliation"][0]["status"] == "consistent"
    assert response["reconciliation"][0]["reporting_status_difference"] is True
def test_refuses_query_without_evidence():
    response = ReportEngine().answer("How much raw coal did MCL produce in 2021-22?")
    assert response["status"] == "insufficient_evidence" and response["evidence"] == []
def test_requires_reliable_query_context():
    response = ReportEngine().answer("How much coal was produced?")
    assert response["status"] == "needs_clarification" and "entity" in response["message"]
