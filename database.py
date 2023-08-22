import pyodbc
import os
from dotenv import load_dotenv
import pandas as pd
from listing import *

load_dotenv()

def connect_to_db():
	server = 'garagesalestracker.database.windows.net'
	database = 'TutorialDB'
	username = os.getenv('DB_USERNAME')
	password = os.getenv('DB_PASSWORD')
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
	return cnxn

def write_data(table, listing):
	address, zipcode, start_date, end_date, latitude, longitude = ["A", "B", "C", "D", "E", "F"]
	print(f"{address}, {zipcode}, {start_date}, {end_date}, {latitude}, {longitude}")
	cnxn = connect_to_db()
	try:
		with cnxn.cursor() as cursor:
			sql =  f"""INSERT INTO {table} (Address, Zipcode, Start_Date, End_Date, Latitude, Longitude)
					VALUES ({address}, {zipcode}, {start_date}, {end_date}, {latitude}, {longitude})"""
			# sql =  f"""INSERT INTO {table} (Address, Zipcode, Start_Date, End_Date, Latitude, Longitude)
			# 		VALUES ({listing.get_data()})"""
			cursor.execute(sql) 
			cnxn.commit()
	finally:
		cnxn.close()

def read_data(table): 
	cnxn = connect_to_db()
	try:
		with cnxn.cursor() as cursor:
			sql = "SELECT * FROM dbo.Employees"
			cursor.execute(sql)

			rows = cursor.fetchall()
			for row in rows:
				print(row)
	finally:
		cnxn.close()

def create_db(db_name):
	cnxn = connect_to_db()
	try:
		with cnxn.cursor() as cursor:
			sql = f"CREATE DATABASE {db_name}"
			cursor.execute(sql)
	finally:
		cnxn.close()

def create_table(table):
	cnxn = connect_to_db()
	try:
		with cnxn.cursor() as cursor:
			sql = f"""CREATE TABLE {table} (
				Address varchar(255),
				Zipcode varchar(255),
				Start_Date varchar(255),
				End_Date varchar(255),
				Latitude varchar(255),
				Longitude varchar(255)
				)"""
			cursor.execute(sql)
	finally:
		cnxn.close()

def delete_columns(table, column):
	cnxn = connect_to_db()
	try:
		with cnxn.cursor() as cursor:
			sql = f"ALTER TABLE {table} DROP COLUMN {column}"
			cursor.execute(sql)
	finally:
		cnxn.close()


location = '701 S Eola Rd, Aurora, IL 60504'
date_range = ['Fri Jun 9', 'Sun Jun 11']
coords = ['41.74317600', '-88.24923400']
times = '''
- Friday, June9, 2023 | 9:00 am - 4:00 pm
- Saturday, June 10, 2023 | 9:00 am - 5:30 pm
- Sunday, June 11, 2023 | 8:00 am - 2:30 pm
		'''
listing = Listing(location, date_range, times, coords)
write_data("TestSales", listing)

#create_table("Test_Sales")