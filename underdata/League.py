"""
UnderData v0.1
"""
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

from . import LEAGUES

class League():
    """ Class League

    Attributes
    ----------
    URL_BASE : str
        Url base for query leagues.
    league : str
        League to get info.
    seasons : list
        List of seasons availables.
    curr_week : dict
        Dictionary with current matches
    table : Pandas DataFrame
        DataFrame with current qualification table
    table_goals : Pandas DataFrame
    	DataFrame with current top-10 scored players
    """

    URL_BASE = "https://www.understat.com/league/"
    league = None
    year = ""
    seasons = []
    table = None
    table_goals = None


    def __init__(self, league='epl', year=""):
        self.league = LEAGUES[league]
        self.year = year

    def set_seasons(self, driver):
        """Function to set seasons availables

        Parameters
        ----------
        driver : Webdriver Object
            Object for make querys to url.
        """
        list_options = driver.find_elements(By.CLASS_NAME, "custom-select-options")
        options = list_options[1].find_elements(By.CSS_SELECTOR, "li")
        list_seasons = []

        for opt in options:
            list_seasons.append(opt.get_attribute('rel'))

        if list_seasons:
            self.seasons = list_seasons

    def set_table(self, driver):
        """Function to set curretn qualification table

        Parameters
        ----------
        driver : Webdriver Object
            Object for make querys to url.
        """
        table = {}
        thead = driver.find_elements(By.XPATH, "//div[@id='league-chemp']/table/thead/tr/th")
        table['N'] = []

        for idx in range(1, len(thead)):
            table[thead[idx].text] = []

        tbody = driver.find_elements(By.XPATH, "//div[@id='league-chemp']/table/tbody/tr/td")

        for idx in range(0, len(tbody), 12):
            table['N'].append(int(tbody[idx].text))
            table['Team'].append(tbody[idx+1].text)
            table['M'].append(int(tbody[idx+2].text))
            table['W'].append(int(tbody[idx+3].text))
            table['D'].append(int(tbody[idx+4].text))
            table['L'].append(int(tbody[idx+5].text))
            table['G'].append(int(tbody[idx+6].text))
            table['GA'].append(int(tbody[idx+7].text))
            table['PTS'].append(int(tbody[idx+8].text))
            table['xG'].append(tbody[idx+9].text)
            table['xGA'].append(tbody[idx+10].text)
            table['xPTS'].append(tbody[idx+11].text)

        if table:
            df_table = pd.DataFrame(table)
            self.table = df_table

    def set_score_players(self, driver):
        """Function to set current top-10 scored players

        Parameters
        ----------
        driver : Webdriver Object
            Object for make querys to url.
        """
        table = {}
        thead = driver.find_elements(By.XPATH, "//div[@id='league-players']/table/thead/tr/th")
        table['N'] = []

        for idx in range(1, len(thead)):
            table[thead[idx].text] = []

        tbody = driver.find_elements(By.XPATH, "//div[@id='league-players']/table/tbody/tr/td")

        for idx in range(0, len(tbody), 11):
            table['N'].append(int(tbody[idx].text))
            table['Player'].append(tbody[idx+1].text)
            table['Team'].append(tbody[idx+2].text)
            table['Apps'].append(int(tbody[idx+3].text))
            table['Min'].append(int(tbody[idx+4].text))
            table['G'].append(int(tbody[idx+5].text))
            table['A'].append(int(tbody[idx+6].text))
            table['xG'].append(tbody[idx+7].text)
            table['xA'].append(tbody[idx+8].text)
            table['xG90'].append(float(tbody[idx+9].text))
            table['xA90'].append(float(tbody[idx+10].text))
            if int(tbody[idx].text) == 10:
                break

        if table:
            df_table = pd.DataFrame(table)
            self.table_goals = df_table

    def get_info(self):
        """Function to get general information of a league.

        Raises
        ------
        exc : Exception
            Exception if something was wrong

        Returns
        -------
        str : str
            Success string
        """
        try:
            driver = webdriver.Firefox()
            driver.get(self.URL_BASE + self.league + "/" + self.year)
            self.set_seasons(driver)
            self.set_table(driver)
            self.set_score_players(driver)
        except Exception as exc:
            raise exc
        finally:
            driver.quit()

        return "Get info of " + self.league
