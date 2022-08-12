# Strava 5K Leaderboard

https://running.thegamblingclub.co.uk/
- Selenium web scraper to fetch the PBs from Strava
- Generates HTML using Jinja template
- Deployed via GitHub pages


```
# Install
make install

# Fetch the data
make get-data

# Generate the leaderboard and push the HTML
make deploy
```