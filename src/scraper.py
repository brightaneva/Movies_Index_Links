import requests
import json
import time
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class Series_Spider:

    def __init__(self,title, season):
        self.original_title = title.title()
        self.season = season
        self.title = title.replace(" ", "+")

        # create a headless browser while blocking img nd scripts
        options = Options()
        options.headless = True
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        prefs = {"profile.managed_default_content_settings.images": 0}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--ignore-certificate-errors')
        #browser path
        s = Service('../chromedriver.exe')
        self.driver = webdriver.Chrome(
           service=s, options=options)

        self.header = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"
        }

    # Create a request interceptor
    def interceptor(self,request):
        del request.headers['Referer']  # Delete the header first
        request.headers['Referer'] = 'some_referer'

    # Set the interceptor on the driver

        # self.driver._client.set_header_overrides(headers=dict_headers)
    def get_response(self,link):
        self.driver.request_interceptor = self.interceptor
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        return soup

    # def search_results_list(self):
    #     page = self.get_response()
    #     result = []
    #     for show in page.find_all("li","ui-li-has-thumb"):
    #         show_wrapper = show.find("a")
    #         if show_wrapper.find("h3").text.strip() == self.original_title:
    #             data = {
    #                 "name" : show_wrapper.find("h3").text.strip(),
    #                 "link" : show_wrapper.get("href")
    #             }
    #             result.append(data)
    #         else:
    #             print("results not found")
    #     return result

    def get_series_page(self):
        """get series page link"""
        url = f'https://o2tvseries.co/search/?q={self.title}'
        page = self.get_response(url)
        series_page = [show.find("a").get("href") for show in page.find_all("li","ui-li-has-thumb") if show.find("h3").text.strip() == self.original_title]
        self.driver.quit()
        return series_page

    def get_series_season_page(self):
        """get series page link"""
        url =  f"https://o2tvseries.co{self.get_series_page()}"
        page = self.get_response(url)
        episodes_page = [show.find("a").get("href") for show in page.find_all("li","ui-li-has-count") if show.find("h3").text.strip() == self.season]
        self.driver.quit()
        return episodes_page

def main():
    print(Series_Spider("silicon valley","Season 06").get_series_season_page())

if __name__ == "__main__":
    # Start the stopwatch / counter
    # t1_start = time.perf_counter()
    main()
    # # Stop the stopwatch / counter
    # t1_stop = time.perf_counter()

    # print("Elapsed time:", t1_stop, t1_start)


    # print("Elapsed time during the whole program in seconds:",
    #                                     t1_stop-t1_start)
