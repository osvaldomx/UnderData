# ⚽️ Understat 

[![License: MIT](https://img.shields.io/github/license/osvaldomx/underdata)](https://opensource.org/licenses/MIT)
![Python: 3.9](https://img.shields.io/badge/python-3.9-informational)
![PyPI](https://img.shields.io/pypi/v/understat)
[![PyPI Downloads](https://static.pepy.tech/badge/underdata)](https://pepy.tech/projects/underdata)

---
A clean, fast, and dependency-free Python client for football analytics data from [Understat](https://understat.com/).

Understat provides a simple, object-oriented interface to access detailed football statistics, including Expected Goals (xG), match results, and individual player performance. It processes the data into clean, ready-to-use Pandas DataFrames, making it perfect for data analysis, visualizations, and modeling. There are available 6 european leagues: **Premier League**, **La Liga**, **Bundesliga**, **Serie A**, **Ligue 1** and **Russian Premier League** from season 2014/2015.

---
### 🎯 Key Features 

* **League-Level Data**: Get full season standings, match schedules, and player stats for major leagues.
* **Team-Specific Analysis**: Access a team's complete match history and seasonal roster.
* **Detailed Player Statistics**: Retrieve game-by-game logs and individual shot data for any player.
* **Granular Match Data**: Pull shot maps, lineups, and key events from a single match.
* **Pandas Integration**: All data is delivered in structured and intuitive Pandas DataFrames.
* **Lightweight**: No browser or external driver dependencies required.

---

### 🔖 Note
This package is in development yet, then can change.
___

### 🚀 Installation
To install the package:
```sh
pip install underdata
```

or:
```sh
git clone git@github.com:osvaldomx/UnderData.git
cd understat
python setup.py install
```
---

### 🛫 Quick Start & Usage 

The library is designed to be intuitive. Here are a few examples to get you started.

| Object             | url                                                     |
| -------------------| ------------------------------------------------------- |
| underdata.league() | `https://www.understat.com/league/<league_name>/<year>` |
| underdata.team()   | `https://www.understat.com/team/<team_name>/<year>`     |
| underdata.player() | `https://www.understat.com/player/<player_id>`          |
| underdata.match()  | `https://www.understat.com/player/<match_id>`           |


#### 1. Get League Standings

Analyze an entire league's performance. The `get_teams()` method can provide a basic or advanced statistical table.
```python
from underdata.league import League

# Initialize the league for a specific season
la_liga = League(league_name="La_liga", season=2023)

# Get the advanced standings table
teams_df = la_liga.get_teams(advanced=True)

print("La Liga 2023/2024 Final Standings (Advanced Stats)")
print(teams_df.head())
```

#### 2. Analyze a Specific Team

Drill down into a single team's performance over a season.
```python
from underdata.team import Team

# Initialize a specific team
real_madrid = Team(team_name="Real Madrid", season=2023)

# Get the team's complete match history
match_history_df = real_madrid.get_match_history()

print("Real Madrid's Last 5 Matches of the Season:")
print(match_history_df.tail())
```

#### 3. Get Detailed Player Data

Analyze a single player's performance, including their shot data, perfect for creating shot maps.
```python
from soccermetrics.player import Player

# Initialize a player using their Understat ID (e.g., Jude Bellingham's ID is 8369)
bellingham = Player(player_id=8369)

# Get all shots from the 2023 season
bellingham_shots = bellingham.get_shot_data(season=2023)

print(f"Jude Bellingham took {len(bellingham_shots)} shots in the 2023/2024 season.")
print(bellingham_shots[['date', 'result', 'xG', 'shotType']].head())
```

#### 4. Analyze a Single Match

Get all the shot data and lineups from a specific match using its ID.
```python
from soccermetrics.match import Match

# Initialize a match using its Understat ID (e.g., a Real Madrid vs Barcelona match)
el_clasico = Match(match_id=21817)

# Get all shots from the match
shot_data = el_clasico.get_shot_data()

print(f"There were a total of {len(shot_data)} shots in the match.")
```
---
### ✅ Contributing

Contributions are welcome! If you'd like to help improve Underdata, please follow these steps:

1. Open an Issue: Before starting any work, please open an issue on GitHub to discuss the proposed change or feature. This helps ensure that your work aligns with the project's goals.

2. Fork the Repository: Fork the project to your own GitHub account.

3. Create a Feature Branch: Create a new branch for your changes (git checkout -b feat/YourAmazingFeature).

4. Develop: Make your changes and add tests to cover them.

5. Submit a Pull Request: Push your branch to your fork and open a pull request back to the main repository.
---
### License

This project is licensed under the MIT License - see the `LICENSE` file for details.

