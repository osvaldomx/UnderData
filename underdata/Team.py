# underdata/team.py

import pandas as pd
from typing import Dict, List
from . import client

class Team:
    """
    Representa un equipo y una temporada, proporcionando acceso
    a su historial de partidos y a los datos de su plantilla.
    """
    BASE_URL = "https://understat.com/team"

    def __init__(self, team_name: str, season: int):
        """
        Inicializa el objeto Team y carga los datos.

        Args:
            team_name (str): El nombre del equipo (ej. 'Real Madrid').
            season (int): El año de inicio de la temporada (ej. 2023).
        """
        # Reemplaza espacios por guiones bajos para la URL
        formatted_name = team_name.replace(' ', '_')
        page_url = f"{self.BASE_URL}/{formatted_name}/{season}"

        # Obtenemos los dos conjuntos de datos de la página del equipo
        self._match_history_data = client.get_data_from_html(page_url, "datesData")
        self._statistics_data = client.get_data_from_html(page_url, "statisticssData")
        self._players_data = client.get_data_from_html(page_url, "playersData")

    def get_match_history(self) -> pd.DataFrame:
        """
        Devuelve un DataFrame con el historial completo de partidos de la temporada.
        """
        if not self._match_history_data:
            return pd.DataFrame()

        # Creamos el DataFrame a partir de los datos de partidos
        df = pd.json_normalize(self._match_history_data)

        # Seleccionamos y renombramos las columnas más importantes
        rename_map = {
            "date": "Fecha",
            "h.title": "Local",
            "a.title": "Visitante",
            "goals.h": "Goles Local",
            "goals.a": "Goles Visitante",
            "xG.h": "xG Local",
            "xG.a": "xG Visitante",
            "result": "Resultado"
        }
        
        df = df[rename_map.keys()].rename(columns=rename_map)
        df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.date

        return df.sort_values(by="Fecha").reset_index(drop=True)

    def get_statistics(self) -> pd.DataFrame:
        # To Do
        return pd.DataFrame()

    def get_roster(self, advanced: bool = False) -> pd.DataFrame:
        """
        Devuelve un DataFrame con la plantilla del equipo y sus estadísticas.

        Args:
            advanced (bool, optional): Si es True, incluye métricas avanzadas.
                                       Defaults to False.
        """
        if not self._players_data:
            return pd.DataFrame()

        # Creamos el DataFrame y nos aseguramos de que las columnas sean numéricas
        players_df = pd.DataFrame(self._players_data)
        numeric_cols = ['time', 'goals', 'xG', 'assists', 'xA', 'shots']
        for col in numeric_cols:
            players_df[col] = pd.to_numeric(players_df[col])

        # Definimos las columnas para la vista básica y avanzada
        default_cols = [
            'player', 'position', 'apps', 'time', 'goals', 'assists', 'shots'
        ]
        advanced_cols = default_cols + [
            'xG', 'xA', 'key_passes', 'yellow_cards', 'red_cards', 'npg',
            'npxG', 'xGChain', 'xGBuildup'
        ]

        final_cols = advanced_cols if advanced else default_cols

        return (
            players_df[final_cols]
            .sort_values(by='time', ascending=False)
            .reset_index(drop=True)
        )