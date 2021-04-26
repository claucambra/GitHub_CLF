import os
import sys
import getopt
import configparser

from src.data_fetch import * 

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
				sys.exit("Stopping.")
	else:
		print("No configuration file found.")
		confirm = input("This application requires a GitHub developer token to work. Set? [Y/n] ")
		if confirm == 'y' or confirm == "Y" or not confirm:
			return run_setup()
		else:
			sys.exit("Stopping.")

gh_token = config_check_get_token()
print(get_top_users(gh_token))

#print(get_user_data("torvalds", ghToken)["contributionsCollection"]["contributionCalendar"]["totalContributions"])
