import requests
import time
import json

from ovapi_line import OvapiLine
from sql_helpers import connect_to_database, create_table, upsert_ovapi_lines, create_partitions


def query_api(base_url: str, endpoint: str, max_tries: int = 1):
    """Queries an API for an url and a specific endpoint
    Returns the content of the response for a 200 success code
    Otherwise retries until tries get to max_tries then fails.
    The retry mechanism is exponential, a high max_tries parameter
    can lead to long calls.

    Args:
        base_url (str): Base url of the endpoint
        endpoint (str): Specific endpoint to query
        max_tries (int, optional): Number of tries until the function fails

    Returns:
        dict: Content of the api response for a success, None otherwise
    """
    url = f"{base_url}{endpoint}"
    print(f"Querying data from {url}...")
    retry_count = 0
    while retry_count < max_tries:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"{len(data)} objects were successfully received from {url}")
            return data
        else:
            print(
                f"Error: Unable to fetch data from {url}. Status code: {response.status_code}")
            retry_count += 1
            # Retry with exponential backoff
            wait_time = 2 ** retry_count
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    print(f"Stopped retrying on {url} after {max_tries} tries")

    return None


def check_and_parse_ovapi_lines(data: dict):
    """Check if data isn't empty or bad type then
    tries to parse the data to OvapiLine type

    Args:
        data (dict): Dict of ovapi lines under the API
        format: https://github.com/koch-t/KV78Turbo-OVAPI/wiki/Line

    Raises:
        ValueError: Data is empty or bad type

    Returns:
        List[OvapiLine]: Incoming data parsed as
    """
    if data is None or not isinstance(data, dict):
        raise ValueError(
            "The data passed doesn't conform to OVAPI"
            "standard (not a proper dictionary)")
    ovapi_line_list = [OvapiLine(line_id, data[line_id]) for line_id in data]
    print("All objects match the expected OvapiLine format")
    return ovapi_line_list



def extract_and_load_ovapi_data(base_url: str, endpoint:str):
    """ Main function to extract and load the data from 
    an OVAPI endpoint 

    Args:
        base_url (str): Base url of the endpoint to call
        endpoint (str): Specific endpoint to call
    """

    # Query the API
    api_data = query_api(base_url, endpoint)
    # Check data integrity & parse
    ovapi_line_list = check_and_parse_ovapi_lines(api_data)

    # Load database settings
    with open("settings.json", "r") as config_file:
        db_params = json.load(config_file)

    # Create database (PostgreSQL)
    conn = connect_to_database(**db_params)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    create_table(cursor)

    # Create partitions of the table
    create_partitions(cursor, ovapi_line_list)

    # Insert data into the table
    upsert_ovapi_lines(cursor, ovapi_line_list)

    # Commit changes and close connection
    print("Commiting and closing connection to the database")
    conn.commit()
    conn.close()
    

if __name__ == "__main__":
    base_url = "http://v0.ovapi.nl"
    endpoint = "/line/"
    extract_and_load_ovapi_data(base_url, endpoint)
