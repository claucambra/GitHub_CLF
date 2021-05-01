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
import argparse

from src.data_fetch import *
from src.data_prep import *
from src.location_tools import *

parser = argparse.ArgumentParser(description="Easily and quickly fetch GitHub user contribution data.")

parser.add_argument("--fetch_user", help="Get data on a specific user on GitHub.")
parser.add_argument("--fetch_top_users", help="Get data on the top 100 most followed users on GitHub.", action="store_true")
parser.add_argument("--get_location", help="Get detailed location data for this fetch (if available).")
# parser.add_argument("--add_location_tofile", help="Add detailed location data to an existing output (if available).")
parser.add_argument("--store_gh_token", help="Store a GitHub dev token in the config (needed for access to APIs).")
parser.add_argument("--temp_gh_token", help="Use a GitHub dev token for this fetch and don't store (needed for access to APIs).")

args = parser.parse_args()

if args.fetch_user and args.fetch_top_users:
	sys.exit("Please fetch either ONE user or ALL users.")
if args.store_gh_token and args.temp_gh_token:
	print("NOTE: You have asked to both store the token and to use it temporarily. Your GitHub token WILL NOT be stored.")

gh_token = ""
config = configparser.ConfigParser()
config_path = "config/config.ini"

if args.temp_gh_token:
	gh_token = args.temp_gh_token
elif args.store_gh_token:
	config["Config"] = {"Token": input_token}

	if not os.path.isdir("config"):
		os.mkdir("config")
	with open (config_path, 'w') as config_file:
		config.write(config_file)

	gh_token = args.store_gh_token

data = {}

if not gh_token:
	if os.path.isfile(config_path) and config.read(config_path) and config["Config"]["Token"]:
		gh_token = config["Config"]["Token"]
	else:
		sys.exit("No GitHub dev token has been provided, nor stored in the config file.")
if args.fetch_user:
	data[args.fetch_user] = get_user_data(args.fetch_user, gh_token)
elif args.fetch_top_users:
	data = get_top_users_data(gh_token)
else:
	sys.exit("No fetch instruction provided.")

prepped_data = data_prepper(data)
file_name = csv_creator(prepped_data)
folder = "output/"

if args.get_location:
	add_detailed_location_to_output(args.get_location, folder + file_name)

print("Done!")
