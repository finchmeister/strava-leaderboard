import json
import re
from operator import itemgetter
from jinja2 import Template


def convert_date(date_string):
    return re.findall(', (.+)', date_string)[0]


with open('template/index.html') as file_:
    template = Template(file_.read())

with open('athlete_data.json') as athlete_data_json:
    athletes_data = json.load(athlete_data_json)

sorted_athlete_data = []
for athlete_id in athletes_data:
    athlete_data = athletes_data[athlete_id]

    best_5K = None
    for activity_id in athlete_data['5Ks']:
        best_5K = athlete_data['5Ks'][activity_id]

    if best_5K is None:
        continue

    sorted_athlete_data.append({
        'name': athlete_data['name'],
        'time': best_5K['time'],
        'date': convert_date(best_5K['date']),
        'url': best_5K['url']
    })

sorted_athlete_data = sorted(sorted_athlete_data, key=itemgetter('time'))

rendered_template = template.render(athlete_data=sorted_athlete_data)

with open('docs/index.html', 'w') as file_:
    file_.write(rendered_template)
