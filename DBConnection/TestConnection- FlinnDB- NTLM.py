import jaydebeapi

# Parameterize the connection details at the top of the script
server = 'FSI-FSQL3-PROD'
database = 'FlinnWebPriceDW'
username = 'svc_webscrape'
password = 'A9wCQKVPNLzm!d$AC$fY'
domain = 'fsi'

# Path to the JDBC driver JAR file
jdbc_driver_path = '/Users/g6-media/Downloads/sqljdbc_12-2.6/enu/jars/mssql-jdbc-12.6.2.jre8.jar'
jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'

# JDBC connection URL
connection_url = f'jdbc:sqlserver://{server};databaseName={database};encrypt=true;trustServerCertificate=true;integratedSecurity=true;'

# Additional connection properties
connection_properties = {
    'user': f'{username}',
    'password': password,
    'integratedSecurity': 'true',
    'authenticationScheme': 'NTLM',
    'domain': domain
}

# Create a connection
try:
    connection = jaydebeapi.connect(
        jdbc_driver_class,
        connection_url,
        connection_properties,
        [jdbc_driver_path]
    )

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

except jaydebeapi.DatabaseError as e:
    print("Error connecting to the database: ", e)
