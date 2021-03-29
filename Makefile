install:
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt


get-data:
	venv/bin/python3 get_pbs.py


deploy:
	venv/bin/python3 generate_leaderboard.py
	git add docs/ athlete_data.json
	git commit -m "Deployment $$(date)"
	git push origin master
	@echo https://running.thegamblingclub.co.uk/

update-leaderboard: get-data deploy
