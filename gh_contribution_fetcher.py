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
import configparser

from src.data_fetch import * 
from src.data_prep import *

gh_token = ""
config = configparser.ConfigParser()
config_path = "config/config.ini"

def run_setup():
	input_token = input("Please type in your GitHub developer token.\n")
	while not input_token:
		input_token = input("Please type in your GitHub developer token.\n")
	config["Config"] = {"Token": input_token}
	if not os.path.isdir("config"):
		os.mkdir("config")
	with open (config_path, 'w') as config_file:
		config.write(config_file)
	print(f"Token saved in {config_path}")
	return input_token

def temp_key_set():
	input_token = input("Please type in your GitHub developer token.\n")
	if not input_token:
		sys.exit("Stopping.")
	else:
		return input_token

def config_check_get_token():
	if os.path.isfile(config_path) and config.read(config_path) and config["Config"]["Token"]:
		confirm = input("Use stored GitHub developer token? [Y/n] ")
		if confirm == 'y' or confirm == "Y" or not confirm:
			return config["Config"]["Token"]
		else:
			confirm = input("Set a new GitHub developer token? [Y/n] ")
			if confirm == 'y' or confirm == "Y" or not confirm:
				return run_setup()
			else:
				confirm = input("Use a temporary GitHub developer token? (Will not be stored) [Y/n] ")
				if confirm == 'y' or confirm == "Y" or not confirm:
					return temp_key_set()
				else:
					sys.exit("Stopping.")
	else:
		print("No configuration file found.")
		confirm = input("This application requires a GitHub developer token to work. Set? [Y/n] ")
		if confirm == 'y' or confirm == "Y" or not confirm:
			return run_setup()
		else:
			confirm = input("Use a temporary GitHub developer token? (Will not be stored) [Y/n] ")
			if confirm == 'y' or confirm == "Y" or not confirm:
				return temp_key_set()
			else:
				sys.exit("Stopping.")

def ask_about_database():
	confirm = input("Upload to database? [Y/n]")
	if confirm == 'y' or confirm == "Y" or not confirm:
		return true
	else:
		return false

print("\nMake sure you have write access to your current folder!\n")
gh_token = config_check_get_token()

print("""
	0. Cancel and exit
	1. Fetch a specific user's data
	2. Fetch top 1000 GitHub users' data
	
	Please enter the number of your selection.
	""")
selection = input()

if not selection or selection == "0":
	sys.exit()
else:
	selection = int(selection)
	data = {}
	if selection == 1:
		username = input("Enter GitHub username: ")
		data[username] = get_user_data(username, gh_token)
	elif selection == 2:
		data = get_top_users_data(gh_token)
	
	prepped_data = data_prepper(data)
	csv_creator(prepped_data)
