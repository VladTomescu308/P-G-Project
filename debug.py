import pyodbc

# Connect to SQL Server using Windows Authentication (SSMS)
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ALEX_TUTU;'           # ex: localhost\SQLEXPRESS
    'DATABASE=Proiect Practica;'                
    'Trusted_Connection=yes;'        # Windows Authentication
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM COUNTRIES")

countries = cursor.fetchall()

print(countries)

conn.close()