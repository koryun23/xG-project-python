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


class FBRefParser:

    def __init__(self):

        self.url_by_domestic_league = {
            "premier-league": "https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats",
            "La Liga": "https://fbref.com/en/comps/12/2022-2023/2022-2023-La-Liga-Stats",
            "Bundesliga": "https://fbref.com/en/comps/20/2022-2023/2022-2023-Bundesliga-Stats",
            "Serie A": "https://fbref.com/en/comps/11/2022-2023/2022-2023-Serie-A-Stats",
            "Ligue 1": "https://fbref.com/en/comps/13/2022-2023/2022-2023-Ligue-1-Stats"
        }

        self.url_by_continental_league = {
            "ucl-2022-2023": "https://fbref.com/en/comps/8/2022-2023/2022-2023-Champions-League-Stats"
        }

    # fbref
    def get_all_data_in_top_5_leagues(self):
        for league in self.url_by_domestic_league:
            for i in range(2000, 2023):
                time.sleep(5)
                season = f"{i}-{i + 1}"
                stats_by_season_and_league = self.get_stats_by_season_and_league_top_5(season, league)
                with open(f"{league} {season}", "w") as file:
                    json.dump(stats_by_season_and_league, file)

    # fbref
    def get_stats_by_season_and_league_top_5(self, season, league):
        soup = BeautifulSoup(requests.get(self.url_by_domestic_league[league].replace("2022-2023", season)).content,
                             "html.parser")
        data = {}
        stats_div_list = soup.find_all("div", {"class": "table_wrapper tabbed"})
        at_regular_season_div = True  # First table is always regular season table where th represents the rank rather than
        # the team name
        for stats_div in stats_div_list:
            stats_table = stats_div.find("table").find("tbody")
            stats_table_rows = stats_table.find_all("tr")
            for row in stats_table_rows:
                if at_regular_season_div:
                    current_team_name = row.find("td").text.strip()
                else:
                    current_team_name = row.find("th").text.strip()
                current_team_stats = row.find_all("td")
                for stat in current_team_stats:
                    if current_team_name in data:
                        data[current_team_name][stats_div["id"] + " " + stat["data-stat"]] = stat.text
                    else:
                        data[current_team_name] = {}
            at_regular_season_div = False  # Starting from second table, the flag should be down, as the team name is tr
        print(data)
        return data



    def get_ucl_group_stage_stats(self):
        group_stage_data = []
        soup = BeautifulSoup(requests.get(self.url_by_continental_league["ucl-2022-2023"]).content, "html.parser")
        group_stage_div = soup.find("div", {"class": "section_wrapper"})
        all_groups_list = group_stage_div.find_all("div", {"class": "table_wrapper"})
        for group in all_groups_list:
            group_table = group.find("table").find("tbody").find_all("tr")
            for row in group_table:
                current_team_stats = {}
                td_list = row.find_all("td")
                for td in td_list:
                    if td["data-stat"] == "team":
                        current_team_stats[td["data-stat"]] = self.filter_team_name(td.text)
                    else:
                        current_team_stats[td["data-stat"]] = td.text
                group_stage_data.append(current_team_stats)
        return group_stage_data

    def get_ucl_overall_stats(self):
        all_data = []
        soup = BeautifulSoup(requests.get(self.url_by_continental_league["ucl-2022-2023"]).content, "html.parser")
        all_stats_table = soup.find("div", {"id": "switcher_results2022-202380"}).find("div").find("table").find(
            "tbody").find_all("tr")
        for table_row in all_stats_table:
            if table_row.get("class") and "blank_table" in table_row.get("class"):
                continue
            current_team_stats = {}
            td_list = table_row.find_all("td")
            rank = table_row.find("th")
            current_team_stats[rank["data-stat"]] = rank.text
            for td in td_list:
                if td["data-stat"] == "team":
                    current_team_stats[td["data-stat"]] = self.filter_team_name(td.text)
                else:
                    current_team_stats[td["data-stat"]] = td.text
            all_data.append(current_team_stats)
        return all_data

    def get_ucl_play_off_stats(self):
        result = []
        group_stage_stat_list = self.get_ucl_group_stage_stats()
        overall_stat_list = self.get_ucl_overall_stats()
        for group_stage_stat in group_stage_stat_list:
            current_team_play_off_stat = {}
            current_team_overall_stats = {}
            for overall_stat in overall_stat_list:
                if overall_stat["team"] == group_stage_stat["team"]:
                    current_team_overall_stats = overall_stat
                    break
            for stat in group_stage_stat:
                if group_stage_stat[stat].replace(".", "").isnumeric():
                    value = float(current_team_overall_stats[stat]) - float(group_stage_stat[stat])
                    if stat == "games" and value == 0:
                        break
                    current_team_play_off_stat[stat] = float(current_team_overall_stats[stat]) - float(group_stage_stat[stat])
                else:
                    current_team_play_off_stat[stat] = group_stage_stat[stat]
            if len(current_team_play_off_stat) > 1:
                result.append(current_team_play_off_stat)
        return result

    def filter_team_name(self, team_name):
        for i in range(len(team_name)):
            if team_name[i].isupper():
                return team_name[i:]

