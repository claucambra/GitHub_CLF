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
import getopt
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
#print(get_top_users(gh_token))
#print(data_prepper({"elChupaCambra": get_user_data("elChupaCambra", gh_token)}))

print(get_user_data("elChupaCambra", gh_token))
