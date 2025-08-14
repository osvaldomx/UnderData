"""
Defines the Player class for obtaining detailed data for a single player.
"""

import pandas as pd
from typing import Dict, List, Any
from . import client


class Player:
    """
    Represents a player, providing access to their match history and shot data.

    The class is initialized with a player's unique Understat ID.
    """
    BASE_URL = "https://understat.com/player"

    def __init__(self, player_id: int):
        """
        Initializes the Player object and loads all their data.

        Args:
            player_id (int): The unique integer ID for the player on Understat.
        """
        self.player_id = player_id
        page_url = f"{self.BASE_URL}/{self.player_id}"

        # Fetch all relevant data sets from the player's page
        self._matches_data = client.get_data_from_html(page_url, "matchesData")
        self._shots_data = client.get_data_from_html(page_url, "shotsData")
        self._groups_data = client.get_data_from_html(page_url, "groupsData")

    def get_match_logs(self, season: int) -> pd.DataFrame:
        """
        Returns a DataFrame of all matches played in a specific season.

        Args:
            season (int): The starting year of the season (e.g., 2023).

        Returns:
            A DataFrame with stats for each match played in that season.
        """
        # Filter the raw data for the specified season
        season_matches = [
            match for match in self._matches_data if int(match['season']) == season
        ]
        if not season_matches:
            return pd.DataFrame()

        df = pd.DataFrame(season_matches)
        
        # Select, rename, and format important columns
        df['date'] = pd.to_datetime(df['date']).dt.date
        df = df.rename(columns={'time': 'minutes', 'h_team': 'home_team', 'a_team': 'away_team'})

        final_cols = [
            'date', 'home_team', 'away_team', 'goals', 'assists', 'shots',
            'key_passes', 'minutes', 'xG', 'xA', 'xGChain', 'xGBuildup'
        ]
        
        return df[final_cols].sort_values(by="date").reset_index(drop=True)

    def get_shot_data(self, season: int) -> pd.DataFrame:
        """
        Returns a DataFrame of all shots taken in a specific season.

        Args:
            season (int): The starting year of the season (e.g., 2023).

        Returns:
            A DataFrame where each row is a single shot.
        """
        # Filter the raw data for the specified season
        season_shots = [
            shot for shot in self._shots_data if int(shot['season']) == season
        ]
        if not season_shots:
            return pd.DataFrame()

        df = pd.DataFrame(season_shots)
        
        # Ensure key columns are numeric for analysis
        numeric_cols = ['X', 'Y', 'xG', 'shots', 'goals']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col])
            
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        return df.sort_values(by="date").reset_index(drop=True)