import requests
import json

def get_top_users(auth_token = None):
	headers = {"Authorization": f"bearer {auth_token}"}
	
	min_followers = 2000
	
	results = []
	
	print(auth_token) if auth_token != None else None
	
	for num in range(1, 11):
		url = f"https://api.github.com/search/users?q=followers:>{min_followers}+sort:followers&page={num}&per_page=100"
		r = requests.get(url, headers = headers if auth_token != None else None)
		results.append(r.json())
	
	usernames = []
	
	for page in results:
		for item in page["items"]:
			usernames.append(item["login"])
		
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
	
	r = requests.post("https://api.github.com/graphql", data = json.dumps(query), headers = headers)
	
	return r.json()["data"]["user"]

