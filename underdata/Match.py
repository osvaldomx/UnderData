# underdata/match.py

"""
Define la clase Match para obtener datos detallados de un único partido.
"""

import pandas as pd
from typing import Dict, Any
from . import client


class Match:
    """
    Representa un único partido, proporcionando acceso a los datos
    de los tiros, alineaciones e información general.
    """
    BASE_URL = "https://understat.com/match"

    def __init__(self, match_id: int):
        """
        Inicializa el objeto Match y carga sus datos.

        Args:
            match_id (int): El ID único del partido en Understat.
        """
        self.match_id = match_id
        page_url = f"{self.BASE_URL}/{self.match_id}"

        # Extraemos los tres conjuntos de datos de la página del partido
        self._shots_data = client.get_data_from_html(page_url, "shotsData")
        self._rosters_data = client.get_data_from_html(page_url, "rostersData")
        self._match_data = client.get_data_from_html(page_url, "matchData")

    def get_shot_data(self) -> pd.DataFrame:
        """
        Devuelve un DataFrame donde cada fila es un tiro del partido.

        Ideal para crear mapas de tiros (shot maps).
        """
        if not self._shots_data:
            return pd.DataFrame()

        df = pd.DataFrame(self._shots_data)
        
        # Nos aseguramos de que las columnas importantes sean numéricas
        numeric_cols = ['X', 'Y', 'xG']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col])
            
        df['date'] = pd.to_datetime(df['date']).dt.date

        return df

    def get_rosters(self) -> Dict[str, pd.DataFrame]:
        """
        Devuelve las alineaciones de ambos equipos.

        Returns:
            Un diccionario con dos claves, 'home' y 'away', cada una
            conteniendo un DataFrame con los jugadores de ese equipo.
        """
        home_roster = pd.DataFrame(self._rosters_data.get('h', []))
        away_roster = pd.DataFrame(self._rosters_data.get('a', []))
        
        return {"home": home_roster, "away": away_roster}

    def get_match_info(self) -> Dict[str, Any]:
        """
        Devuelve un diccionario con información general del partido.
        """
        return self._match_data