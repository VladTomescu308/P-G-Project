import pyodbc

# Connect to SQL Server using Windows Authentication (SSMS)
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=SILVIA-LAPTOP;'           # ex: localhost\SQLEXPRESS
    'DATABASE=P&G Project;'                
    'Trusted_Connection=yes;'        # Windows Authentication
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM COUNTRIES")

countries = cursor.fetchall()

print(countries)

conn.close()