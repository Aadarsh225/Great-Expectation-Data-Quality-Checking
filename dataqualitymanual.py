import great_expectations as gx
import pandas as pd

df = pd.DataFrame({
    "Employee_ID": [101, 102, 103, 104, 104],   # duplicate ID
    "Name": ["Aadarsh", "Ram", "Sita", "John", None],   # null name
    "Email": [
        "aadarsh@gmail.com",
        "ram@yahoo.com",
        "invalid_email",      # bad email
        "john@test.com",
        "sita@gmail.com"
    ],
    "Age": [22, 35, 17, 150, 28],   # invalid ages
    "Country": ["Nepal", "India", "USA", "Mars", None],   # bad + null
    "Phone": [
        "9841234567",
        "9800001111",
        "12345",          # bad phone
        "9812345678",
        None
    ],
    "Salary": [50000, 70000, -1000, 200000, 45000],  # negative salary
    "Department": [
        "IT",
        "HR",
        "Finance",
        "Unknown",   # invalid
        "Sales"
    ],
    "Status": [
        "Active",
        "Inactive",
        "Active",
        "Pending",   # invalid
        "Active"
    ],
    "Gender": [
        "Male",
        "Female",
        "Female",
        "Other",
        "Unknown"    # invalid
    ],
    "Rating": [4.5, 3.2, 6.0, -1, 4.0],   # invalid range
    "Join_Date": [
        "2024-01-10",
        "2023-05-15",
        "2024/10/20",   # bad format
        "2025-02-01",
        None
    ]
})

# print(df)

context=gx.get_context()

try:
    context.suites.add(
        gx.ExpectationSuite(name="Details_suite")
    )
except Exception:
    pass

datasource = context.data_sources.add_pandas(
    name="manual_source"
)

asset = datasource.add_dataframe_asset(
    name="employee_data"
)

batch_request=asset.build_batch_request(
    options={"dataframe":df}
)

validator=context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="Details_suite"


)
## Vlidation whether the employee id is unique or not
validator.expect_column_values_to_be_unique("Employee_ID")

## validation wheather name field is null or not

validator.expect_column_values_to_not_be_null("Name")

## Validating wheather all email are valid or not

validator.expect_column_values_to_match_regex(
    "Email",
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

## Validaing the age range between 18 and 100
validator.expect_column_values_to_be_between(
    "Age",
    min_value=18,
    max_value=100
)

## Validating the country allowed or not
validator.expect_column_values_to_be_in_set(
    "Country",
    ["Nepal", "India", "USA", "Canada"]
)

## Validating the phone Length
validator.expect_column_value_lengths_to_be_between(
    "Phone",
    min_value=10,
    max_value=10
)

## Validating the salary wheather it is positive or not

validator.expect_column_values_to_be_between(
    "Salary",
    min_value=0
)

## Validation the department
validator.expect_column_values_to_be_in_set(
    "Department",
    ["IT", "HR", "Finance", "Sales"]
)

## Validating the status
validator.expect_column_values_to_be_in_set(
    "Status",
    ["Active","Inactive"]

)

## validating the gender set
validator.expect_column_values_to_be_in_set(
    "Gender",
    ["Male","Female","Other"]
)

## Validating the rating of the column
validator.expect_column_values_to_be_between(
    "Rating",
    min_value=0,
    max_value=5
)

## validating the date format

validator.expect_column_values_to_match_strftime_format(
    "Join_Date",
    "%Y-%m-%d"
)

results = validator.validate()
print(results)

