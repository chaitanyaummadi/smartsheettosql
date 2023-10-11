import pyodbc

import smartsheet

 

# Azure SQL Database connection details

server_name = "city-ops.database.windows.net"

database_name = "reporting-bi"

username = "city-ops"

password = "Qcf#a$qRn4HAmx7qHb8sUyJ"

 

# Smartsheet API access token

smartsheet_access_token = "63XfpMrhd3MGfoOZmtrEgZ6i9VIwsmpwtRfeb"

smartsheet_sheet_id = "2965979680165764"  # Specify the Smartsheet sheet ID

 

# Initialize Smartsheet client

ss_client = smartsheet.Smartsheet(smartsheet_access_token)

 

# Fetch the Smartsheet data and sheet name

sheet = ss_client.Sheets.get_sheet(smartsheet_sheet_id)

sheet_name = sheet.name

rows = sheet.rows

 

# Extract column names from the sheet's columns

column_names = [column.title for column in sheet.columns]

 

# Establish a connection to Azure SQL Database

connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server_name};Database={database_name};Uid={username};Pwd={password};"

connection = pyodbc.connect(connection_string)

cursor = connection.cursor()

 

# Check if the table already exists in the database

if sheet_name:

    cursor.execute(f"DROP TABLE IF EXISTS [{sheet_name}]")

    connection.commit()

 

# Create a dynamic SQL query to create the table with Smartsheet name and column names

create_table_query = f"""

CREATE TABLE [{sheet_name}] (

    {', '.join([f'[{column}] NVARCHAR(MAX)' for column in column_names])}

)

"""

 

# Execute the dynamic SQL query to create the table

cursor.execute(create_table_query)

connection.commit()

 

# Iterate through the rows and insert data into the table

for row in rows:

    values = [cell.value for cell in row.cells]

 

    # Generate a dynamic SQL INSERT INTO statement

    insert_query = f"INSERT INTO [{sheet_name}] VALUES ({', '.join(['?'] * len(values))})"

   

    # Execute the INSERT INTO statement with parameterized values

    cursor.execute(insert_query, values)

    connection.commit()

 

# Close the database connection

connection.close()
