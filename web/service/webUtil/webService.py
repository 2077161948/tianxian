import json
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


class webService:

    def __init__(self):
        self.scheme = None
        self.link = []
        self.link_ed = []
        self.url_pattern = re.compile(r'(?:(?:http|https|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+|"?/?(?!/)(?:[^"\s]+/)*[^"\s]+"?')

    def web_download(self, url, is_all, search_type, is_imitate, js_code):
        scheme = urlparse(url)
        self.scheme = scheme
        pass

    def download_js_css_image(self, url_list):
        pass

    def get_page(self, url, is_imitate):
        if is_imitate is False:
            get = requests.get(url)
            if get.status_code == 200:
                text = get.text
                findall = re.findall(self.url_pattern, text)
                for item in findall:
                    if item not in self.link_ed and item not in self.link:
                        self.link.append(item)
                return text
        else:
            pass
        # 下面使用Selenium实现

    def is_html(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            return True
        except:
            return False

    def is_xml(self, text):
        try:
            ET.fromstring(text)
            return True
        except:
            return False

    def is_json(self,text):
        try:
            json.loads(text)
            return True
        except ValueError:
            return False
