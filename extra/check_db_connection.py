import psycopg2
from psycopg2 import OperationalError

# Define your RDS database connection parameters
db_params = {
    "user": "dbuser",
    "password": "dbpassword",
    "host": "exampledb.cculi2axzscc.us-east-1.rds.amazonaws.com",
    "port": "5432",
    "database": "exampledb",
}

try:
    # Attempt to connect to the RDS database
    conn = psycopg2.connect(**db_params)

    # If the connection is successful, print a message
    print("Connected to the RDS database!")

    # Close the connection
    conn.close()

except OperationalError as e:
    print(f"Error: {e}")
