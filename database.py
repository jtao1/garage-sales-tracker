import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

server = 'garagesalestracker.database.windows.net'
database = 'TutorialDB'
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
