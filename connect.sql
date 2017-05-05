import psycopg2

# connect to database
conn = psycopg2.connect(dbname="db_project", host="localhost", port="5432")

# create a cursor
cursor = conn.cursor()


# execute SQL statement
cursor.execute("select * from artikel")

# get the resultset as a tuple
result = cursor.fetchall()

# iterate through resultset
for artikel in result:
	print (artikel)
