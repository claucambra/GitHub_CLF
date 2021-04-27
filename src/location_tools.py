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

import os
import sys
import requests
import json 
import csv
import re

def get_location_details(geonames_username, location_string):
	url = f"http://api.geonames.org/searchJSON?q={location_string}&maxRows=1&username={geonames_username}"
	r = requests.get(url)
	
	r = r.json()
		
	if "status" in r:
		message = r["status"]["message"]
		print(f"Error fetching location: {message} (api.geonames.org)")
		return ""
	elif r["totalResultsCount"] == 0:
		print(f"No results found for {location_string}")
		return ""
	else:
		return r["geonames"][0]

def add_detailed_location_to_output(geonames_username, csv_filename):
	with open (csv_filename, "r") as csvfile:
		reader = csv.DictReader(csvfile, delimiter=",")
		
		split_filepath = os.path.splitext(csv_filename)
		filepath_new = split_filepath[0] + "_detailed_location" + split_filepath[1]
		
		with open(filepath_new, "w") as new_csvfile:
			
			fieldnames = ["username", "name", "bio", "provided_location", "location_name", "location_name_type", "admin_division_1_name", "country_name", "lat", "lng", "total_contributions", "average_daily_contributions", "average_weekly_contributions", "daily_record"]
			
			datawriter = csv.DictWriter(new_csvfile, delimiter=",", fieldnames=fieldnames)
			datawriter.writeheader()
			
			current_user_num = 0
				
			for row in reader:
				
				current_user_name = row["username"]
				current_user_num += 1
				sys.stdout.write(f"\rWriting user {current_user_name} data to file...\t\t{str(current_user_num)} ")
				sys.stdout.flush()
				
				latitude = ""
				longitude = ""
				location_name = ""
				location_name_type = ""
				admin_division_1_name = ""
				country_name = ""
				
				if row["location"]:
					location_query = row["location"]
					location_query = re.sub(r"Earth", "", location_query, flags = re.I)
					location_query = re.sub(r"(USA|U\.S\.A\.|US|U\.S\.|United States)", "United States of America", location_query)
					location_query = re.sub(r"SF", "San Francisco", location_query)
					location_query = re.sub(r"(UK|U\.K\.)", "United Kingdom", location_query, flags = re.I)
					location_query = re.sub(r"(PRC|P\.R\.C\.)", "China", location_query)
					location_query = re.sub(r"\s+,\s+$", "", location_query)
					location_query = re.sub(r"@", " , ", location_query)
					location_query = re.sub(r"/.+", "", location_query)
					print(location_query)

					location_data = get_location_details(geonames_username, location_query)
					if location_data:
						latitude = location_data["lat"]
						longitude = location_data["lng"]
						location_name = location_data["name"]
						location_name_type = location_data["fcodeName"]
						if "continent" not in location_name_type and "region" not in location_name_type:
							admin_division_1_name = location_data["adminName1"]
							country_name = location_data["countryName"]
						if "region" in location_name_type and "California" in location_name:
							country_name = "United States of America"
				
				user_dict = {
					"username": row["username"],
					"name": row["name"],
					"bio": row["bio"],
					"provided_location": row["location"],
					"location_name": location_name,
					"location_name_type": location_name_type,
					"admin_division_1_name": admin_division_1_name,
					"country_name": country_name,
					"lat": latitude,
					"lng": longitude,
					"total_contributions": row["total_contributions"],
					"average_weekly_contributions": row["average_weekly_contributions"],
					"average_daily_contributions": row["average_daily_contributions"],
					"daily_record": row["daily_record"],
				}
				
				datawriter.writerow(user_dict)

#print(get_location_details("", "Malaga, Spain"))
#print(add_detailed_location_to_output("", "../output/output4.csv"))

