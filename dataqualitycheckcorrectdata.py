import pandas as pd
import great_expectations as gx

df = pd.DataFrame({
    "Hero_ID": [
        1001,1002,1003,1004,1005,
        1006,1007,1008,1009,1010,
        1011,1012,1013,1014,1015,
        1016,1017,1018,1019,1020
    ],

    "Hero_Name": [
        "Iron Man","Captain America","Thor","Hulk","Black Widow",
        "Spider-Man","Doctor Strange","Wolverine","Deadpool","Loki",
        "Batman","Superman","Wonder Woman","Flash","Aquaman",
        "Green Lantern","Cyborg","Robin","Nightwing","Shazam"
    ],

    "Real_Name": [
        "Tony Stark","Steve Rogers","Thor Odinson","Bruce Banner","Natasha Romanoff",
        "Peter Parker","Stephen Strange","Logan","Wade Wilson","Loki Laufeyson",
        "Bruce Wayne","Clark Kent","Diana Prince","Barry Allen","Arthur Curry",
        "Hal Jordan","Victor Stone","Dick Grayson","Richard Grayson","Billy Batson"
    ],

    "Email": [
        "tony.stark@marvel.com",
        "steve.rogers@marvel.com",
        "thor@marvel.com",
        "bruce.banner@marvel.com",
        "natasha@marvel.com",
        "peter.parker@marvel.com",
        "strange@marvel.com",
        "logan@marvel.com",
        "wade@marvel.com",
        "loki@marvel.com",
        "bruce.wayne@dc.com",
        "clark.kent@dc.com",
        "diana@dc.com",
        "barry@dc.com",
        "arthur@dc.com",
        "hal.jordan@dc.com",
        "victor@dc.com",
        "robin@dc.com",
        "nightwing@dc.com",
        "billy@dc.com"
    ],

    "Universe": [
        "Marvel","Marvel","Marvel","Marvel","Marvel",
        "Marvel","Marvel","Marvel","Marvel","Marvel",
        "DC","DC","DC","DC","DC",
        "DC","DC","DC","DC","DC"
    ],

    "Age": [
        45,105,1500,50,35,
        21,42,137,38,1000,
        40,38,3000,28,34,
        36,33,22,30,29
    ],

    "Gender": [
        "Male","Male","Male","Male","Female",
        "Male","Male","Male","Male","Male",
        "Male","Male","Female","Male","Male",
        "Male","Male","Male","Male","Male"
    ],

    "Phone": [
        "9841234501","9841234502","9841234503","9841234504","9841234505",
        "9841234506","9841234507","9841234508","9841234509","9841234510",
        "9841234511","9841234512","9841234513","9841234514","9841234515",
        "9841234516","9841234517","9841234518","9841234519","9841234520"
    ],

    "Power_Level": [
        90,85,99,98,80,
        88,92,91,87,89,
        95,97,94,86,83,
        84,82,75,81,93
    ],

    "City": [
        "New York","Brooklyn","Asgard","Unknown","Moscow",
        "Queens","New York","Canada","New York","Asgard",
        "Gotham","Metropolis","Themyscira","Central City","Atlantis",
        "Coast City","Detroit","Gotham","Bludhaven","Philadelphia"
    ],

    "Team": [
        "Avengers","Avengers","Avengers","Avengers","Avengers",
        "Avengers","Avengers","X-Men","X-Force","Asgardians",
        "Justice League","Justice League","Justice League","Justice League","Justice League",
        "Justice League","Teen Titans","Bat Family","Titans","Justice League"
    ],

    "Experience_Years": [
        20,80,1200,25,15,
        5,18,100,12,900,
        18,15,2500,8,10,
        12,9,6,11,7
    ],

    "Mission_Success_Rate": [
        95.5,94.2,99.8,90.0,89.5,
        91.0,96.7,88.9,85.5,93.3,
        97.2,98.1,99.4,92.7,87.8,
        89.1,84.6,80.2,86.9,93.5
    ],

    "Salary": [
        90000,85000,100000,95000,80000,
        70000,92000,88000,76000,91000,
        98000,99000,97000,86000,84000,
        83000,81000,75000,82000,94000
    ],

    "Status": [
        "Active","Active","Active","Active","Active",
        "Active","Active","Active","Active","Inactive",
        "Active","Active","Active","Active","Active",
        "Active","Active","Active","Active","Active"
    ],

    "Join_Date": [
        "2008-05-02","1941-03-01","1000-01-01","1962-05-01","1964-04-01",
        "1962-08-01","1963-07-01","1974-10-01","1991-02-01","1949-01-01",
        "1939-05-01","1938-06-01","1941-12-01","1956-10-01","1941-11-01",
        "1940-07-01","1980-10-01","1940-04-01","1984-03-01","1940-02-01"
    ]
})

# print(df)

context = gx.get_context()

try:
    context.suites.add(
        gx.ExpectationSuite(name="SuperHero_Suite")
    )
except Exception:
    pass

datasource = context.data_sources.add_pandas(
    name="SuperHeroes"
)

asset = datasource.add_dataframe_asset(name="Heroes")
batch_request=asset.build_batch_request(
    options={"dataframe":df}
)

validator=context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="SuperHero_Suite"
)


validator.expect_column_values_to_not_be_null("Hero_Name")
validator.expect_column_values_to_not_be_null("Email")

validator.expect_column_values_to_be_unique("Hero_ID")

validator.expect_compound_columns_to_be_unique(
    ["Hero_Name", "Universe"]
)

validator.expect_column_values_to_match_regex(
    "Email",
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

validator.expect_column_values_to_match_regex(
    "Phone",
    r"^\d{10}$"
)

validator.expect_column_values_to_be_between(
    "Mission_Success_Rate",
    min_value=0,
    max_value=100
)

validator.expect_column_values_to_be_between(
    "Power_Level",
    min_value=0,
    max_value=100
)

validator.expect_column_values_to_be_in_set(
    "Universe",
    ["Marvel", "DC"]
)

validator.expect_column_values_to_be_in_set(
    "Status",
    ["Active","Inactive"]
)


validator.expect_column_values_to_be_in_set(
    "Gender",
    ["Male","Female"]
)

validator.expect_column_values_to_be_between(
    "Salary",
    min_value=0


)
results = validator.validate()
print(results)

 

