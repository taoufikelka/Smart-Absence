import sqlite3
from sqlite3 import Error

def create_connection(db_file):
	
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

def List_tables(conn):
	cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = [
		v[0] for v in cursor.fetchall()
		if v[0] != "sqlite_sequence"
	]
	cursor.close()
	return tables

def main():

	database = r"Database/database.db"
	conn = create_connection(database)
	cursor = conn.cursor()

#creating database from sql file
	sqlfile = open("Database/database.sql", "r")
	sqlscript = sqlfile.read()
	try:
		cursor.executescript(sqlscript)
	except Error as e:
		print("[!] Error : ",e)

	for i in range(10):
		sqlinsert = "INSERT INTO Levels (ID_Level, Label) VALUES (" + str(i+1000) + ", 'lvl_" +  str(i) + "')"
		try:
			cursor.execute(sqlinsert)
		except Error as e:
			print(e)


	for tb in List_tables(conn):
		print("Table : ",tb)

	conn.close()

if __name__ == '__main__':
	main()