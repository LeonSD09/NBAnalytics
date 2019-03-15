# Imports
import nba_api as nba
import pandas as pd

"""==================================================================================================================
Test Player Stat Data Logic from nba_api
=================================================================================================================="""
# Use LeagueDashPlayerStats endpoint
from nba_api.stats.endpoints import leaguedashplayerstats
"""
Docs
https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguedashplayerstats.md
"""

"""==================================================================================================================
# Determine available data points for each measure type
(Base)|(Advanced)|(Misc)|(Four Factors)|(Scoring)|(Opponent)|(Usage)|(Defense)

Note: Four Factors, Opponent, and Defense returned errors - skipped for now
=================================================================================================================="""

def get_columns_for_measure_type(measure_type):
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        last_n_games=0,
        season='2018-19',
        measure_type_detailed_defense=measure_type,
        month=0,
        opponent_team_id=0,
        period=0,
        date_from_nullable='2018-02-01',
        date_to_nullable='2018-02-01'
    )
    return player_stats.get_dict()['resultSets'][0]['headers']

get_columns_for_measure_type('Base')
get_columns_for_measure_type('Advanced')
get_columns_for_measure_type('Misc')
get_columns_for_measure_type('Scoring')
get_columns_for_measure_type('Usage')

"""==================================================================================================================
# Create UDF that returns team ID
=================================================================================================================="""
import nba_api.stats.static.teams as teams
teams.get_teams()

team_full_name_map = {}
for dict in teams.get_teams():
    team_full_name_map[dict['full_name']] = dict['id']

team_full_name_map['Atlanta Hawks']

team = 'Boston Celtics'
if isinstance(team, str):
    print(teams.find_teams_by_full_name(team)[0]['id'])

def team_full_name_to_id(team_full_name):
    if isinstance(team_full_name, str):
        return teams.find_teams_by_full_name(team_full_name)[0]['id']

"""==================================================================================================================
# Determine list utlization by endpoint
=================================================================================================================="""

team_list = ['Philadelphia 76ers', 'Toronto Raptors']
team_id_list = [team_full_name_to_id(tm) for tm in team_list]
team_id_list

player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
    last_n_games=0,
    season='2018-19',
    measure_type_detailed_defense='Base',
    month=0,
    opponent_team_id=0,
    period=0,
    date_from_nullable='2019-01-01',
    date_to_nullable='2019-01-31',
    team_id_nullable=team_id_list)
header = player_stats.get_dict()['resultSets'][0]['headers']
data = player_stats.get_dict()['resultSets'][0]['rowSet']
pd.DataFrame(data=data, columns=header).sample(10)

# Looks like if list is passed, only first value passed gets pulled from endpoint

"""==================================================================================================================
# Create UDF that returns data given dimensions (to be made available in dashboard)
=================================================================================================================="""
from datetime import date, timedelta
yesterday = (date.today() - timedelta(1)).strftime('%Y-%m-%d')
print(yesterday)

from nba_api.stats.library.parameters import *
"""
Information about paramaters and their values:
https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/library/parameters.md
"""

print(PeriodNullable.default)
print(PaceAdjust.default)
print(ShotClockRangeNullable.default)
print(LeagueIDNullable.default)

def get_player_stats_df(
    date_from='2018-10-16',
    date_to=(date.today() - timedelta(1)).strftime('%Y-%m-%d'),
    team=0,
    opp_team=0,
    division=DivisionNullable.default,
    vs_division=DivisionNullable.default,
    conference=ConferenceNullable.default,
    vs_conference=ConferenceNullable.default,
    period=0,
    game_segment=GameSegmentNullable.default,
    home_away=LocationNullable.default,
    outcome=OutcomeNullable.default,
    player_position=PlayerPositionAbbreviationNullable.default,
    player_experience=PlayerExperienceNullable.default,
    starter_bench=StarterBenchNullable.default,
    shot_clock_range=ShotClockRangeNullable.default
):

    # Convert team name inputs to ID lists, if applicable
    if opp_team != 0:
        opp_team = [team_full_name_to_id(tm) for tm in opp_team]
    if team != 0:
        team = [team_full_name_to_id(tm) for tm in team]

    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        last_n_games=0,
        season='2018-19',
        measure_type_detailed_defense='Base',
        month=0,
        opponent_team_id=opp_team,
        period=period,
        date_from_nullable=date_from,
        date_to_nullable=date_to,
        team_id_nullable=team,
        division_simple_nullable=division,
        vs_division_nullable=vs_division,
        conference_nullable=conference,
        vs_conference_nullable=vs_conference,
        game_segment_nullable=game_segment,
        location_nullable=home_away,
        outcome_nullable=outcome,
        player_position_abbreviation_nullable=player_position,
        player_experience_nullable=player_experience,
        starter_bench_nullable=starter_bench,
        shot_clock_range_nullable=shot_clock_range)
    header = player_stats.get_dict()['resultSets'][0]['headers']
    data = player_stats.get_dict()['resultSets'][0]['rowSet']
    return pd.DataFrame(data=data, columns=header)

# Second Quarter on February 1 in a Win
test_data = get_player_stats_df(date_from=yesterday,
                                date_to=yesterday,
                                period=2,
                                outcome='W')
test_data.sample(10)

# January Celtics' Wins
test_data = get_player_stats_df(date_from='2019-01-01',
                                date_to='2019-01-31',
                                team='Boston Celtics',
                                outcome='W')
test_data.sample(10)

# Testing List Functionality
# Celtics, Sixers in QTRs 1,3 - Jan 26 through Feb 2
test_data = get_player_stats_df(date_from='2019-01-26',
                                date_to='2019-02-02',
                                team=['Boston Celtics', 'Philadelphia 76ers'],
                                period=[1,3])
test_data.sample(10)
test_data.TEAM_ABBREVIATION.unique()
# Only first value gets used


test_data = get_player_stats_df(date_from='2018-10-16',
                                date_to='2019-01-31',
                                period='9')
test_data.head()
