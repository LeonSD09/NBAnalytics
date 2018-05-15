import nba_py as nba
import pandas as pd
import json

# Get Scoreboard data for March 10, 2018
sb = nba_py.Scoreboard(month=03, day=10, year=2018, offset=0)

# Print Keys
for key, value in sb.json.iteritems() :
	print key

"""
resource
resultSets
parameters
"""

sb_resource = sb.json['resource'] 
# The endpoint used to acquire the data
# 'scoreboard'

sb_results = sb.json['resultSets'] 
# A list of dictionaries with all of the data
for key, value in sb_results[0].iteritems() :
	print key
"""
headers
rowSet
name
"""

sb_parameters = sb.json['parameters'] 
# A dictionary with the input parameters 
# Print data in paramaters dict
for key, value in sb_parameters.iteritems():
	print '{}:\t{}'.format(key, value)
"""
LeagueID:	00
GameDate:	03/10/2018
DayOffset:	0
"""	

# Data Name
for result in sb_results:
	print result['name']
"""
GameHeader
LineScore
SeriesStandings
LastMeeting
EastConfStandingsByDay
WestConfStandingsByDay
Available
"""

# Column names
for result in sb_results:
	print result['headers']
"""
[u'GAME_DATE_EST', u'GAME_SEQUENCE', u'GAME_ID', u'GAME_STATUS_ID', u'GAME_STATUS_TEXT', u'GAMECODE', u'HOME_TEAM_ID', u'VISITOR_TEAM_ID', u'SEASON', u'LIVE_PERIOD', u'LIVE_PC_TIME', u'NATL_TV_BROADCASTER_ABBREVIATION', u'LIVE_PERIOD_TIME_BCAST', u'WH_STATUS']
[u'GAME_DATE_EST', u'GAME_SEQUENCE', u'GAME_ID', u'TEAM_ID', u'TEAM_ABBREVIATION', u'TEAM_CITY_NAME', u'TEAM_WINS_LOSSES', u'PTS_QTR1', u'PTS_QTR2', u'PTS_QTR3', u'PTS_QTR4', u'PTS_OT1', u'PTS_OT2', u'PTS_OT3', u'PTS_OT4', u'PTS_OT5', u'PTS_OT6', u'PTS_OT7', u'PTS_OT8', u'PTS_OT9', u'PTS_OT10', u'PTS', u'FG_PCT', u'FT_PCT', u'FG3_PCT', u'AST', u'REB', u'TOV']
[u'GAME_ID', u'HOME_TEAM_ID', u'VISITOR_TEAM_ID', u'GAME_DATE_EST', u'HOME_TEAM_WINS', u'HOME_TEAM_LOSSES', u'SERIES_LEADER']
[u'GAME_ID', u'LAST_GAME_ID', u'LAST_GAME_DATE_EST', u'LAST_GAME_HOME_TEAM_ID', u'LAST_GAME_HOME_TEAM_CITY', u'LAST_GAME_HOME_TEAM_NAME', u'LAST_GAME_HOME_TEAM_ABBREVIATION', u'LAST_GAME_HOME_TEAM_POINTS', u'LAST_GAME_VISITOR_TEAM_ID', u'LAST_GAME_VISITOR_TEAM_CITY', u'LAST_GAME_VISITOR_TEAM_NAME', u'LAST_GAME_VISITOR_TEAM_CITY1', u'LAST_GAME_VISITOR_TEAM_POINTS']
[u'TEAM_ID', u'LEAGUE_ID', u'SEASON_ID', u'STANDINGSDATE', u'CONFERENCE', u'TEAM', u'G', u'W', u'L', u'W_PCT', u'HOME_RECORD', u'ROAD_RECORD']
[u'TEAM_ID', u'LEAGUE_ID', u'SEASON_ID', u'STANDINGSDATE', u'CONFERENCE', u'TEAM', u'G', u'W', u'L', u'W_PCT', u'HOME_RECORD', u'ROAD_RECORD']
[u'GAME_ID', u'PT_AVAILABLE']
"""

