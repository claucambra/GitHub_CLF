import psycopg2

connection = psycopg2.connect("host=localhost dbname=postgres user=postgres")
cur = connection.cursor()

def check_and_create_table():
	cur.execute("""
		CREATE TABLE IF NOT EXISTS github_contributions(
		id integer PRIMARY KEY,
		username text,
		name text,
		bio text,
		location text,
		total_contributions integer,
		average_weekly_contributions float,
		average_daily_contributions float
		)
	""")
	connection.commit()
