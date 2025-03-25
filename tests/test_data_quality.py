import pandas as pd

# Load the processed data
df = pd.read_excel("data/handeled_missing.xlsx")


def test_columns_exist():
    expected_columns = {"sys_created_on", "resolved_at", "category", "priority"}
    assert expected_columns.issubset(df.columns), "Missing required columns"

def test_no_null_values():
    assert df.notnull().all().all(), "Data contains null values"

def test_valid_dates():
    assert (df["resolved_at"] >= df["sys_created_on"]).all(), "Resolved date is before created date"

# Run tests
test_columns_exist()
test_no_null_values()
test_valid_dates()

print("✅ All tests passed!")
 
