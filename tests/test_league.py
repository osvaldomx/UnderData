import pandas as pd
from ..underdata.league import League

def test_get_la_liga_standings():
    """
    Tests the main functionality of the League class by fetching and
    validating the standings for a specific season.
    """
    # ARRANGE: Preparamos los datos necesarios para la prueba
    league_name = "La_liga"
    season = 2023 # Usamos una temporada pasada para que los datos no cambien

    # ACT: Ejecutamos la acción que queremos probar
    la_liga = League(league_name=league_name, season=season)
    standings_df = la_liga.get_teams()

    # ASSERT: Verificamos que los resultados son los correctos
    assert isinstance(standings_df, pd.DataFrame), "El resultado debe ser un DataFrame de Pandas"
    
    assert len(standings_df) == 20, "La Liga debe tener 20 equipos"
    
    expected_columns = ['title', 'M', 'W', 'D', 'L', 'G', 'GA', 'PTS']
    assert all(col in standings_df.columns for col in expected_columns), "Faltan columnas esenciales en la tabla"
    
    # Verificamos un dato conocido: el ganador de esa temporada
    winner = standings_df.iloc[0]
    assert winner['title'] == 'Real Madrid', "El primer lugar de la tabla no es el esperado"
    assert winner['PTS'] == 95, "Los puntos del primer lugar no coinciden"