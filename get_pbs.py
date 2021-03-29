from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json


class PBFetcher:

    wait_time = 5

    updates_made = []

    distance_map = {
        '5k': {
            'profile-element':'#athlete-profile > div.row.no-margins > div.spans5.offset1.sidebar > div.section.comparison.borderless > div.running.hidden > table > tbody:nth-child(4) > tr:nth-child(4) > td:nth-child(2) > a'
        },
        '10k': {
            'profile-element':'#athlete-profile > div.row.no-margins > div.spans5.offset1.sidebar > div.section.comparison.borderless > div.running.hidden > table > tbody:nth-child(4) > tr:nth-child(5) > td:nth-child(2) > a'
        },
        'Half-Marathon': {
            'profile-element':'#athlete-profile > div.row.no-margins > div.spans5.offset1.sidebar > div.section.comparison.borderless > div.running.hidden > table > tbody:nth-child(4) > tr:nth-child(6) > td:nth-child(2) > a'
        },
    }

    def __init__(self):
        self.driver = self.get_driver()
        auth_json = self.get_auth_data()
        self.email = auth_json['email']
        self.password = auth_json['password']
        self.data = self.get_athlete_data()

    def main(self):
        self.login()
        for athlete_id in self.data:
            self.update_pbs(athlete_id)

        self.save_athlete_data()
        self.driver.close()

        for update in self.updates_made:
            athlete_id = update['athlete_id']
            distance = update['distance']
            print(f'Updated {athlete_id} {distance} pb')

        if self.updates_made is []:
            print('No updates made')

    def get_driver(self):
        return webdriver.Chrome(ChromeDriverManager().install())

    def login(self):
        self.driver.get('https://www.strava.com/login')
        email_field = self.driver.find_element_by_css_selector('#email')
        email_field.send_keys(self.email)
        password_field = self.driver.find_element_by_css_selector('#password')
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(2)

    def update_pbs(self, athlete_id):
        self.driver.get('https://www.strava.com/athletes/' + athlete_id)
        athlete_data = self.data.get(athlete_id)

        pbs_to_fetch = {}

        for distance in self.distance_map:
            if distance not in athlete_data:
                athlete_data[distance] = {}

            try:
                pb_element = WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.distance_map[distance]['profile-element']))
                )
            except TimeoutException:
                print(f'{distance} PB for athlete {athlete_id} not set')
                continue

            pb_time = pb_element.get_attribute('innerHTML')
            pb_url = pb_element.get_attribute("href")
            pb_id = re.findall('activities/([0-9]+)', pb_url)[0]

            if athlete_data[distance].get(pb_id) is not None:
                print(f'Already recorded {distance} {pb_id} for athlete: {athlete_id}')
                continue

            athlete_data[distance][pb_id] = {
                'time': pb_time,
                'url': 'https://www.strava.com/activities/' + pb_id + '/overview'
            }

            pbs_to_fetch[distance] = pb_id

        for distance in pbs_to_fetch:
            pb_id = pbs_to_fetch[distance]
            print(f'Fetching new {distance} {pb_id} for athlete: {athlete_id}')
            self.driver.get('https://www.strava.com/activities/' + pb_id)

            time_element = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#heading time'))
            )

            athlete_data[distance][pb_id]['date'] = time_element.text

            self.data[athlete_id] = athlete_data
            self.save_athlete_data()
            self.updates_made.append({'athlete_id': athlete_id, 'distance': distance})

    def get_auth_data(self):
        with open('auth.json') as auth_json:
            return json.load(auth_json)

    def get_athlete_data(self):
        with open('athlete_data.json') as athlete_data_json:
            return json.load(athlete_data_json)

    def save_athlete_data(self):
        with open('athlete_data.json', 'w') as outfile:
            json.dump(self.data, outfile, indent=2)


pb_fetcher = PBFetcher()
pb_fetcher.main()
