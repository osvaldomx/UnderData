# underdata
Python package for get data of [www.understat.com](www.understat.com). There are available 6 european leagues: **Premier League**, **La Liga**, **Bundesliga**, **Serie A**, **Ligue 1** and **Russian Premier League** from season 2014/2015.

___
### Note
This package is in development yet, then can change.
___

## Installation
To install the package:
~~~sh
git clone git@github.com:osvaldomx/UnderData.git
cp ~/understat /<your_project>
~~~
This package use `selenium` therefore you will have to install [geckodriver](https://github.com/mozilla/geckodriver/releases).

## Getting started

| Object | url |
| ------ | --- |
| understat.League() | `https://www.understat.com/league/<league_name>/<year>` |
| understat.Team() | `https://www.understat.com/team/<team_name>/<year>` |

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

>>> league.table                    # Get the current qualification table or correspondant to the specific year
     N                     Team   M   W   D   L   G  GA  PTS          xG          xGA         xPTS
0    1          Manchester City  38  32   2   4  95  23   98  93.72-1.28   25.73+2.73   90.64-7.36
1    2                Liverpool  38  30   7   1  89  22   97  79.46-9.54   29.15+7.15  83.45-13.55
.
.
.

>>> league.table_goals              # Get top-10 of scorers
    N                     Player             Team  Apps   Min   G   A          xG          xA  xG90  xA90
0   1  Pierre-Emerick Aubameyang          Arsenal    36  2740  22   5  23.55+1.55   4.99-0.01  0.77  0.16
1   2                 Sadio Mané        Liverpool    36  3100  22   1  16.76-5.24   5.12+4.12  0.49  0.15
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
    week          date                     home                     away  goals_home  goals_away  xG_home  xG_away result                               url
0      1  Aug 12, 2018                liverpool                 West Ham           4           0     4.34     0.40    win  https://understat.com/match/9205
1      2  Aug 20, 2018           Crystal Palace                liverpool           0           2     0.37     2.82    win  https://understat.com/match/9216
.
.
.

>>> team.player_stats              # Get info of all team players in specific year
      Id                   Player  Pos  Apps   Min   G   A  Sh90  KP90          xG          xA  xG90  xA90
0    838               Sadio Mané  F M    36  3100  22   1  2.53  1.31  16.76-5.24   5.12+4.12  0.49  0.15
1   1250            Mohamed Salah    F    38  3274  22   8  3.77  1.87  21.79-0.21  10.47+2.47  0.60  0.29
.
.
.
```

## Contributing