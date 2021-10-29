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
from underdata.League import League

league = League(league="epl", year="2018")
league.get_info()
```
this will open a browser with geckodriver with the purpose of get general information of the league `EPL` in year `2018`. To access to the information, run:

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
```

## Contributing