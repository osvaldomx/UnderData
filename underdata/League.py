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

    def get_players(self, advanced: bool = False) -> pd.DataFrame:
        """
        Returns a DataFrame with player stats for the season.

        Args:
            advanced (bool, optional): If True, includes advanced metrics like
                                       xGChain and xGBuildup. Defaults to False.
        """
        if not self._players_data:
            return pd.DataFrame()

        # Step 1: Create the full DataFrame from the raw data
        players_df = pd.DataFrame(self._players_data)

        # Ensure key stat columns are numeric for sorting
        numeric_cols = ['games', 'time', 'goals', 'xG', 'assists', 'xA', 'shots']

        for col in numeric_cols:
            players_df[col] = pd.to_numeric(players_df[col])

        # Calculate derived metrics
        players_df['xG90'] = players_df['xG'] / (players_df['time'] / 90)
        players_df['xA90'] = players_df['xA'] / (players_df['time'] / 90)
        
        # Step 2: Define the default and advanced column sets
        default_cols = [
            'id', 'player_name', 'team_title', 'position', 'games', 'time',
            'goals', 'assists', 'shots', 'xG', 'xA', 'xG90', 'xA90'
        ]

        advanced_cols = [
            'player_name', 'team_title', 'position', 'games', 'time',
            'goals', 'xG', 'assists', 'xA', 'shots', 'key_passes',
            'yellow_cards', 'red_cards', 'npg', 'npxG', 'xG90', 
            'xA90', 'xGChain', 'xGBuildup'
        ]

        # Step 3: Choose columns based on the 'advanced' parameter
        if advanced:
            final_cols = advanced_cols
        else:
            final_cols = default_cols
        
        # Step 4: Return the filtered and sorted DataFrame
        final_table = (
            players_df[final_cols]
            .sort_values(by='goals', ascending=False)
            .reset_index(drop=True)
        )
        
        return final_table
    
    def get_matches(self, matchday: int | None = None) -> pd.DataFrame:
        """
        Devuelve un DataFrame con los partidos de la temporada, 
        agrupados por fecha.

        Args:
            matchday (int, optional): Filtra los partidos por una
                                      jornada específica.
                                      Defaults a None (todos los partidos).
        """
        if not self._teams_data:
            return pd.DataFrame()

        # Aplanamos los datos para tener una fila por partido y por equipo
        per_match_df = pd.json_normalize(
            self._teams_data,
            record_path=['history'],
            meta=['id', 'title']
        )
        per_match_df['date'] = pd.to_datetime(per_match_df['date'])

        # Separamos los partidos de local y visitante
        home_games = per_match_df[per_match_df['h_a'] == 'h']
        away_games = per_match_df[per_match_df['h_a'] == 'a']

        # Unimos los datos para tener una fila por partido
        matches_df = pd.merge(
            home_games,
            away_games,
            on='date',
            suffixes=('_home', '_away')
        )

        # Filtramos por jornada si el usuario lo solicita
        if matchday:
            # Asumimos que la jornada se puede deducir del número de partidos jugados
            # Esto puede necesitar un ajuste si hay jornadas dobles o aplazadas
            matches_df = matches_df.iloc[(matchday-1)*10 : matchday*10]

        # Seleccionamos y renombramos las columnas para el resultado final
        matches_df = matches_df[[
            'date', 'title_home', 'scored_home', 'scored_away', 'title_away'
        ]].rename(columns={
            'date': 'Fecha',
            'title_home': 'Local',
            'scored_home': 'Goles Local',
            'scored_away': 'Goles Visitante',
            'title_away': 'Visitante'
        })

        return matches_df.sort_values(by='Fecha').reset_index(drop=True)

        