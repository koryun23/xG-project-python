import math
import time
import urllib.request

from bs4 import BeautifulSoup
import requests
import httpx
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from json_to_csv_converter import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class WhoScoredParser:
    def get_data_bs(self, url):
        r = requests.get(url, params={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        })
        print(r.status_code)
    def get_data_selenium(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        all_scripts = driver.find_elements("script")
        print(len(all_scripts))
        for script in all_scripts:
            if 'require.config.params["args"] = {' in script.text:
                print(script)

parser = WhoScoredParser()
parser.get_data_bs("https://www.whoscored.com/")