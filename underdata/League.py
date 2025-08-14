# underdata/league.py

import pandas as pd
from typing import Dict, List
from . import client

class League:
    """
    Representa una liga y temporada, proporcionando acceso a sus datos.
    """
    BASE_URL = "https://understat.com/league"

    def __init__(self, league_name: str, season: int):
        self.league_name = league_name
        self.season = season
        
        page_url = f"{self.BASE_URL}/{self.league_name}/{self.season}"

        # Los datos se cargan inmediatamente al crear el objeto.
        self._teams_data = client.get_data_from_html(page_url, "teamsData")
        self._players_data = client.get_data_from_html(page_url, "playersData")

    def get_teams(self, advanced: bool = False) -> pd.DataFrame:
        """Devuelve un DataFrame de pandas con los datos de los equipos."""
        if not self._teams_data:
            return pd.DataFrame()
        
        # Step 1: Flatten the per-match data from the 'history' key
        teams_df = pd.json_normalize(
            self._teams_data,
            record_path=['history'],
            meta=['id', 'title']
        )

        # Ensure all stat columns are numeric for calculation
        numeric_cols = [
            'wins', 'draws', 'loses', 'scored', 'missed', 'pts',
            'xG', 'xGA', 'npxG', 'npxGA', 'xpts'
        ]
        
        for col in numeric_cols:
            teams_df[col] = pd.to_numeric(teams_df[col])

        # Step 2: Group by team and aggregate the stats for the season
        league_table = teams_df.groupby(['id', 'title']).sum(numeric_only=True)

        # Step 3: Calculate derived metrics
        league_table['M'] = league_table['wins'] + league_table['draws'] + league_table['loses']

        # Step 4: Rename columns for final presentation
        rename_map = {
            'wins': 'W', 'draws': 'D', 'loses': 'L',
            'scored': 'G', 'missed': 'GA', 'pts': 'PTS'
        }
        league_table = league_table.rename(columns=rename_map)
        
        # Step 5: Define column order, sort by points, and reset index
        final_col_order = [
            'M', 'W', 'D', 'L', 'G', 'GA', 'PTS', 'xG',
            'xGA', 'xpts'
        ]

        advanced_metrics = ['npxG', 'npxGA', 'npxGD', 'ppda.att', 'ppda.def', 
                            'ppda_allowed.att', 'ppda_allowed.def']
        
        if advanced:
            final_col_order += advanced_metrics
        
        final_table = (
            league_table[final_col_order]
            .sort_values(by='PTS', ascending=False)
            .reset_index()
        )
        
        return final_table

    @property
    def get_players(self) -> pd.DataFrame:
        """Devuelve un DataFrame de pandas con los datos de los jugadores."""
        return pd.DataFrame(self._players_data)