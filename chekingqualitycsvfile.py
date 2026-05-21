import great_expectations as gx
import pandas as pd

# Read CSV
df = pd.read_csv("ecommerce_transactions.csv")

# GX context
context = gx.get_context()

# Create suite
try:
    context.suites.add(
        gx.ExpectationSuite(name="transaction_suite")
    )
except Exception:
    pass

# Datasource
datasource = context.data_sources.add_pandas(
    name="csv_source"
)

# Data asset
asset = datasource.add_dataframe_asset(
    name="transactions"
)

# Batch request
batch_request = asset.build_batch_request(
    options={"dataframe": df}
)

# Validator
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="transaction_suite"
)

# Expectations
validator.expect_column_values_to_not_be_null("Transaction_ID")
validator.expect_column_values_to_be_unique("Transaction_ID")
validator.expect_column_values_to_be_between(
    "Purchase_Amount",
    min_value=0
)
validator.expect_column_values_to_be_between(
    "Age",
    min_value=18,
    max_value=100
)
validator.expect_column_values_to_match_strftime_format(
    "Transaction_Date",
    "%Y-%m-%d"
)

# Save suite
context.suites.add_or_update(
    validator.expectation_suite
)

# Run validation
results = validator.validate()

print(results)