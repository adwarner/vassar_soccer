# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas as pd 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import Select 

from bs4 import BeautifulSoup, SoupStrainer

os.chdir("C:\\Users\\adwar\\Documents\\vassar_soccer")


class VC_Athletics():
    
    def __init__(self):
        
        self.driver = webdriver.Chrome("chromedriver")
        
    def launch_website(self):
        
        self.driver.get("https://www.vassarathletics.com/schedule.aspx?path=msoc")
        
    def get_links(self):
        
        links = []
        html = BeautifulSoup(self.driver.page_source)
        
        for link in html.find_all('a', href=True):
            links.append(link['href'])
        
        links = [i for i in links if str(i).find("boxscore") == 0]
        return(links)
        

x = VC_Athletics()
x.launch_website()
links = x.get_links()


pd.read_html()

class get_html(self, links):
    
    def __init__(self)
    