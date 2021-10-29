"""
UnderData v0.1
"""
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

class Team():
    """Class Team

    Attributes
    ----------

    """
    URL_BASE = "https://www.understat.com/team/"
    team = None
    year = None
    weeks = 0
    games = {}
    player_stats = {}


    def __init__(self, team="Liverpool", year=""):
        self.team = team
        self.year = year

    def set_games(self, driver):
        """Function to set results of the last games

        Parameters
        ----------
        driver : Webdriver Object
            Driver to manage querys to browser
        """
        table = {
            'week': [],
            'date': [],
            'home': [],
            'away': [],
            'goals_home': [],
            'goals_away': [],
            'xG_home': [],
            'xG_away': [],
            'result': [],
            'url': []
        }
        games = driver.find_elements(By.CLASS_NAME, "calendar-date-container")
        self.weeks = len(games)
        cont = 1
        for game in games:
            date = game.find_element(By.CSS_SELECTOR, ".calendar-date").text
            side = game.find_element(By.CSS_SELECTOR, ".calendar-date").get_attribute("data-side")
            res = game.find_element(By.CSS_SELECTOR, ".calendar-date").get_attribute("data-result")

            table['week'].append(cont)
            table['date'].append(date)

            if side == 'h':
                table['home'].append(self.team)
                table['away'].append(game.find_element(By.CSS_SELECTOR, ".team-title").text)
            else:
                table['away'].append(self.team)
                table['home'].append(game.find_element(By.CSS_SELECTOR, ".team-title").text)

            try:
                goals_home = int(game.find_element(By.CSS_SELECTOR, ".team-home").text)
                goals_away = int(game.find_element(By.CSS_SELECTOR, ".team-away").text)
            except Exception:
                goals_home = None
                goals_away = None

            table['goals_home'].append(goals_home)
            table['goals_away'].append(goals_away)

            try:
                xg_home = float(game.find_element(By.CSS_SELECTOR,
                                                    "div.teams-xG > span.team-home").text)
                xg_away = float(game.find_element(By.CSS_SELECTOR,
                                                    "div.teams-xG > span.team-away").text)
            except Exception:
                xg_home = None
                xg_away = None

            table['xG_home'].append(xg_home)
            table['xG_away'].append(xg_away)

            if res == 'w':
                table['result'].append('win')
            elif res == 'd':
                table['result'].append('draw')
            elif res == 'l':
                table['result'].append('loss')
            else:
                table['result'].append(game.find_element(By.CSS_SELECTOR, ".match-time").text)

            try:
                url = game.find_element(By.CSS_SELECTOR, "a.match-info").get_attribute("href")
            except Exception:
                url = None

            table['url'].append(url)

            cont += 1

        self.games = pd.DataFrame(table)

    def set_player_stats(self, driver):
        """Function to set player stats

        Parameters
        ----------
        driver : Webdriver Object
            Driver to manage querys to browser.
        """
        table = {}
        thead = driver.find_elements(By.CSS_SELECTOR, "#team-players > table > thead > tr > th")
        table['Id'] = []

        for idx in range(1, len(thead)):
            table[thead[idx].text] = []

        tbody = driver.find_elements(By.CSS_SELECTOR, "#team-players > table > tbody > tr > td")

        for idx in range(0, len(tbody), 13):
            if tbody[idx].text:
                table['Id'].append(int(tbody[idx+1].find_element(By.CSS_SELECTOR,
                                    "#team-players > table > tbody > tr > td.player-title > a").\
                                    get_attribute("href").split("/")[-1]))
                table['Player'].append(tbody[idx+1].text)
                table['Pos'].append(tbody[idx+2].text)
                table['Apps'].append(int(tbody[idx+3].text))
                table['Min'].append(int(tbody[idx+4].text))
                table['G'].append(int(tbody[idx+5].text))
                table['A'].append(int(tbody[idx+6].text))
                table['Sh90'].append(float(tbody[idx+7].text))
                table['KP90'].append(float(tbody[idx+8].text))
                table['xG'].append(tbody[idx+9].text)
                table['xA'].append(tbody[idx+10].text)
                table['xG90'].append(float(tbody[idx+11].text))
                table['xA90'].append(float(tbody[idx+12].text))
            else:
                break

        self.player_stats = pd.DataFrame(table)

    def get_info(self):
        """Function to get general info of the team

        Raises
        ------
        exc : Exception
            Exception if something was wrong.

        Returns
        -------
        str : str
            Success string.
        """
        try:
            driver = webdriver.Firefox()
            driver.get(self.URL_BASE + self.team + "/" + self.year)
            self.set_games(driver)
            self.set_player_stats(driver)
        except Exception as exc:
            raise exc
        finally:
            driver.quit()

        return "Get info of " + self.team
