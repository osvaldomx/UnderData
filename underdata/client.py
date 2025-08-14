# underdata/client.py

import re
import json
import codecs
from typing import Any, Dict, List
import requests
from bs4 import BeautifulSoup, Tag


class DataNotFoundError(Exception):
    """Lanzada cuando no se pueden encontrar los datos en el HTML."""
    pass

def get_data_from_html(url: str, data_variable: str) -> List[Dict[str, Any]]:
    """
    Obtiene el HTML de una URL y extrae una variable de datos específica.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Error al obtener la URL {url}: {e}") from e

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    scripts = soup.find_all("script")

    for script in scripts:
        if isinstance(script, Tag) and script.string and data_variable in script.string:
            # 1. Expresión regular para capturar el contenido de JSON.parse('...')
            match = re.search(
                rf"{re.escape(data_variable)}\s*=\s*JSON\.parse\('(.+?)'\)",
                script.string
            )

            if match:
                # 2. Extraer la cadena codificada
                encoded_string = match.group(1)
                
                # 3. Decodificar la cadena de escape a un string JSON normal
                decoded_string = codecs.decode(encoded_string, 'unicode_escape')
                
                try:
                    # 4. Parsear el string JSON ya limpio
                    data = json.loads(decoded_string)
                    
                    # Understat devuelve un diccionario, lo convertimos a una lista de sus valores
                    if isinstance(data, dict):
                        return list(data.values())
                    return data
                except json.JSONDecodeError as e:
                    raise DataNotFoundError(
                        f"Error al decodificar JSON para '{data_variable}'."
                    ) from e

    raise DataNotFoundError(
        f"No se pudo encontrar la variable '{data_variable}' en el script."
    )