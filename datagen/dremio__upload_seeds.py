#!/usr/bin/env python3

import os
from http.cookies import SimpleCookie

from dremio.flight.connection import DremioFlightEndpointConnection
from dremio.flight.query import DremioFlightEndpointQuery
from dremio.middleware.cookie import CookieMiddlewareFactory
from pyarrow import flight
import csv


class DFDremioFlightEndpointConnection(DremioFlightEndpointConnection):
    project_id: str

    def __init__(self, params):
        super().__init__(params)
        self.project_id = params.get('project_id')

    def connect(self) -> flight.FlightClient:
        """Connects to Dremio Flight server endpoint with the
        provided credentials."""
        try:
            # Default to use an unencrypted TCP connection.
            scheme = "grpc+tcp"
            client_cookie_middleware = CookieMiddlewareFactory()
            tls_args = {}

            if self.tls:
                tls_args = self._set_tls_connection_args()
                scheme = "grpc+tls"

            if self.project_id:
                cookie = SimpleCookie()
                '''
                Load "project_id=<project-uuid>" into the Cookie container.
                Note we're no longer using it as a black box, and the client
                is making up its own cookie which is less than conformant
                to RFC 6265.  This should ideally not be used in production
                systems.
                '''
                cookie['project_id'] = self.project_id
                '''
                Update the middleware's cookie jar dict, normally intended to be
                internal-only.
                '''
                client_cookie_middleware.cookies.update(cookie.items())

            if self.username and (self.password or self.token):
                print('software')
                return self._connect_to_software(tls_args, client_cookie_middleware, scheme)

            elif self.token:
                print('cloud')
                return self._connect_to_cloud(tls_args, client_cookie_middleware, scheme)

            raise ConnectionError("Username+token or token must be supplied.")

        except Exception:
            print("There was an error trying to connect to the Dremio Flight Endpoint")
            raise


class DFDremioFlightEndpoint:
    def __init__(self, connection_args: dict) -> None:
        self.connection_args = connection_args
        self.dremio_flight_conn = DFDremioFlightEndpointConnection(
            self.connection_args)

    def connect(self) -> flight.FlightClient:
        return self.dremio_flight_conn.connect()

    def get_reader(self, client: flight.FlightClient) -> flight.FlightStreamReader:
        dremio_flight_query = DremioFlightEndpointQuery(
            self.connection_args.get("query"), client, self.dremio_flight_conn
        )
        return dremio_flight_query.get_reader()


def run_query(query: str):
    config = {
        'hostname': 'data.dremio.cloud',
        'port': 443,
        'token': os.environ.get('DREMIO_TOKEN'),
        'username': None,
        'password': None,
        'tls': True,
        # 'disable_certificate_verification': True,
        'path_to_certs': os.path.join(os.path.dirname(__file__),
                                      "./dremio_bundle.pem"),
        'query': query,
        'project_id': 'e94ab14a-43d8-44dd-8f59-cffbb1f0f12f',
    }
    endpoint = DFDremioFlightEndpoint(config)
    client = endpoint.connect()
    cursor = endpoint.get_reader(client)
    data = cursor.read_all()

    print(data.to_pandas())
    return data


def column_type(col):
    if col in ['org_id', 'user_id', 'price']:
        return 'int'
    elif col in ['created_at', 'event_timestamp']:
        return 'timestamp'
    elif col in ['is_first_user']:
        return 'boolean'
    else:
        return 'varchar'


def column_quote(col):
    if col in ['org_id', 'user_id', 'price']:
        return False
    elif col in ['created_at', 'event_timestamp']:
        return True
    elif col in ['is_first_user']:
        return False
    else:
        return True


def create_query(file):
    table = file.split('.')[0]
    full_table_name = schema + table

    with open(file_path + file, 'r') as file:
        first_line = file.readline().strip()
    columns = first_line.split(',')

    columns_types_string = ', '.join([f'{col} {column_type(col)}' for col in columns])
    create_query = f"""create table {full_table_name} ({columns_types_string});"""
    return create_query


def drop_query(file):
    table = file.split('.')[0]
    full_table_name = schema + table
    drop_query = f"""DROP TABLE IF EXISTS {full_table_name};"""
    return drop_query


def create_insert_statements(file, batch_size):

    csv_file_path = file_path + file
    table = file.split('.')[0]
    full_table_name = schema + table

    with open(file_path + file, 'r') as file:
        columns_string = file.readline().strip()
        columns_list = columns_string.split(',')

    # List to hold the generated SQL statements
    sql_statements = []

    # Read the CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Process the rows in batches
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        values1 = []
        
        for row in batch:
            elements = []
            for col in columns_list:
                # elements.append(f"'{row[col]}'" if column_quote(col) else f"{row[col]}")
                element_to_append = f"{row[col]}"
                element_to_append = element_to_append.replace('T', ' ').replace('Z', '') if column_type(col) == 'timestamp' else element_to_append
                element_to_append = element_to_append.replace("'", "''").replace('’', "''") if column_type(col) == 'varchar' else element_to_append
                element_to_append = f"'{element_to_append}'" if column_quote(col) else f"{element_to_append}"
                elements.append(element_to_append)
            values1.append(f"({', '.join(elements)})")

        # Create the SQL statement for the current batch
        sql_statement = f"insert into {full_table_name} ({columns_string}) values {', '.join(values1)};"
        sql_statements.append(sql_statement)
    
    return sql_statements


file_path = '../seeds/'
target_schema = os.environ.get('DREMIO_FOLDER')
schema = '"Alexey S3".alexeydremiobucket.' + target_schema + '.'


seed_files = []
for path in os.listdir(file_path):
    if os.path.isfile(os.path.join(file_path, path)):
        if path.endswith(".csv"):
            seed_files.append(path)
print(seed_files)


for filename in seed_files:
    print(f'\n{filename} ==========================================')
    print(drop_query(filename))
    run_query(drop_query(filename))

    print(create_query(filename))
    run_query(create_query(filename))

    insert_statements = create_insert_statements(filename, 500)
    for statement in insert_statements:
        print(statement)
        run_query(statement)
