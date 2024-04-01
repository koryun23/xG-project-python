
from json_to_csv_converter import *

from scrapers.FBRefParser import FBRefParser
from scrapers.UnderstatParser import UnderstatParser
from scrapers.FotMobParser import FotMobParser

def push_json_data_to_file(self, json_data, filename="understat-epl/epl-2022-2023.json"):
    with open(filename, "w") as epl2023:
        json.dump(json_data, epl2023)


class ShotAnalyzer:
    # def __init__(self):
    #    # expecting to get a python dictionary
    #    self.filtered_json_data = self.__filter(json_data)

    # private method
    def __filter(self, __json_data):
        # json_data must include match_info and shot_data
        # must return a dictionary consisting of shots

        data = __json_data["data"]
        all_shot_list = []
        for item in data:
            match_info = item["match_info"]
            shot_data = item["shot_data"]
            home_team_shot_data_list = shot_data["h"]
            away_team_shot_data_list = shot_data["a"]
            all_shot_data_list = home_team_shot_data_list + away_team_shot_data_list
            for shot_data in all_shot_data_list:
                filtered_shot_data = {
                    "home_team": match_info["team_h"],
                    "away_team": match_info["team_a"],
                    "home_team_goals": match_info["h_goals"],
                    "away_team_goals": match_info["a_goals"],
                    "home_team_xg": match_info["h_xg"],
                    "away_team_xg": match_info["a_xg"],
                    "result": shot_data["result"],
                    "X": shot_data["X"],
                    "Y": shot_data["Y"],
                    "xg": shot_data["xG"],
                    "player": shot_data["player"],
                    "situation": shot_data["situation"],
                    "home_team": shot_data["h_team"],
                    "away_team": shot_data["a_team"],
                    "home_team_goals": shot_data["h_goals"],
                    "away_team_goals": shot_data["a_goals"],
                    "shot_taken_by": shot_data["h_a"]
                }

                all_shot_list.append(filtered_shot_data)
        return {
            "all_shots": all_shot_list
        }

    def extract_all(self, __json_data):
        return self.__filter(__json_data)

    def extract_shots_for_team(self, __json_data, __team_name):
        __json_data = self.__filter(__json_data)["all_shots"]
        result = []
        for item in __json_data:
            if (item["home_team"] == __team_name and item["shot_taken_by"] == "h") or \
                    (item["away_team"] == __team_name and item["shot_taken_by"] == "a"):
                # take the shot data and match_info
                result.append(item)
        return {
            "all_shots": result
        }

    def extract_shots_against_team(self, __json_data, __team_name):
        __json_data = self.__filter(__json_data)["all_shots"]
        result = []
        for item in __json_data:
            if (item["home_team"] == __team_name and item["shot_taken_by"] == "a") or \
                    (item["away_team"] == __team_name and item["shot_taken_by"] == "h"):
                # take the shot data and match_info
                result.append(item)
        return {
            "all_shots": result
        }

urls = ['https://www.fotmob.com/matches/tottenham-hotspur-vs-marseille/2fup9r#4010182',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-sporting-cp/2sajmr#4010184',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-eintracht-frankfurt/2sr360#4010186',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-eintracht-frankfurt/2sr360#4010187',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-sporting-cp/2sajmr#4010190',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-marseille/2fup9r#4010192',
                                  'https://www.fotmob.com/matches/ac-milan-vs-tottenham-hotspur/2fkeff#4060606',
                                  'https://www.fotmob.com/matches/ac-milan-vs-tottenham-hotspur/2fkeff#4060607']


fotMobParser = FotMobParser()
urls = ['https://www.fotmob.com/matches/tottenham-hotspur-vs-marseille/2fup9r#4010182',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-sporting-cp/2sajmr#4010184',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-eintracht-frankfurt/2sr360#4010186',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-eintracht-frankfurt/2sr360#4010187',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-sporting-cp/2sajmr#4010190',
                                  'https://www.fotmob.com/matches/tottenham-hotspur-vs-marseille/2fup9r#4010192',
                                  'https://www.fotmob.com/matches/ac-milan-vs-tottenham-hotspur/2fkeff#4060606',
                                  'https://www.fotmob.com/matches/ac-milan-vs-tottenham-hotspur/2fkeff#4060607']
current_game = fotMobParser.parse_shot_data_from_url(False, urls[7])
with open("ucl-2022-2023/ucl-shots-by-top-4.json", "r") as shots_by_top_4_json:
    final_result = json.load(shots_by_top_4_json)
with open("ucl-2022-2023/ucl-shots-by-top-4.json", "w") as shots_by_top_4_json:
    final_result += current_game
    json.dump(final_result, shots_by_top_4_json)

