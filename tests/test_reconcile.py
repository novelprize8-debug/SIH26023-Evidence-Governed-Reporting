from src.reconcile import Evidence, reconcile

def test_consistent():
    a = Evidence("MCL", "Coal Production", 100, "MT", "2024-25", "OC", "G10", "Actual", "a.pdf", 10, "T1")
    b = Evidence("Mahanadi Coalfields Limited", "Coal Production", 100, "MT", "2024-25", "OC", "G10", "Actual", "b.pdf", 12, "T2")
    # Entity aliases are not yet resolved in this v1 scaffold, so this intentionally
    # documents a future requirement rather than assuming aliasing works.
    assert reconcile(a, b)["status"] == "not_comparable"

def test_status_difference():
    a = Evidence("MCL", "Coal Production", 100, "MT", "2024-25", "OC", "G10", "Provisional")
    b = Evidence("MCL", "Coal Production", 102, "MT", "2024-25", "OC", "G10", "Actual")
    assert reconcile(a, b)["status"] == "potentially_explainable_difference"

def test_unresolved_conflict():
    a = Evidence("MCL", "Coal Production", 100, "MT", "2024-25", "OC", "G10", "Actual")
    b = Evidence("MCL", "Coal Production", 106, "MT", "2024-25", "OC", "G10", "Actual")
    assert reconcile(a, b)["status"] == "unresolved_conflict"
