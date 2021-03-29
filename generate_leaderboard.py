import json
import re
from operator import itemgetter
from jinja2 import Template
import datetime
import time


def convert_date(date_string):
    return re.findall(', (.+)', date_string)[0]


def convert_time_to_seconds(time_string):
    x = time.strptime(time_string, '%H:%M:%S' if len(time_string) > 5 else '%M:%S')
    return datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()

with open('template/index.html') as file_:
    template = Template(file_.read())

with open('athlete_data.json') as athlete_data_json:
    athletes_data = json.load(athlete_data_json)

distances = ['5k', '10k', 'Half-Marathon']

sorted_athlete_data = {}
for athlete_id in athletes_data:
    athlete_data = athletes_data[athlete_id]

    for distance in distances:
        pb = None
        for activity_id in athlete_data[distance]:
            pb = athlete_data[distance][activity_id]

        if pb is None:
            continue

        if distance not in sorted_athlete_data:
            sorted_athlete_data[distance] = []

        sorted_athlete_data[distance].append({
            'name': athlete_data['name'],
            'time': pb['time'],
            'timeSeconds': convert_time_to_seconds(pb['time']),
            'date': convert_date(pb['date']),
            'url': pb['url']
        })

for distance in sorted_athlete_data:
    sorted_athlete_data[distance] = sorted(sorted_athlete_data[distance], key=itemgetter('timeSeconds'))

rendered_template = template.render(sorted_athlete_data=sorted_athlete_data)

with open('docs/index.html', 'w') as file_:
    file_.write(rendered_template)
