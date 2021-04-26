# GitHub_Contribution_Fetcher

A small python application that fetches a number of stats (within the past year) about a GitHub user and cleanly outputs them to a CSV file.

## How it works

GitHub offers a  GraphQL API which you can use to extract (public) statistics about a given GitHub user. This API requires an authentication token, which you can acquire from the Developer Settings area of your GitHub account settings.

GitHub also offers a REST API that you can use to find users. You can filter by certain metrics to get a list of users and some of their characteristics. 

GCF sorts users by numbers of followers and filters out users with less than 2000 users (by default). This provides slightly over 1000 users that we can then query the GraphQL API about to get some of these user's public details and simple contribution metrics.

## Limits

A 1000 user limit per request is imposed by the GitHub REST API, hence the 2000 default follower minimum used by GCF.

It must also be kept in mind that both APIs have a rate limit of 5000 an hour. Keep this in mind as each time the top 1000 users' data is retrieved, this is counts towards the rate limit.

## Python Module Dependencies

- OS
- Sys
- ConfigParser
- Requests
- JSON
- CSV



## Usage

Simply run `gh_contribution_fetcher.py` with Python 3:

`python gh_contribution_fetcher.py`