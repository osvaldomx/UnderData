[![License: MIT](https://img.shields.io/github/license/osvaldomx/underdata)](https://opensource.org/licenses/MIT)
![Python: 3.9](https://img.shields.io/badge/python-3.9-informational)
![PyPI](https://img.shields.io/pypi/v/understat)
![Selenium: 4.0](https://img.shields.io/badge/selenium-4.0.0-informational)


# underdata
Python package for get data of [www.understat.com](www.understat.com). There are available 6 european leagues: **Premier League**, **La Liga**, **Bundesliga**, **Serie A**, **Ligue 1** and **Russian Premier League** from season 2014/2015.

___
### Note
This package is in development yet, then can change.
___

## Installation
To install the package:
~~~sh
pip install underdata
~~~

or:
~~~sh
git clone git@github.com:osvaldomx/UnderData.git
cd understat
python setup.py install
~~~
This package use `selenium` therefore you will have to install [geckodriver](https://github.com/mozilla/geckodriver/releases).

## Getting started

| Object             | url                                                     |
| -------------------| ------------------------------------------------------- |
| underdata.League() | `https://www.understat.com/league/<league_name>/<year>` |
| underdata.Team()   | `https://www.understat.com/team/<team_name>/<year>`     |
| underdata.Player() | `https://www.understat.com/player/<player_id>`          |
| underdata.Match()  | `https://www.understat.com/player/<match_id>`           |

### Examples

#### League

To get general information of a league:

```python
# import
>>> from underdata.League import League
>>> league = League(league="epl", year="2018")
>>> league.get_info()
'Get info of EPL'
```
this will open a browser with `geckodriver` with the purpose of get general information of the league `EPL` in the year `2018`. To access to the information, run:

```python
>>> league.seasons                  # Get seasons availables in www.understats.com
['2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014']

>>> league.table                    # Get the current qualification table for specific year
     N                 Team   M   W   D   L   G  GA  PTS          xG          xGA         xPTS
0    1      Manchester City  38  32   2   4  95  23   98  93.72-1.28   25.73+2.73   90.64-7.36
1    2            Liverpool  38  30   7   1  89  22   97  79.46-9.54   29.15+7.15  83.45-13.55
.
.
.

>>> league.table_goals              # Get top-10 of scorers
    N              Player         Team  Apps   Min   G   A          xG          xA  xG90  xA90
0   1          Aubameyang      Arsenal    36  2740  22   5  23.55+1.55   4.99-0.01  0.77  0.16
1   2          Sadio Mané    Liverpool    36  3100  22   1  16.76-5.24   5.12+4.12  0.49  0.15
.
.
.
```

#### Team

To get general information of a league:

```python
# import
>>> from underdata.Team import Team
>>> team = Team(team="liverpool", year="2018")
>>> Team.get_info()
'Get info of Liverpool'
```
this will open a browser with `geckodriver` with the purpose of get general information of the team `Liverpool` in the year `2018`. To access to the information, run:

```python
>>> team.games                      # Get info of games of team in specific year
    week          date                  home             away  goals_home  goals_away  xG_home
0      1  Aug 12, 2018             liverpool         West Ham           4           0     4.34
1      2  Aug 20, 2018        Crystal Palace        liverpool           0           2     0.37
.
.
.

>>> team.player_stats              # Get info of all team players in specific year
      Id           Player  Pos  Apps   Min   G   A  Sh90  KP90          xG          xA  xG90
0    838       Sadio Mané  F M    36  3100  22   1  2.53  1.31  16.76-5.24   5.12+4.12  0.49
1   1250    Mohamed Salah    F    38  3274  22   8  3.77  1.87  21.79-0.21  10.47+2.47  0.60
.
.
.
```

#### Player

To get general information of a player:

```python
# import
>>> from underdata.Player import Player
>>> player = Player(player_id="1250")
>>> player.get_info()
'Get info of Mohamed Salah'
```
this will open a browser with `geckodriver` with the purpose of get general information of the player with id `1250`. To access to the information, run:

```python
>>> player.table_seasons                    # Get info of seasons of the player
      Season        Team  Apps   Min   G   A  Sh90  KP90          xG          xA  xG90  xA90
0  2021/2022   Liverpool     9   810  10   5  4.44  2.33   7.50-2.50   3.14-1.86  0.83  0.35
1  2020/2021   Liverpool    37  3085  22   5  3.68  1.60  20.25-1.75   6.53+1.53  0.59  0.19
.
.
.

>>> player.player_history                   # Get info of all appears of the player
         Date               Home Score         Away  Pos Min Sh  G KP  A         xG         xA
0  2021-10-24  Manchester United   0-5    Liverpool  FWR  90  7  3  2  1  2.25-0.75  0.51-0.49
1  2021-10-16            Watford   0-5    Liverpool  FWR  90  5  1  2  1  0.40-0.60  0.36-0.64
.
.
.
```

#### Match

To get general information of a Match:

```python
# import
>>> from underdata.Match import Match
>>> match = Match(match_id="16463")
>>> match.get_info()
'Get info of Manchester United vs Liverpool'
```
this will open a browser with `geckodriver` with the purpose of get general information of the match with id `16463`. To access to the information, run:
```python
>>> match.match_stats                    # Get stats of the match
                     Player  Pos  Min  Sh  G  KP  A         xG         xA
0              David de Gea   GK   90   0  0   0  0       0.00       0.00
1         Aaron Wan-Bissaka   DR   90   0  0   0  0       0.00       0.00
2           Victor Lindelöf   DC   90   0  0   0  0       0.00       0.00
...
25               Sadio Mané  Sub    8   1  0   0  0  0.11+0.11       0.00
26  Alex Oxlade-Chamberlain  Sub   21   1  0   1  0  0.02+0.02  0.04+0.04
27             Curtis Jones  Sub   64   1  0   1  0  0.15+0.15  0.03+0.03

```

## Contributing