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

# width = 105, height = 68
FIELD_WIDTH = 105

class FotMobParser:

    def __init__(self):
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--lang=en')
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "https://www.fotmob.com/leagues/42/matches/champions-league?season=2022-2023"
        self.urls_from_teams = {
            'Manchester City': ['https://www.fotmob.com/matches/sevilla-vs-manchester-city/2bly45#4010157',
                                'https://www.fotmob.com/matches/manchester-city-vs-borussia-dortmund/2r3sj0#4010230',
                                'https://www.fotmob.com/matches/fc-kobenhavn-vs-manchester-city/2ci00w#4010158',
                                'https://www.fotmob.com/matches/fc-kobenhavn-vs-manchester-city/2ci00w#4010160',
                                'https://www.fotmob.com/matches/manchester-city-vs-borussia-dortmund/2r3sj0#4010233',
                                'https://www.fotmob.com/matches/sevilla-vs-manchester-city/2bly45#4010234',
                                'https://www.fotmob.com/matches/manchester-city-vs-rb-leipzig/80y7706#4060600',
                                'https://www.fotmob.com/matches/manchester-city-vs-rb-leipzig/80y7706#4060601',
                                'https://www.fotmob.com/matches/manchester-city-vs-bayern-munchen/2rh3nv#4140600',
                                'https://www.fotmob.com/matches/manchester-city-vs-bayern-munchen/2rh3nv#4140601',
                                'https://www.fotmob.com/matches/manchester-city-vs-real-madrid/2ey0nu#4140606',
                                'https://www.fotmob.com/matches/manchester-city-vs-real-madrid/2ey0nu#4140607',
                                'https://www.fotmob.com/matches/manchester-city-vs-inter/2ez486#4140608'],
            'Liverpool': ['https://www.fotmob.com/matches/liverpool-vs-napoli/2u64rq#4010119',
                          'https://www.fotmob.com/matches/ajax-vs-liverpool/2giois#4010120',
                          'https://www.fotmob.com/matches/rangers-vs-liverpool/2g22kj#4010125',
                          'https://www.fotmob.com/matches/rangers-vs-liverpool/2g22kj#4010127',
                          'https://www.fotmob.com/matches/ajax-vs-liverpool/2giois#4010129',
                          'https://www.fotmob.com/matches/liverpool-vs-napoli/2u64rq#4010130',
                          'https://www.fotmob.com/matches/real-madrid-vs-liverpool/2gxhcg#4060604',
                          'https://www.fotmob.com/matches/real-madrid-vs-liverpool/2gxhcg#4060605'],
            'Chelsea': ['https://www.fotmob.com/matches/chelsea-vs-dinamo-zagreb/2v4bud#4010132',
                        'https://www.fotmob.com/matches/chelsea-vs-salzburg/2tji5d#4010206',
                        'https://www.fotmob.com/matches/chelsea-vs-ac-milan/2e8fge#4010135',
                        'https://www.fotmob.com/matches/chelsea-vs-ac-milan/2e8fge#4010137',
                        'https://www.fotmob.com/matches/chelsea-vs-salzburg/2tji5d#4010207',
                        'https://www.fotmob.com/matches/chelsea-vs-dinamo-zagreb/2v4bud#4010210',
                        'https://www.fotmob.com/matches/chelsea-vs-borussia-dortmund/2r3eg7#4060610',
                        'https://www.fotmob.com/matches/chelsea-vs-borussia-dortmund/2r3eg7#4060611',
                        'https://www.fotmob.com/matches/chelsea-vs-real-madrid/2exnh5#4140596',
                        'https://www.fotmob.com/matches/chelsea-vs-real-madrid/2exnh5#4140597'],
            'Tottenham Hotspur': ['https://www.fotmob.com/matches/tottenham-hotspur-vs-marseille/2fup9r#4010182',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-sporting-cp/2sajmr#4010184',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-eintracht-frankfurt/2sr360#4010186',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-eintracht-frankfurt/2sr360#4010187',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-sporting-cp/2sajmr#4010190',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-marseille/2fup9r#4010192',
                                  'https://www.fotmob.com/matches/ac-milan-vs-tottenham-hotspur/2fkeff#4060606',
                                  'https://www.fotmob.com/matches/ac-milan-vs-tottenham-hotspur/2fkeff#4060607']}
        self.all_shot_coordinates = {
            # url - array of coordinates
        }
        self.color_from_name = {
            "Manchester City": ["#69A8D8"],
            "Liverpool": ["#d3171e", "#00A398"],
            "Chelsea": ["#EAD73A", "#064b95"],
            "Tottenham Hotspur": ["#132257"]
        }
        self.all_shots_data_from_url = {

        }

    def parseUrls(self):
        self.driver.get(self.base_url)

        for i in range(7, 17):
            url = self.base_url + f"&page={i}"
            self.driver.get(url)
            time.sleep(1)
            all_games = self.driver.find_elements_by_class_name("css-1fkfix2-LeagueMatchCSS")
            print(len(all_games))
            for game in all_games:
                team_names = game.find_element_by_class_name(
                    "css-1gpzk3u-MatchCSS-MatchDesktop-hideOnMobile").find_elements_by_class_name("css-czv0w8-TeamName")
                if team_names[0].text in self.urls_from_teams:
                    self.urls_from_teams[team_names[0].text].append(
                        game.find_element_by_tag_name("a").get_attribute("href"))
                elif team_names[1].text in self.urls_from_teams:
                    self.urls_from_teams[team_names[1].text].append(
                        game.find_element_by_tag_name("a").get_attribute("href"))
            time.sleep(1)
        print(self.urls_from_teams)
        # print(r.content)

    def parse_shot_data_from_url(self, against, url):
        team = "Tottenham Hotspur"
        self.driver.get(url)
        time.sleep(5)
        self.all_shots_data_from_url[url] = []
        [home_team, away_team, score] = WebDriverWait(self.driver, 15).until(lambda a: self.get_teams_playing())
        print(home_team, away_team, score)
        shotmapWrapper = WebDriverWait(self.driver, 15).until(
            lambda a: self.driver.find_element_by_class_name("css-v6f2wb-ShotmapWrapper"))
        pitchWrapper = WebDriverWait(self.driver, 15).until(
            lambda a: shotmapWrapper.find_element_by_class_name("css-1yqptsh-PitchWrapper"))
        print(len(pitchWrapper.find_elements_by_class_name("css-b4kkkk-PitchSVGWrapper")))
        all_shot_circles = WebDriverWait(self.driver, 15).until(lambda a: pitchWrapper.find_element_by_class_name("css-b4kkkk-PitchSVGWrapper").find_elements_by_id("fieldShot"))
        all_shots = []
        for shot in all_shot_circles:
            shot_data = {}
            if shot.tag_name == "use":  # is a goal
                if (not against and float(shot.get_attribute("x")) > FIELD_WIDTH / 2 and away_team in team) or \
                        (not against and float(shot.get_attribute("x")) < FIELD_WIDTH / 2 and home_team in team) or \
                        (against and float(shot.get_attribute("x")) > FIELD_WIDTH / 2 and home_team in team) or \
                        (against and float(shot.get_attribute("x")) < FIELD_WIDTH / 2 and away_team in team):
                    WebDriverWait(self.driver, 2)
                    ActionChains(self.driver).move_to_element(shot).click().perform()
                    shot_data = WebDriverWait(self.driver, 15).until(
                        lambda a: self.get_shot_data_from_shot_tag_and_shotmap_wrapper(shot, shotmapWrapper))
                    shot_data["team_for"] = away_team if (against and team == home_team) or (
                            not against and team == away_team) else home_team
                    shot_data["team_against"] = home_team if (against and team == home_team) or (
                            not against and team == away_team) else away_team

            elif (shot.get_attribute("fill") in self.color_from_name[team] and not against) or \
                    (shot.get_attribute("fill") not in self.color_from_name[team] and against):
                WebDriverWait(self.driver, 2)
                ActionChains(self.driver).move_to_element(shot).click().perform()
                shot_data = WebDriverWait(self.driver, 15).until(
                    lambda a: self.get_shot_data_from_shot_tag_and_shotmap_wrapper(shot, shotmapWrapper))
                if shot_data:
                    shot_data["team_for"] = away_team if (against and team == home_team) or (
                                not against and team == away_team) else home_team
                    shot_data["team_against"] = home_team if (against and team == home_team) or (
                                not against and team == away_team) else away_team
            if shot_data:
                if shot_data["Result"] != "Goal" or shot.tag_name == "use":
                    print(shot_data)
                    all_shots.append(shot_data)
        self.driver.close()
        return all_shots
    def parse_shot_data(self, against):
        for team in self.urls_from_teams:
            urls = self.urls_from_teams[team]
            for url in urls:
                self.driver.get(url)
                self.all_shots_data_from_url[url] = []
                [home_team, away_team, score] = WebDriverWait(self.driver, 15).until(lambda a: self.get_teams_playing())
                print(home_team, away_team, score)
                shotmapWrapper = WebDriverWait(self.driver, 15).until(lambda a: self.driver.find_element_by_class_name("css-v6f2wb-ShotmapWrapper"))
                pitchWrapper = WebDriverWait(self.driver, 15).until(lambda a: shotmapWrapper.find_element_by_class_name("css-1yqptsh-PitchWrapper"))
                all_shot_circles = WebDriverWait(self.driver, 15).until(lambda a: pitchWrapper.find_elements_by_id("fieldShot"))
                all_shots = []
                for shot in all_shot_circles:
                    shot_data = {}
                    if(not shot.get_attribute("fill")): # is a goal
                        if (not against and float(shot.get_attribute("x")) > FIELD_WIDTH / 2 and away_team in team) or \
                                (not against and float(shot.get_attribute("x")) < FIELD_WIDTH / 2 and home_team in team) or \
                                (against and float(shot.get_attribute("x")) > FIELD_WIDTH / 2 and home_team in team) or \
                                (against and float(shot.get_attribute("x")) < FIELD_WIDTH / 2 and away_team in team):

                            WebDriverWait(self.driver, 2)
                            ActionChains(self.driver).move_to_element(shot).click().perform()
                            WebDriverWait(self.driver, 2)
                            shot_data = WebDriverWait(self.driver, 15).until(lambda a: self.get_shot_data_from_shot_tag_and_shotmap_wrapper(shot, shotmapWrapper))
                            shot_data["team_for"] = away_team if (against and team == home_team) or (
                                        not against and team == away_team) else home_team
                            shot_data["team_against"] = home_team if (against and team == home_team) or (
                                        not against and team == away_team) else away_team

                    elif (shot.get_attribute("fill") in self.color_from_name[team] and not against) or \
                        (shot.get_attribute("fill") not in self.color_from_name[team] and against):
                        WebDriverWait(self.driver, 2)
                        ActionChains(self.driver).move_to_element(shot).click().perform()
                        WebDriverWait(self.driver, 2)
                        shot_data = WebDriverWait(self.driver, 15).until(lambda a: self.get_shot_data_from_shot_tag_and_shotmap_wrapper(shot, shotmapWrapper))
                        shot_data["team_for"] = away_team if (against and team == home_team) or (not against and team == away_team) else home_team
                        shot_data["team_against"] = home_team if (against and team == home_team) or (not against and team == away_team) else away_team
                    if shot_data:
                        print(shot_data)
                        all_shots.append(shot_data)
                """
                goal_shot_list = shotmapWrapper.find_element_by_class_name("css-1yqptsh-PitchWrapper")\
                    .find_elements_by_tag_name("g")
                for goal_shot in goal_shot_list:
                    if (float(goal_shot.get_attribute("x")) > FIELD_WIDTH / 2 and away_team in team) or \
                            (float(goal_shot.get_attribute("x")) < FIELD_WIDTH / 2 and home_team in team):
                        if against:
                            team_for = home_team if away_team == team else away_team
                            team_against = team
                        else:
                            team_for = team
                            team_against = home_team if away_team == team else away_team
                        shot_data = self.get_goal_data_from_shot_tag_and_shotmap_wrapper(goal_shot, shotmapWrapper)
                        shot_data["team_for"] = team_for
                        shot_data["team_against"] = team_against
                        all_shots.append(shot_data)
                """

                self.all_shots_data_from_url[url] = all_shots
            print(self.all_shots_data_from_url)
            # self.all_shot_coordinates[url] = coordinates

    def get_shot_data_from_shot_tag_and_shotmap_wrapper(self, shot, shotmapWrapper):
        shot_data = {}
        shot_info_div = shotmapWrapper.find_element_by_class_name(
            "css-11w9g1f-FullscreenShotInfoContainer")
        shot_info_list = shot_info_div.find_element_by_class_name(
            "css-s5r6e1-ShotInfo").find_element_by_tag_name("ul").find_elements_by_tag_name("li")
        shot_xg_data_list = shot_info_div.find_element_by_class_name(
            "css-fn6kl5-FullscreenGoalGraphics-commonGoalGraphics").find_element_by_class_name(
            "css-1ypll8-FullscreenXGContainer-commonXGContainer").find_elements_by_tag_name("span")
        shot_data["xg"] = shot_xg_data_list[0].text
        if shot.get_attribute("cx"):
            shot_data["x"] = shot.get_attribute("cx")
            shot_data["y"] = shot.get_attribute("cy")
        else:
            shot_data["x"] = shot.get_attribute("x")
            shot_data["y"] = shot.get_attribute("y")
        for shot_info in shot_info_list:
            type = shot_info.find_elements_by_tag_name("span")
            shot_data[type[0].text] = type[1].text
        return shot_data

    def get_goal_data_from_shot_tag_and_shotmap_wrapper(self, goal_shot, shotmapWrapper):
        shot_data = {}

        WebDriverWait(self.driver, 2)
        ActionChains(self.driver).move_to_element(goal_shot).click().perform()
        WebDriverWait(self.driver, 2)
        shot_info_div = shotmapWrapper.find_element_by_class_name(
            "css-11w9g1f-FullscreenShotInfoContainer")
        shot_info_list = shot_info_div.find_element_by_class_name(
            "css-s5r6e1-ShotInfo").find_element_by_tag_name("ul").find_elements_by_tag_name("li")
        shot_xg_data_list = shot_info_div.find_element_by_class_name(
            "css-fn6kl5-FullscreenGoalGraphics-commonGoalGraphics").find_element_by_class_name(
            "css-1ypll8-FullscreenXGContainer-commonXGContainer").find_elements_by_tag_name("span")
        shot_data["xg"] = shot_xg_data_list[0].text
        shot_data["x"] = goal_shot.get_attribute("x")
        shot_data["y"] = goal_shot.get_attribute("y")
        for shot_info in shot_info_list:
            type = shot_info.find_elements_by_tag_name("span")
            shot_data[type[0].text] = type[1].text
        print(shot_data)

        return shot_data

    def get_teams_playing(self):
        headers = WebDriverWait(self.driver, 15).until(lambda a: self.driver.find_elements_by_class_name(
            "css-1qvtz4y-MFHeaderFullscreenHeader"))
        header = headers[1]
        teams_playing = WebDriverWait(self.driver, 15).until(lambda a: header.find_elements_by_class_name(
            "e1rexsj40"))
        score_tag = WebDriverWait(self.driver, 15).until(lambda a: header.find_element_by_class_name("css-ta04x1-MFHeaderStatusScore-topRow"))
        score = score_tag.text
        home_team = teams_playing[0].text
        away_team = teams_playing[1].text
        return home_team, away_team, score

    def get_all_shots_by_team(self, team_name):
        result = []
        team_name = self.filter_team_name(team_name)
        with open("ucl-2022-2023/ucl-2022-2023-shots-links.json") as shots_json:
            all_shots_data_from_url = json.load(shots_json)
            for url in all_shots_data_from_url:
                if team_name in url:
                    shots = all_shots_data_from_url[url]
                    for shot in shots:
                        if self.filter_team_name(shot["team"]) in team_name:
                            print(len(shot))
                            result.append(shot)
                        else:
                            break
        return result


    def get_shots_of_all_teams(self):
        teams = ["Manchester City", "Liverpool", "Chelsea", "Tottenham Hotspur"]
        teams = [self.filter_team_name(team) for team in teams]
        return {team_name: self.get_all_shots_by_team(team_name) for team_name in teams}


    def filter_team_name(self, team_name):
        filtered = ""
        "asd".lower()
        for s in team_name:
            if s.isupper():
                filtered += s.lower()
            elif s == ' ':
                filtered += "-"
            else:
                filtered += s
        return filtered
