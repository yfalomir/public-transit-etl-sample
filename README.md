
# Blablacar OVAPI data test (Youri Falomir)

This project simulates the extraction and ingestion of data coming from [OvAPI](https://github.com/koch-t/KV78Turbo-OVAPI/wiki)

# 0 - Requirements

For this project, I assume you already have Python installed (>3.7 and 3.8 preferred) and [gcc](https://doc.ubuntu-fr.org/gcc) installed.

This project requires some packages described in requirements.txt. 
Recommended setup steps:
```
python -m venv my-ovapi-env
source my-ovapi-env/bin/activate
pip install -r requirements.txt
```

# 1 - Setup

The script stores the data in a PostgreSQL database. It must be initialized with init_script/init.sql.
You can start one using docker
```
docker run --name postgres-container -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=ovapi_lines -e POSTGRES_USER=postgres -p 5432:5432 -v "$(pwd)/init_script":/docker-entrypoint-initdb.d -d postgres:latest 
```

The credentials and settings to be used by the project must be stored inside `settings.json`

# 2 - How to run the project

This project simply runs by calling `import_ovapi_transport_data.py`
```
python -m import_ovapi_transport_data
```

# 3 - Project structure
```
├── import_ovapi_transport_data.py
├── ovapi_line.py
├── init_script
│   ├── init.sql
├── sql_queries
│   ├── create_ovapi_partition.sql
│   ├── create_ovapi_table.sql
│   └── upsert_ovapi_row.sql
├── dag_definition.py
└── tests
    ├── __init__.py
    └── test_query_api.py
├── sql_helpers.py
├── README.md
├── requirements.txt
├── sample_data
│   └── success_data.json
├── settings.json
```


import_ovapi_transport_data.py: The main file orchestrating the import of data
ovapi_line.py: Class representing objects from the OVAPI line endpoint
sql_helpers.py: Functions to interact with the database (using sql_queries)
dag_definition.py: Sample definition of a DAG that would orchestrate this import
As mentioned in the test, no airflow infrastructure was set up, this is just a dummy example

sql_queries: Contains templated queries to manage the database, table and data
init.sql: Creates a custom type needed for the ingestion

sample_data: Contains data used for testing (in the test directory)
settings.json: Contains parameters to connect to the PostgreSQL, must match the db you want to use

# 4 - Testing 
The project contains minimal unit testing to verify success, failure and retry behavior depending on the response of the API. In production, more tests would be needed
To run the tests run the following command from the root of the project
```
python tests/test_query_api.py 
```

# 5 - Further data usage and maintenance

The data is extracted using the requests module and parsed via the OvapiLine class, changes in data structure should be passed down to the class.


The data is made available in the OvapiRawLineInformation table. This table stores quasi-raw data from the API. Specific columns are detailed in the column comments.

The table is partitioned by id and DataOwnerCode, this improves performance for per Owner (company) analysis. There is one partition by DataOwnerCode

# 6 - Possible improvements

## Extraction
- The current loading method fails if any row doesn't match the predefined format which is helpful for integrity but reduces data freshness in the case of a few wrongly formatted rows.
- If acceptable for the use case, we could drop badly formatted data and import the remaining one only.

- The settings and secrets management could be centralized in airflow or environment variables instead of inside sub-modules

## Loading
- The loading strategy could be switched to a batch import if the data were of a few orders of magnitude bigger and write performance was an issue.
- We could batch upsert by a thousand lines or by ten thousand lines to flatten the load on the database.

## Database & Modelization
- The current data storage makes use of the TEXT type mainly (unfortunately even some attributes suffixed with "number" are strings in the API). Some data could be cleaned later in the transformation process to open for more suitable data types.

- If filtering on transport type is a common use case, adding the column to the index would be beneficial for read operations (while causing a slight reduction in write performance). Also, the column could be a foreign key (integer) to a descriptive table.

- Database connection and permission should obviously be managed securely.

## DAG

- The DAG is minimal. It only calls one Python function which renders the process weak. To improve this we would (with more time) setup some cloud/shared storage (like s3), and then we could create specific tasks:
    - Extract task that stores the data in this storage.
    - Data quality check task
    - Loading task (to the database).
    
- Options I discarded:
  - Using Xcoms -> they are made for metadata and small amounts of information, won't scale
  - Storing the extract in the file system -> Doesn't scale to more than 1 worker
