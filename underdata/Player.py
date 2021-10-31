"""
UnderData v0.1
"""
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

class Player():
    """Class Player
    """
    URL_BASE = "https://www.understat.com/player/"
    player_id = None
    player_name = None
    table_seasons = {}
    player_history = {}

    def __init__(self, player_id="2097") -> None:
        self.player_id = player_id

    def _set_player_name(self, driver) -> None:
        self.player_name = driver.find_element(By.CSS_SELECTOR, "#header").text

    def _set_table_seasons(self, driver) -> None:
        table = {}
        thead = driver.find_elements(By.CSS_SELECTOR, "#player-groups > table > thead > tr > th")

        for idx in range(1, len(thead)):
            table[thead[idx].text] = []

        tbody = driver.find_elements(By.CSS_SELECTOR, "#player-groups > table > tbody > tr > td")

        for idx in range(1, len(tbody)-13, 13):
            table[list(table.keys())[0]].append(tbody[idx].text)
            table[list(table.keys())[1]].append(tbody[idx+1].text)
            table[list(table.keys())[2]].append(int(tbody[idx+2].text))
            table[list(table.keys())[3]].append(int(tbody[idx+3].text))
            table[list(table.keys())[4]].append(int(tbody[idx+4].text))
            table[list(table.keys())[5]].append(int(tbody[idx+5].text))
            table[list(table.keys())[6]].append(float(tbody[idx+6].text))
            table[list(table.keys())[7]].append(float(tbody[idx+7].text))
            table[list(table.keys())[8]].append(tbody[idx+8].text)
            table[list(table.keys())[9]].append(tbody[idx+9].text)
            table[list(table.keys())[10]].append(float(tbody[idx+10].text))
            table[list(table.keys())[11]].append(float(tbody[idx+11].text))

        self.table_seasons = pd.DataFrame(table)

    def _set_player_history(self, driver) -> None:
        table = {}
        thead = driver.find_elements(By.CSS_SELECTOR, "#player-history > table > thead > tr > th")

        for idx in range(1, len(thead)):
            table[thead[idx].text] = []

        pages = int(driver.find_elements(By.CSS_SELECTOR, ".pagination li")[-1].text)

        for page in range(2, pages+2):
            tbody = driver.find_elements(By.CSS_SELECTOR,
                                            "#player-history > table > tbody > tr > td")
            for idx in range(1, len(tbody), 13):
                if tbody[idx-1].text:
                    table[list(table.keys())[0]].append(tbody[idx].text)
                    table[list(table.keys())[1]].append(tbody[idx+1].text)
                    table[list(table.keys())[2]].append(tbody[idx+2].text)
                    table[list(table.keys())[3]].append(tbody[idx+3].text)
                    table[list(table.keys())[4]].append(tbody[idx+4].text)
                    table[list(table.keys())[5]].append(tbody[idx+5].text)
                    table[list(table.keys())[6]].append(tbody[idx+6].text)
                    table[list(table.keys())[7]].append(tbody[idx+7].text)
                    table[list(table.keys())[8]].append(tbody[idx+8].text)
                    table[list(table.keys())[9]].append(tbody[idx+9].text)
                    table[list(table.keys())[10]].append(tbody[idx+10].text)
                    table[list(table.keys())[11]].append(tbody[idx+11].text)

            if page != pages+1:
                element = driver.find_element(By.CSS_SELECTOR, ".page[data-page='"+str(page)+"']")
                element.click()
                print("click in page "+str(page), end="\r")

        self.player_history = pd.DataFrame(table)

    def get_info(self) -> str:
        """Function to get general information of specific player

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
            driver.get(self.URL_BASE + self.player_id)
            self._set_player_name(driver)
            self._set_table_seasons(driver)
            self._set_player_history(driver)
        except Exception as exc:
            raise exc
        finally:
            driver.quit()

        return "Get info of " + self.player_name
