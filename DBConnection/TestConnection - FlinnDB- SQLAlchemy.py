from sqlalchemy import create_engine

# Parameterize the connection details at the top of the script
server = 'FSI-FSQL3-PROD'
database = 'FlinnWebPriceDW'
username = 'svc_webscrape'
password = 'A9wCQKVPNLzm!d$AC$fY'
driver = 'ODBC Driver 17 for SQL Server'

# Create the connection string
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={{{driver}}};'

try:
    # Establish a connection
    engine = create_engine(connection_string)

    # Test the connection
    with engine.connect() as connection:
        result = connection.execute("SELECT @@version")
        row = result.fetchone()
        while row:
            print(row[0])
            row = result.fetchone()

    print("Connection successful!")

except Exception as e:
    print("Error connecting to the database: ", e)
