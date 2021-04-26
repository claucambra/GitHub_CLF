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

import sys
import requests
import json

def get_top_users(auth_token = None, in_min_followers = 2000):
	headers = {"Authorization": f"bearer {auth_token}"}
	
	min_followers = in_min_followers
	
	results = []
	
	for num in range(1, 11):
		progress = 100*(num-1)
		sys.stdout.write(f"\rFetching top users... {str(progress)}/{str(1000)}")
		sys.stdout.flush()
		url = f"https://api.github.com/search/users?q=followers:>{min_followers}+sort:followers&page={num}&per_page=100"
		r = requests.get(url, headers = headers if auth_token != None else None)
		results.append(r.json())
	
	if("Bad credentials" in results[0]["message"]):
		print("\rYour token has been rejected. Are you sure you typed it in correctly? Is it still valid?")
		sys.exit(2)
	else:
		print("\rFetching complete. Collating results...")
		
		usernames = []
		
		for page in results:
			if "items" in page:
				for item in page["items"]:
					usernames.append(item["login"])
			else:
				print("\rNo items found on this page...")
			
		return usernames

def get_user_data(username, auth_token):
	headers = {"Authorization": f"bearer {auth_token}"}
	
	query = {
		"query": f"""query {{
			user(login: \"{username}\") {{
				name
				bio
				location
				contributionsCollection {{
					contributionCalendar {{
						colors
						totalContributions
						weeks {{
							contributionDays {{
								contributionCount
								date
								weekday
							}}
							firstDay
						}}
					}}
				}}
			}}
		}}"""
	}
	
	print(f"Getting {username}'s data...")
	r = requests.post("https://api.github.com/graphql", data = json.dumps(query), headers = headers)
	
	return r.json()["data"]["user"]

def get_top_users_data(auth_token, in_min_followers = 2000):
	top_users = get_top_users(auth_token, in_min_followers)
	
	all_users_data = {}
	
	for user in top_users:
		data = get_user_data(user, auth_token)
		all_users_data[user] = data
	
	return all_users_data
