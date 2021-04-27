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

def get_location_details(geonames_username, location_string):
	url = f"http://api.geonames.org/searchJSON?q={location_string}&maxRows=1&username={geonames_username}"
	r = requests.get(url)
	
	r = r.json()
	
	if "status" in r:
		message = r["status"]["message"]
		print(f"Error fetching location: {message} (api.geonames.org)")
		return
	else:
		return r["geonames"][0]

#print(get_location_details("Malaga, Spain"))
