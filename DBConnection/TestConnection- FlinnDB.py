import pyodbc

# Parameterize the connection details at the top of the script
server = 'FSI-FSQL3-PROD'
database = 'FlinnWebPriceDW'
username = r'fsi\svc_webscrape'
# username = 'anarayanan'
password = 'A9wCQKVPNLzm!d$AC$fY'
driver = '{ODBC Driver 17 for SQL Server}'

# Create a connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Establish a connection
    connection = pyodbc.connect(connection_string)

    # Create a cursor object using the connection
    cursor = connection.cursor()

    # Execute a simple query to test the connection
    cursor.execute("SELECT @@version;")

    # Fetch the result
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    print("Connection successful!")

except pyodbc.Error as e:
    print("Error connecting to the database: ", e)
