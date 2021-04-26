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

import csv
import os

def data_prepper(users_dict):
	user_data = []
	
	num_users = users_dict.keys().len()
	current_user_num = 0
	
	for user in users_dict:
		current_user_num += 1
		sys.stdout.write(f"\rPreparing data of user... {str(current_user_num)}/{str(num_users)}")
		sys.stdout.flush()
		
		contribCalendar = users_dict[user]["contributionsCollection"]["contributionCalendar"]
		
		num_weeks = 0
		num_days = 0
		daily_record = 0
		
		for week in contribCalendar["weeks"]:
			num_weeks += 1
			for day in week["contributionDays"]:
				num_days += 1
				if day["contributionCount"] > daily_record:
					daily_record = day["contributionCount"]
		
		avg_weekly_contrib = contribCalendar["totalContributions"] / num_weeks
		avg_daily_contrib = contribCalendar["totalContributions"] / num_days
		
		user_dict = {
			"username": user,
			"name": users_dict[user]["name"],
			"bio": users_dict[user]["bio"],
			"location": users_dict[user]["location"],
			"total_contributions": contribCalendar["totalContributions"],
			"average_weekly_contributions": avg_weekly_contrib,
			"average_daily_contributions": avg_daily_contrib,
			"daily_record": daily_record,
		}
		
		user_data.append(user_dict)
	
	print("\rUser data prepped.")
	
	return user_data

def csv_creator(prepped_data):
	if not os.path.isdir("output"):
		os.mkdir("output")
	
	file_num = 1
	
	while os.path.isfile(f"output/output{file_num}.csv"):
		file_num += 1
	
	with open("output/output{file_num}.csv", "w") as csvfile:
		table_headers = prepped_data[0].keys()
		
		datawriter = csv.writer(csvfile, delimiter=",", fieldnames=table_headers)
		datawriter.writeheader()
		
		for user in prepped_data:
			writer.writerow(user)
