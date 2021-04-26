# Copyright 2021 Claudio Cambra
#
# This file is part of GitHub Contribution Fetcher.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import psycopg2

#connection = psycopg2.connect("host=localhost dbname=postgres user=postgres")
#cur = connection.cursor()

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
