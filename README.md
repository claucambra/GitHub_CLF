# GitHub_Contribution_Fetcher

A small python application that fetches a number of stats (within the past year) about a GitHub user and cleanly outputs them to a CSV file.

## Python Module Dependencies

- Argparser
- ConfigParser
- JSON
- CSV
- OS
- Requests
- Sys

## Usage

GHCF offers both a command-line-interface version (`ghcf-cli.py`) and a straight command version (`ghcf.py`).

Both methods require the creation and providing of a [GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token), required for access to GitHub's APIs. The same applies for the detailed location service required by [GeoNames](http://www.geonames.org/export/web-services.html), which requires the creation of a user account and the provision of a verified username.

### CLI version

Simply run `ghcf-cli.py` with Python 3 and follow the on-screen instructions:

`python ghcf-cli.py`

### Pure command version

The pure command version accepts a number of arguments. `ghcf.py` comes with a help command (`-h`) that details these and how you need to use them:

```
usage: ghcf.py [-h] [--fetch_user FETCH_USER] [--fetch_top_users] [--get_location GET_LOCATION]
               [--store_gh_token STORE_GH_TOKEN] [--temp_gh_token TEMP_GH_TOKEN]

Easily and quickly fetch GitHub user contribution data.

optional arguments:
  -h, --help            show this help message and exit
  --fetch_user FETCH_USER
                        Get data on a specific user on GitHub. (Provide a username!)
  --fetch_top_users
                        Get data on the top 1000 most followed users on GitHub. (No need for additional
                        arguments.)
  --get_location GET_LOCATION
                        Get detailed location data for this fetch (if available). Provide a username for
                        GeoNames.org (https://www.geonames.org/login)
  --store_gh_token STORE_GH_TOKEN
                        Store a GitHub dev token in the config (needed for access to APIs).
                        (https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-
                        access-token)
  --temp_gh_token TEMP_GH_TOKEN
                        Use a GitHub dev token for this fetch and don't store (needed for access to
                        APIs). (https://docs.github.com/en/github/authenticating-to-github/creating-a-
                        personal-access-token)
```

## How it works

GitHub offers a  GraphQL API which you can use to extract (public) statistics about a given GitHub user. This API requires an authentication token, which you can acquire from the Developer Settings area of your GitHub account settings.

GitHub also offers a REST API that you can use to find users. You can filter by certain metrics to get a list of users and some of their characteristics.

GHCF sorts users by numbers of followers and filters out users with less than 2000 users (by default). This provides slightly over 1000 users that we can then query the GraphQL API about to get some of these user's public details and simple contribution metrics.

GHCF also supports the use of GeoNames.org's API to find more detailed location data from a user's provided location.

## Limits

A 1000 user limit per request is imposed by the GitHub REST API, hence the 2000 default follower minimum used by GHCF.

It must also be kept in mind that both APIs have a rate limit of 5000 an hour. Keep this in mind as each time the top 1000 users' data is retrieved, this is counts towards the rate limit.

The GeoNames API also has a limit of 20,000 requests a day.

## Importing into PostgreSQL

Before copying our CSV data into our PostgreSQL database we need to create a table that will fit our data. We can do this with the following command:

```
CREATE TABLE IF NOT EXISTS gh_users_contributions (
    username VARCHAR(39) NOT NULL,
    name VARCHAR(100),
    bio TEXT,
    provided_location TEXT,
    location_name VARCHAR(50),
    location_name_type TEXT,
    admin_division_1_name VARCHAR(50),
    country_name VARCHAR(50),
    lat FLOAT,
    lng FLOAT,
    total_contributions INT,
    average_daily_contributions FLOAT,
    average_weekly_contributions FLOAT,
    daily_record INT,

    PRIMARY KEY(username)
);
```

After that, we can simply `cat` our CSV file outputted by GHCF and feed this through to `psql` in the terminal:

```
psql -d zcraamb -c "TRUNCATE TABLE gh_users_contributions"

cat output1_detailed_location.csv | psql -d zcraamb -c "COPY gh_users_contributions(username, name, bio, provided_location, location_name, location_name_type, admin_division_1_name, country_name, lat, lng, total_contributions, average_daily_contributions, average_weekly_contributions, daily_record) FROM STDIN DELIMITER ',' CSV HEADER;"
```
