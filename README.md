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

## Contributing