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

def data_prepper(users_dict):
	user_data = []
	
	for user in users_dict:
		contribCalendar = user["contributionsCollection"]["contributionCalendar"]
		
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
			"name": user["name"],
			"bio": user["bio"],
			"location": user["location"],
			"total_contributions": contribCalendar["totalContributions"],
			"average_weekly_contributions": avg_weekly_contrib,
			"average_daily_contributions": avg_daily_contrib,
			"daily_record": daily_record,
		}
		
		user_data.append(user_dict)
	
	return user_data
