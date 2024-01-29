from ovapi_line import OvapiLine

from typing import List
import psycopg2
from psycopg2 import sql


def connect_to_database(dbname: str, user: str, password: str, host: str, port: str):
    """Connects to the database described in the parameters

    Args:
        dbname (str): 
        user (str): 
        password (str): 
        host (str): 
        port (str): 

    Returns:
        connection: Connection to the database of choice
    """
    print(f"Connecting to database {dbname} at {host}:{port}")
    return psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host, port=port)



def create_table(cursor):
    """If the table (for the ovapi data) doesn't exist,
    creates it

    Args:
        cursor (cusrsor): Cursor pointing to the database of choice
    """
    with open("./sql_queries/create_ovapi_table.sql", "r") as f:
        creation_query = f.read()
    cursor.execute(creation_query)
    print("Table 'OvapiRawLineInformation' was created (if it didn't exist).")



def upsert_ovapi_lines(cursor, ovapi_line_list: List[OvapiLine]):
    """Upserts a list of OvapiLine object to the database pointed
    by the cursor

    Args:
        cursor (cursor): Points to the database of choice
        ovapi_line_list (List[OvapiLine]): Information to upsert
    """
    with open("./sql_queries/upsert_ovapi_row.sql", "r") as f:
        insert_query = f.read()

    cursor.executemany(insert_query, [
                       ovapi_line.format_for_insert()
                       for ovapi_line in ovapi_line_list])

    print(f"Upserting {len(ovapi_line_list)} records into the table.")


def create_partitions(cursor, ovapi_line_list: List[OvapiLine]):
    """Create partitions using the provided SQL script
    The choice was made to partition by DataOwnerCode
    The function iterates over them and creates a partition
    for each different code

    Args:
        cursor (cursor): Cursor pointing to the database of choice
        ovapi_line_list (List[OvapiLine]): List of lines to import used to gather
        DataOwnerCodes
    """
    with open("./sql_queries/create_ovapi_partition.sql", "r") as f:
        partition_query = f.read()

    ovapi_partition_arguments_list = [
        (line.data_owner_code,)
        for line in ovapi_line_list]
    ovapi_partition_arguments_list = list(set(ovapi_partition_arguments_list))

    for partition_argument in ovapi_partition_arguments_list:
        cursor.execute(
            sql.SQL(partition_query).format(table=sql.Identifier(
                f"OvapiRawLineInformation__{partition_argument[0]}")),
            partition_argument)
    print(f"{len(ovapi_partition_arguments_list)} partitions were created.")
