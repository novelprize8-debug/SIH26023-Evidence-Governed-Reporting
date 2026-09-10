"""CLI view of the seeded cross-source MCL validation case."""
from .report_engine import ReportEngine

if __name__ == "__main__":
    response = ReportEngine().answer("How much raw coal did MCL produce in 2023-24?")
    print(response["message"])
    print("Calculation:", response["calculation"]["calculation"]["expression"])
    print("Reconciliation:", response["reconciliation"][0]["status"])