# Sample Data
print sb_results[0]['rowSet']
"""
[[u'2018-03-10T00:00:00', 1, u'0021700987', 3, u'Final', u'20180310/PHXCHA', 1610612766, 1610612756, u'2017', 4, u'     ', None, u'Q4       - ', 1], [u'2018-03-10T00:00:00', 2, u'0021700988', 3, u'Final', u'20180310/WASMIA', 1610612748, 1610612764, u'2017', 4, u'     ', None, u'Q4       - ', 1], [u'2018-03-10T00:00:00', 3, u'0021700989', 3, u'Final', u'20180310/MEMDAL', 1610612742, 1610612763, u'2017', 4, u'     ', None, u'Q4       - ', 1], [u'2018-03-10T00:00:00', 4, u'0021700990', 3, u'Final', u'20180310/SASOKC', 1610612760, 1610612759, u'2017', 4, u'     ', u'ABC', u'Q4       - ABC', 1], [u'2018-03-10T00:00:00', 5, u'0021700991', 3, u'Final', u'20180310/ORLLAC', 1610612746, 1610612753, u'2017', 4, u'     ', None, u'Q4       - ', 1]]
"""

# Dump to DataFrame
dfDicts = {}
for result in sb_results:
	dfDicts[result['name']] = pd.DataFrame(data=result['rowSet'], columns=result['headers'])

for key, value in dfDicts.iteritems() :
	print key
"""
Available
EastConfStandingsByDay
LastMeeting
SeriesStandings
GameHeader
LineScore
WestConfStandingsByDay
"""

# Example DataFrame
print dfDicts['LineScore']
"""
         GAME_DATE_EST  GAME_SEQUENCE     GAME_ID     TEAM_ID  \
0  2018-03-10T00:00:00              1  0021700987  1610612756   
1  2018-03-10T00:00:00              1  0021700987  1610612766   
2  2018-03-10T00:00:00              2  0021700988  1610612764   
3  2018-03-10T00:00:00              2  0021700988  1610612748   
4  2018-03-10T00:00:00              3  0021700989  1610612763   
5  2018-03-10T00:00:00              3  0021700989  1610612742   
6  2018-03-10T00:00:00              4  0021700990  1610612759   
7  2018-03-10T00:00:00              4  0021700990  1610612760   
8  2018-03-10T00:00:00              5  0021700991  1610612753   
9  2018-03-10T00:00:00              5  0021700991  1610612746   

  TEAM_ABBREVIATION TEAM_CITY_NAME TEAM_WINS_LOSSES  PTS_QTR1  PTS_QTR2  \
0               PHX        Phoenix            19-49        25        26   
1               CHA      Charlotte            29-38        32        27   
2               WAS     Washington            38-29        20        28   
3               MIA          Miami            36-31        26        34   
4               MEM        Memphis            18-48        13        17   
5               DAL         Dallas            21-45        31        25   
6               SAS    San Antonio            37-29        19        24   
7               OKC  Oklahoma City            39-29        24        28   
8               ORL        Orlando            20-47        27        31   
9               LAC             LA            36-29        30        26   

   PTS_QTR3 ...   PTS_OT8  PTS_OT9  PTS_OT10  PTS  FG_PCT  FT_PCT  FG3_PCT  \
0        21 ...         0        0         0  115   0.506   0.684    0.563   
1        35 ...         0        0         0  122   0.506   0.778    0.406   
2        28 ...         0        0         0  102   0.442   0.794    0.350   
3        43 ...         0        0         0  129   0.591   0.714    0.357   
4        33 ...         0        0         0   80   0.357   0.765    0.389   
5        28 ...         0        0         0  114   0.481   0.857    0.345   
6        25 ...         0        0         0   94   0.465   0.571    0.500   
7        25 ...         0        0         0  104   0.459   0.667    0.357   
8        31 ...         0        0         0  105   0.452   0.778    0.333   
9        31 ...         0        0         0  113   0.526   0.857    0.389   

   AST  REB  TOV  
0   27   35   14  
1   24   41   12  
2   22   40   15  
3   27   42   10  
4   19   41   14  
5   21   52   10  
6   26   43   14  
7   24   49   15  
8   20   33   14  
9   17   41   15  
"""