# with open("ucl-2022-2023/ucl-shots-against-top-4.json", "r") as shots_by_matches_json:
#     final_result = json.load(shots_by_matches_json)
# with open("ucl-2022-2023/ucl-shots-against-top-4.json", "w") as shots_by_matches_json:
#     final_result += current_game
#     json.dump(final_result, shots_by_matches_json)






# bd1 = fotMobParser.parse_shot_data_from_url(True, 'https://www.fotmob.com/matches/manchester-city-vs-borussia-dortmund/2r3sj0#4010230')
# kobenhavn1 = fotMobParser.parse_shot_data_from_url(True, 'https://www.fotmob.com/matches/fc-kobenhavn-vs-manchester-city/2ci00w#4010158')
# kobenhavn2 = fotMobParser.parse_shot_data_from_url(True, 'https://www.fotmob.com/matches/fc-kobenhavn-vs-manchester-city/2ci00w#4010160')
# bd2 = fotMobParser.parse_shot_data_from_url(True, 'https://www.fotmob.com/matches/manchester-city-vs-borussia-dortmund/2r3sj0#4010233')
# sevilla2 = fotMobParser.parse_shot_data_from_url(True, 'https://www.fotmob.com/matches/sevilla-vs-manchester-city/2bly45#4010234')
#
# teams_2021 = ["Manchester City", "Manchester United", "Chelsea", "Liverpool"]
# teams_2022 = ["Manchester City", "Liverpool", "Chelsea", "Tottenham"]
# understat = UnderstatParser()
# final_standings = understat.get_final_standings("2021")
# for team in final_standings:
#     rank = team["\u2116"]
#     team.pop("\u2116")
#     team["No"] = rank
# with open("understat-epl/epl-2021-2022-standings.json", "w") as final_standings_json:
#     json.dump(final_standings, final_standings_json)
#
# expected_standings = understat.get_expected_standings(2021)
# with open("understat-epl/epl-2021-2022-expected-standings.json", "w") as expected_standings_json:
#     json.dump(expected_standings, expected_standings_json)
#
# expected_standings_top_4 = understat.get_expected_rank_of_top_4(2021, teams_2021)
# with open("understat-epl/epl-2021-2022-standings-top-4.json", "w") as expected_standings_top_4_json:
#     json.dump(expected_standings_top_4, expected_standings_top_4_json)



#print(understat.get_final_standings())
# expected_standings = understat.get_expected_standings()
# with open("understat-epl/epl-2022-2023-expected-standings.json", "w") as expected_standings_json:
#     json.dump(expected_standings, expected_standings_json)
#
# top_4_expected_standings = understat.get_expected_rank_of_top_4()
# with open("understat-epl/epl-2022-2023-standings-top-4.json", "w") as top_4_expected_standings_json:
#     json.dump(top_4_expected_standings, top_4_expected_standings_json)

# teams = ["Manchester City", "Liverpool", "Chelsea", "Tottenham"]
# ucl_play_off_stats_top_4 = []
# with open("ucl-2022-2023/ucl-2022-2023-play-off-stats.json", "r") as ucl_play_off_stats_json:
#     ucl_play_off_stats = json.load(ucl_play_off_stats_json)
#     for team in ucl_play_off_stats:
#         team["xg_diff_per_game"] = team["xg_diff"] / team["games"]
#
# with open("ucl-2022-2023/ucl-2022-2023-play-off-stats.json", "w") as ucl_play_off_stats_json:
#     json.dump(ucl_play_off_stats, ucl_play_off_stats_json)
#
# with open("ucl-2022-2023/ucl-2022-2023-play-off-stats.json", "r") as ucl_play_off_stats_json:
#     ucl_play_off_stats = json.load(ucl_play_off_stats_json)
#     for team in ucl_play_off_stats:
#         if team["team"] in teams:
#             ucl_play_off_stats_top_4.append(team)
#
# with open("ucl-2022-2023/ucl-2022-2023-play-off-stats-top-4.json", "w") as ucl_play_off_stats_top_4_json:
#     json.dump(ucl_play_off_stats_top_4, ucl_play_off_stats_top_4_json)

# group_stage_stats = fbref.get_ucl_group_stage_stats()
# overall_stats = fbref.get_ucl_overall_stats()
# play_off_stats = fbref.get_ucl_play_off_stats()
# print(group_stage_stats)
# print(overall_stats)
# print(play_off_stats)
# with open("ucl-2022-2023/ucl-2022-2023-group-stage-stats.json", "w") as group_stage_stats_json:
#     json.dump(group_stage_stats, group_stage_stats_json)
# with open("ucl-2022-2023/ucl-2022-2023-play-off-stats.json", "w") as play_off_stats_json:
#     json.dump(play_off_stats, play_off_stats_json)
# with open("ucl-2022-2023/ucl-2022-2023-overall-stats.json", "w") as overall_stats_json:
#     json.dump(overall_stats, overall_stats_json)

analyzer = ShotAnalyzer()
