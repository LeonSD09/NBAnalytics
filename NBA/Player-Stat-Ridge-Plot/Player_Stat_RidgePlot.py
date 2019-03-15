from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import time

# Get LeBron James player ID
# https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/players.md
lbj_dict = players.find_players_by_full_name('LeBron James')
lbj_id = lbj_dict[0]['id']

# Using ID, get LeBron's game logs
# https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playergamelog.md

# Test on 2018-19
lbj_game_log_1819 = playergamelog.PlayerGameLog(player_id=lbj_id,
										   		season_all='2018-19',
										   		season_type_all_star='Regular Season')
lbj_game_log_1819_df = lbj_game_log_1819.get_data_frames()[0]
lbj_1819_pts_by_game = (lbj_game_log_1819_df.loc[:, ['GAME_DATE', 'PTS']]
											.sort_values('GAME_DATE'))
"""
lbj_1819_pts_by_game
       GAME_DATE  PTS
26  DEC 02, 2018   22
25  DEC 05, 2018   42
24  DEC 07, 2018   35
23  DEC 08, 2018   20
22  DEC 10, 2018   28
21  DEC 13, 2018   29
20  DEC 15, 2018   24
19  DEC 16, 2018   13
18  DEC 18, 2018   36
17  DEC 21, 2018   22
16  DEC 23, 2018   22
15  DEC 25, 2018   17
13  FEB 05, 2019   18
12  FEB 07, 2019   28
11  FEB 10, 2019   18
10  FEB 12, 2019   28
9   FEB 21, 2019   29
8   FEB 23, 2019   27
7   FEB 25, 2019   24
6   FEB 27, 2019   33
14  JAN 31, 2019   24
5   MAR 01, 2019   31
4   MAR 02, 2019   27
3   MAR 04, 2019   27
2   MAR 06, 2019   31
1   MAR 09, 2019   30
0   MAR 12, 2019   36
40  NOV 03, 2018   28
39  NOV 04, 2018   18
38  NOV 07, 2018   24
37  NOV 10, 2018   25
36  NOV 11, 2018   26
35  NOV 14, 2018   44
34  NOV 17, 2018   22
33  NOV 18, 2018   51
32  NOV 21, 2018   32
31  NOV 23, 2018   22
30  NOV 25, 2018   24
29  NOV 27, 2018   14
28  NOV 29, 2018   38
27  NOV 30, 2018   28
48  OCT 18, 2018   26
47  OCT 20, 2018   24
46  OCT 22, 2018   32
45  OCT 24, 2018   19
44  OCT 25, 2018   28
43  OCT 27, 2018   35
42  OCT 29, 2018   29
41  OCT 31, 2018   29
"""

def print_season(season):
    print(f'Retreiving data for {season} season - ', end="", flush=True)

# Pull for all seasons (since 2003-04)
# Create list of seasons
seasons = [f'{2000+i}-{i+1:02d}' for i in range(3,19,1)]
lbj_game_log_career = pd.DataFrame()
for season in seasons:
	print_season(season)
	season_logs = playergamelog.PlayerGameLog(player_id=lbj_id,
										   	  season_all=season,
										   	  season_type_all_star='Regular Season')
	season_logs_df = (season_logs.get_data_frames()[0]
		                         .loc[:, ['SEASON_ID', 'GAME_DATE', 'PTS']]
		                         .sort_values('GAME_DATE'))
	lbj_game_log_career = lbj_game_log_career.append(season_logs_df)
	print(f'Complete!')
	# Quick pause 
	time.sleep(5)

# Format the SEASON_ID
def format_season_id(val):
	season_start_yr = val[1:]
	season_end_yr_abbr = f"{(int(season_start_yr[2:]) + 1):02d}"
	return f'{season_start_yr}-{season_end_yr_abbr}'

# Add formatted SEASON_ID column, SEASON
lbj_game_log_career['SEASON'] = lbj_game_log_career.SEASON_ID.apply(format_season_id)

lbj_game_log_career.sample(10)
"""
   SEASON_ID     GAME_DATE  PTS   SEASON
8      22006  MAR 31, 2007   39  2006-07
3      22003  APR 09, 2004   24  2003-04
12     22010  MAR 18, 2011   43  2010-11
33     22013  JAN 29, 2014   34  2013-14
33     22009  JAN 19, 2010   28  2009-10
45     22005  JAN 14, 2006   46  2005-06
6      22010  MAR 30, 2011   35  2010-11
9      22006  MAR 28, 2007   24  2006-07
6      22004  APR 09, 2005   40  2004-05
29     22017  FEB 07, 2018   37  2017-18
"""	

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
# Initialize the FacetGrid object
pal = sns.cubehelix_palette(len(lbj_game_log_career.SEASON.unique()), rot=-.25, light=.7)
g = sns.FacetGrid(lbj_game_log_career, row="SEASON", hue="SEASON", aspect=15, height=.5, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "PTS", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
g.map(sns.kdeplot, "PTS", clip_on=False, color="w", lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "PTS")

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)

g.fig.suptitle('LeBron James, Point Distribution by Season',
			   x=.2, ha='left',
			   va='top',
			   weight='bold')
plt.show()

""" RESOURCES
https://seaborn.pydata.org/examples/kde_ridgeplot.html
https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/players.md
https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playergamelog.md
https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
https://stackoverflow.com/questions/5598181/python-multiple-prints-on-the-same-line
https://matplotlib.org/gallery/subplots_axes_and_figures/figure_title.html
https://matplotlib.org/api/_as_gen/matplotlib.pyplot.suptitle.html
http://www.eyalshafran.com/team_logos.html
https://stats.nba.com/media/img/teams/logos/season/2018-19/PHI_logo.svg
"""