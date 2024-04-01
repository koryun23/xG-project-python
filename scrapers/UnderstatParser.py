import math
import time
import urllib.request

from bs4 import BeautifulSoup
import requests
import httpx
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from json_to_csv_converter import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class UnderstatParser:

    def get_shot_and_match_data_in_single_match(self, url):
        # url = "https://understat.com/match/16126"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        all_scripts = soup.find_all("script")
        print(len(all_scripts))
        strings = all_scripts[1].string
        shot_data_index_start = strings.index("('") + 2
        shot_data_index_end = strings.index("')")
        print(strings)
        shot_data_json = strings[shot_data_index_start: shot_data_index_end]
        shot_data_json = shot_data_json.encode("utf8").decode("unicode_escape")
        shot_data = json.loads(shot_data_json)
        print(shot_data)

        match_info_index_start = strings.index("match_info 	= JSON.parse('") + len("match_info 	= JSON.parse('")
        match_info_index_end = strings.index("');")
        match_info_json = strings[match_info_index_start: match_info_index_end]
        match_info_json = match_info_json.encode("utf8").decode("unicode_escape")
        match_info_data = json.loads(match_info_json)

        return {
            "match_info": match_info_data,
            "shot_data": shot_data
        }

    # understat
    def get_shot_and_match_data_in_epl(self):
        season_data = {
            "season": "2022-2023",
            "data": []
        }
        url = "https://understat.com/league/EPL/2022"
        driver = webdriver.Chrome()
        driver.get(url)
        calendar = driver.find_element_by_class_name("calendar")
        prev_button = calendar.find_element_by_class_name("calendar-prev")
        next_button = calendar.find_element_by_class_name("calendar-next")
        while not prev_button.get_attribute("disabled"):  # bad practice
            time.sleep(1)  # very very bad practice
            prev_button.click()
            time.sleep(1)  # again very very very bad practice
            all_calendar_games = driver.find_elements_by_class_name("calendar-game")
            for game in all_calendar_games:
                current_game_link = game.find_element_by_class_name("match-info").get_attribute("href")
                match_data = self.get_shot_and_match_data_in_single_match(current_game_link)
                season_data["data"].append(match_data)
        self.push_json_data_to_file(season_data)
        return season_data

    def get_final_standings(self, year):
        result = []
        url = f"https://understat.com/league/EPL/{year}"
        driver = webdriver.Chrome()
        driver.get(url)
        WebDriverWait(driver, 2)
        table = driver.find_element_by_id("league-chemp").find_element_by_tag_name("table")
        table_head_row = table.find_element_by_tag_name("thead").find_element_by_tag_name("tr")
        table_head_row_data_list = table_head_row.find_elements_by_tag_name("th")
        table_body = table.find_element_by_tag_name("tbody")
        table_body_rows = table_body.find_elements_by_tag_name("tr")
        for i in range(len(table_body_rows)):
            current_team_data = {}
            current_row = table_body_rows[i]
            current_row_data_list = current_row.find_elements_by_tag_name("td")
            for j in range(len(current_row_data_list)):
                current_item = current_row_data_list[j]
                if current_item.text.rfind("+") != -1:
                    current_row_data_list[j] = current_item.text[:current_item.text.index("+")]
                    current_team_data[table_head_row_data_list[j].find_element_by_tag_name("span").text] = current_row_data_list[j]

                elif current_item.text.rfind("-") != -1:
                    current_row_data_list[j] = current_item.text[:current_item.text.index("-")]
                    current_team_data[table_head_row_data_list[j].find_element_by_tag_name("span").text] = current_row_data_list[j]

                else:
                    current_team_data[table_head_row_data_list[j].find_element_by_tag_name("span").text] = current_row_data_list[j].text
            result.append(current_team_data)
        return result

    def get_expected_standings(self, year):
        with open(f"understat-epl/epl-{year}-{year+1}-standings.json") as final_standings:
            standings = json.load(final_standings)
            standings.sort(key=lambda team: float(team['xPTS']), reverse=True)
            for i in range(len(standings)):
                standings[i]["xRank"] = i + 1
            return standings

    def get_expected_rank_of_top_4(self, year, teams):
        result = []
        with open(f"understat-epl/epl-{year}-{year+1}-expected-standings.json") as expected_standings:
            expected_standings_list = json.load(expected_standings)
            for team in expected_standings_list:
                if team['Team'] in teams:
                    result.append(team)
        return result

    @staticmethod
    def push_json_data_to_file(json_data, filename="understat-epl/epl-2022-2023.json"):
        with open(filename, "w") as epl2023:
            json.dump(json_data, epl2023)