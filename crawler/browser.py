import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class browser:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=chrome_options)
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()

    def __del__(self):
        self.browser.close()

    def get_result(self, url, plain=False):
        self.browser.get(url)
        text = self.browser.page_source
        if plain:
            text = re.sub("<.*?>", "", text)
        return text

    def get_real_url(self, url):
        self.browser.get(url)
        return self.browser.current_url