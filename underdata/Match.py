"""
UnderData v0.1
"""
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

class Match():
    """Class Match
    """
    URL_BASE = "https://www.understat.com/match/"
    match_id = None
    team_home = None
    team_away = None
    match_score = None
    goals_home = None
    goals_away = None
    match_stats = None

    def __init__(self, match_id="") -> None:
        self.match_id = match_id

    def _set_match(self, driver) -> None:
        self.team_home = driver.find_elements(By.CSS_SELECTOR, ".block-match-result a")[0].text
        self.team_away = driver.find_elements(By.CSS_SELECTOR, ".block-match-result a")[1].text
        score = driver.find_element(By.CSS_SELECTOR, ".block-match-result").text
        score = score.replace(self.team_home, "").replace(self.team_away, "").strip()
        self.match_score = score
        self.goals_home = int(score.split("-")[0])
        self.goals_away = int(score.split("-")[1])

    def _set_match_stats(self, driver) -> None:
        table = {}
        thead = driver.find_elements(By.CSS_SELECTOR, "#match-rosters table thead tr th")

        for idx in range(1, len(thead)):
            table[thead[idx].text] = []

        for _ in range(0,2):
            tbody = driver.find_elements(By.CSS_SELECTOR, "#match-rosters table tbody tr td")

            for idx in range(1, len(tbody), 10):
                if tbody[idx-1].text:
                    table[list(table.keys())[0]].append(tbody[idx].text)
                    table[list(table.keys())[1]].append(tbody[idx+1].text)
                    table[list(table.keys())[2]].append(int(tbody[idx+2].text))
                    table[list(table.keys())[3]].append(int(tbody[idx+3].text))
                    table[list(table.keys())[4]].append(int(tbody[idx+4].text))
                    table[list(table.keys())[5]].append(int(tbody[idx+5].text))
                    table[list(table.keys())[6]].append(int(tbody[idx+6].text))
                    table[list(table.keys())[7]].append(tbody[idx+7].text)
                    table[list(table.keys())[8]].append(tbody[idx+8].text)

            element = driver.find_element(By.CSS_SELECTOR,
                                            ".filters .filter label[for='team-away']")
            element.click()

        self.match_stats = pd.DataFrame(table)

    def get_info(self) -> None:
        """

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
            driver.get(self.URL_BASE + self.match_id)
            self._set_match(driver)
            self._set_match_stats(driver)
        except Exception as exc:
            raise exc
        finally:
            driver.quit()

        return "Get info of " + self.team_home + " vs " + self.team_away
