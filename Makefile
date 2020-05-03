get-data:
	venv/bin/python get_pbs.py

deploy:
	venv/bin/python generate_leaderboard.py
	git add docs/ athlete_data.json
	git commit -m "Deployment $$(date)"
	git push origin master
	@echo https://running.thegamblingclub.co.uk/

update-leaderboard: get-data deploy
