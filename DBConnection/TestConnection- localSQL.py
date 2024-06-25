from sqlalchemy import create_engine, MetaData, text

# Parameterize the connection details at the top of the script
db_credentials = {
    'username': 'root',
    'password': 'Welcome123',
    'host': 'localhost',
    'port': 3306
}

# Create the SQLAlchemy engine without specifying a database
engine = create_engine(
    f"mysql+mysqlconnector://{db_credentials['username']}:{db_credentials['password']}@{db_credentials['host']}:{db_credentials['port']}/"
)

# Initialize MetaData object
meta = MetaData()

# Test the connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection to the MySQL server was successful.")
except Exception as e:
    print(f"Error connecting to the MySQL server: {e}")
