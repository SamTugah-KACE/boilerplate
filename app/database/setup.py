import os
import asyncpg
#from dotenv import load_dotenv





async def execute_sql():
     ###using .env
    #load_dotenv(dotenv_path='config/app.env')
    
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    HOST = os.getenv('DATABASE_HOST')
    DATABASE_USER = os.getenv('DATABASE_USER')

    print("DATABASE_NAME -> ",DATABASE_NAME)
    print("DATABASE_PASSWORD -> ",DATABASE_PASSWORD)
    print("HOST -> ",HOST)
    print("DATABASE_USER -> ",DATABASE_USER)
    try:

        conn2 = await asyncpg.connect(user=f"{DATABASE_USER}", password=f"{DATABASE_PASSWORD}", database=f"{DATABASE_NAME}", host=f"{HOST}")
        db_sql_path = os.path.join(os.path.dirname(__file__), "db.sql")
        
        if os.path.exists(db_sql_path):
            # Read the SQL file
            with open(db_sql_path, 'r') as file:
                sql_commands = file.read()

            # Create extension if not exists
            await conn2.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

                # Execute the SQL commands
            await conn2.execute(sql_commands)
            print(f"SQL script '{db_sql_path}' executed successfully.")
        await conn2.close()

        return True
    
    except Exception as error:
        print("Error executing SQL file:", error)
        return False



async def check_and_create_database():
    """
    Check if a PostgreSQL database exists, if not, create the database and execute a SQL script.

    Args:
        db_name (str): The name of the PostgreSQL database.
        db_sql_path (str): The path to the SQL script to execute.

    Returns:
        bool: True if the database exists or is created successfully, False otherwise.
    """
   
    try:
        
        
        conn = await asyncpg.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )
        
        # Connect to PostgreSQL server
        
        # Connect to PostgreSQL server
        db_name = os.getenv("DATABASE_NAME")
        
        
        # Check if the database exists
        db_exists = await conn.fetchval(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")

        if not db_exists:
            # Create the database if it doesn't exist
            await conn.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully.")
            await conn.close()
            await execute_sql()
           

        return True
    
    except Exception as error:
        print("Error while connecting to PostgreSQL:", error)
        return False


