# Imports
import pandas as pd
from datetime import date, timedelta
from nba_api.stats.endpoints import leaguedashplayerstats
import nba_api.stats.static.teams as teams
from nba_api.stats.library.parameters import *

# Measure Types
measure_type_dict = {
    'Base': 'Base',
    'Advanced': 'Advanced',
    'Misc': 'Misc',
    'Scoring': 'Scoring',
    'Usage': 'Usage',
}

# Pre-populate team values
team_dict = {tm_dict['full_name']: tm_dict['id'] for tm_dict in teams.get_teams()}
team_dict['All'] = 0
team_dict['Los Angeles Lakers']
team_dict['All']

# Division values
div_dict = {'All': DivisionNullable.default,
            'Atlantic': 'Atlantic',
            'Central': 'Central',
            'Northwest': 'Northwest',
            'Pacific': 'Pacific',
            'Southeast': 'Southeast',
            'Southwest': 'Southwest',
            }

# Conference values
conf_dict = {'All': ConferenceNullable.default,
             'East':'East',
             'West':'West',
             }

# Period values
period_dict = {'All': 0,
               'First': '1',
               'Second': '2',
               'Third': '3',
               'Fourth': '4',
               }

# Game Segment values
game_segment_dict = {'All': GameSegmentNullable.default,
                     'First Half': 'First Half',
                     'Overtime': 'Overtime',
                     'Second Half': 'Second Half'
                     }

# Home/Away values
home_away_dict = {'All': LocationNullable.default,
                  'Home': 'Home',
                  'Road': 'Road',
                  }

# Outcome values
outcome_dict = {'All': OutcomeNullable.default,
                'Win': 'W',
                'Loss': 'L',
                }

# Player Position values
player_pos_dict = {'All': PlayerPositionAbbreviationNullable.default,
                   'Forward':'F',
                   'Center': 'C',
                   'Guard': 'G',
                   'Center-Forward': 'C-F',
                   'Forward-Center': 'F-C',
                   'Forward-Guard': 'F-G',
                   'Guard-Forward': 'G-F',
                   }

# Player Experience values
player_exp_dict = {'All': PlayerExperienceNullable.default,
                   'Rookie': 'Rookie',
                   'Sophomore': 'Sophomore',
                   'Veteran': 'Veteran',
                   }

# Starter/Bench values
starter_bench_dict = {'All': StarterBenchNullable.default,
                      'Starters': 'Starters',
                      'Bench': 'Bench',
                     }

# Shot Clock Range values
shot_clock_dict = {'All': ShotClockRangeNullable.default,
                   '24s - 22s': '24-22',
                   '22s - 18s: Very Early': '22-18 Very Early',
                   '18s - 15s: Early': '18-15 Early',
                   '15s - 7s: Average': '15-7 Average',
                   '7s - 4s: Late': '7-4 Late',
                   '4s - 0s: Very Late': '4-0 Very Late',
                   'ShotClock Off': 'ShotClock Off',
                  }

class StatCrosser_Utils:

    def __init__(self):
        self.measure_type_opts = measure_type_dict
        self.opp_team_opts = team_dict
        self.team_opts = team_dict
        self.division_opts = div_dict
        self.vs_division_opts = div_dict
        self.conference_opts = conf_dict
        self.vs_conference_opts = conf_dict
        self.period_opts = period_dict
        self.game_segment_opts = game_segment_dict
        self.home_away_opts = home_away_dict
        self.outcome_opts = outcome_dict
        self.player_position_opts = player_pos_dict
        self.player_experience_opts = player_exp_dict
        self.starter_bench_opts = starter_bench_dict
        self.shot_clock_range_opts = shot_clock_dict

    # UDF that returns team ID given full team name
    def team_full_name_to_id(team_full_name):
        if isinstance(team_full_name, str):
            return teams.find_teams_by_full_name(team_full_name)[0]['id']

    # UDF that returns data given dimensions (to be made available in dashboard)
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



sc_u = StatCrosser_Utils()
sc_u.shot_clock_range_opts
