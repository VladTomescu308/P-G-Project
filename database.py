from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
import warnings
from sqlalchemy import exc

# (Opțional) Ascunde warning-ul legat de versiunea de SQL Server
warnings.filterwarnings('ignore', category=exc.SAWarning)

# 1. Construim stringul
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=SILVIA-LAPTOP;"
    "Database=Proiect Practica;"
    "Trusted_Connection=yes;"
)

# 2. Codificam URL
params = urllib.parse.quote_plus(connection_string)

# 3. Construim URL final
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Engine si Base
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Test connection
try:
    with engine.connect() as connection:
        print("Database connected successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")


# Define the Models
class Countries(Base):
    __tablename__ = 'Countries'
    
    name = Column(String, primary_key=True)
    iso_code = Column(String, nullable=False)
    short_code = Column(String, nullable=False)

    consumer_units = relationship("ConsumerUnits", back_populates="country")

class ConsumerUnits(Base):
    __tablename__ = 'ConsumerUnits'
    
    number_of_consumers = Column(Integer, primary_key = True)
    country_name = Column(String, ForeignKey('Countries.name'), primary_key=True) 

    country = relationship("Countries", back_populates="consumer_units")

Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Adding sample data
def add_sample_countries():
    countries = [
        # Fix: valorile pentru iso și short_code puse între ghilimele (String)
        Countries(name='Test4', iso_code='123', short_code='3'),
        Countries(name='Test5', iso_code='1234', short_code='4'),
        Countries(name='Test6', iso_code='12345', short_code='5')
    ]
    session.add_all(countries)
    session.commit()
    print("Sample countries added.")

def add_sample_consumerUnits():
    consumerUnits = [
        # Fix: le-am atribuit o țară existentă prin Foreign Key
        ConsumerUnits(number_of_consumers=20, country_name='Test1'),
        ConsumerUnits(number_of_consumers=15, country_name='Test2'),
        ConsumerUnits(number_of_consumers=10, country_name='Test3')
    ]
    session.add_all(consumerUnits)
    session.commit()
    print("Sample consumerUnits added.")

# Apelează funcțiile corect (odată fiecare)
add_sample_countries()
add_sample_consumerUnits()

# Close the session
session.close()