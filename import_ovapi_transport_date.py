import requests
import time
import sqlite3
from datetime import datetime

# Function to query the API


def query_api(base_url, endpoint, max_tries=1):
    url = f"{base_url}{endpoint}"
    retry_count = 0
    while retry_count < max_tries:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
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

# Function to create SQLite table


# def create_table(cursor):
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS ovapi_data (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             line_name TEXT,
#             line_number TEXT,
#             departure_times TEXT,
#             last_updated TEXT
#         );
#     ''')
#     print("Table 'ovapi_data' created successfully.")

# # Function to insert data into the SQLite table


# def insert_data(cursor, data):
#     for line in data:
#         print(line)
#         print(type(line))
#         line_name = line.get("LineName", "")
#         line_number = line.get("LineNumber", "")
#         departure_times = str(line.get("DepartureTimes", ""))
#         last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         cursor.execute('''
#             INSERT INTO ovapi_data (line_name, line_number, departure_times, last_updated)
#             VALUES (?, ?, ?, ?);
#         ''', (line_name, line_number, departure_times, last_updated))

#     print(f"{len(data)} records inserted into the table.")

# # Main function to execute the script


def main():
    base_url = "http://v0.ovapi.nl/"
    endpoint = "/line/"

    # Query the API
    api_data = query_api(base_url, endpoint)
    print(api_data)
    print(type(api_data))

    # if api_data:
    #     # Connect to SQLite database
    #     conn = sqlite3.connect('ovapi_database.db')
    #     cursor = conn.cursor()

    #     # Create table if it doesn't exist
    #     create_table(cursor)

    #     # Insert data into the table
    #     insert_data(cursor, api_data)

    #     # Commit changes and close connection
    #     conn.commit()
    #     conn.close()


if __name__ == "__main__":
    main()
