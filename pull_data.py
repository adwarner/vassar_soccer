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

from bs4 import BeautifulSoup 
import re 
import numpy as np 

os.chdir("C:\\Users\\adwar\\Documents\\vassar_soccer")


class VC_Athletics():
    
    def __init__(self):
        
        self.driver = webdriver.Chrome("chromedriver")
        
    def launch_website(self):
        self.driver.get('https://www.vassarathletics.com/schedule.aspx?path=msoc')
        
    def get_links(self):
        
        links = []
        html = BeautifulSoup(self.driver.page_source)
        
        for link in html.find_all('a', href=True):
            links.append(link['href'])
        
        links = [i for i in links if str(i).find("boxscore") == 0]
        return(links)
        
    def quit(self):
        self.driver.quit()
    
class game_data():
    
    def __init__(self, links):
        self.links = links
        self.driver = webdriver.Chrome("chromedriver")

    
    def get_data(self):
        
        links = ['https://www.vassarathletics.com/' + i for i in self.links]
        df = pd.DataFrame()
        j = 0 
        
        for i in links: 
            if j ==0: 
                self.driver.get(i)
                dates_html = self.driver.find_element_by_id('box-score')
                box_score = dates_html.get_attribute('innerHTML')
                game_date = re.search(r'(\d+/\d+/\d+)',box_score)[1]
                
                elem = self.driver.find_element_by_id('play-by-play-period-1')
                elem2 = self.driver.find_element_by_id('play-by-play-period-2')
    
                first_half = pd.read_html(elem.get_attribute('innerHTML'))[0]
                second_half = pd.read_html(elem2.get_attribute('innerHTML'))[0]
                df = pd.concat([first_half, second_half], axis = 0)
                df = df[[i for i in df.columns if i.find('VC') >= 0 or i == 'Clock' or i.find('VAS') >= 0]]
                df['Date'] = game_date
                df.columns = ['Clock', 'VCMS - Play Description', 'Date']
                j += 1
                
            else: 
                df1 = pd.DataFrame()
                
                self.driver.get(i)
                
                dates_html = self.driver.find_element_by_id('box-score')
                box_score = dates_html.get_attribute('innerHTML')
                game_date = re.search(r'(\d+/\d+/\d+)',box_score)[1]
                
                elem = self.driver.find_element_by_id('play-by-play-period-1')
                elem2 = self.driver.find_element_by_id('play-by-play-period-2')
    
                first_half = pd.read_html(elem.get_attribute('innerHTML'))[0]
                second_half = pd.read_html(elem2.get_attribute('innerHTML'))[0]
                df1 = pd.concat([first_half, second_half], axis = 0)
            
                df1 = df1[[i for i in df1.columns if i.find('VC') >= 0 or i == 'Clock' or i.find('VAS') >= 0]]
                df1['Date'] = game_date

                df1.columns = ['Clock', 'VCMS - Play Description', 'Date']

                df = pd.concat([df, df1], axis = 0)
                j += 1
            
        return(df)
    
    def quit(self):
        self.driver.quit()

vassar_athletics = VC_Athletics()
vassar_athletics.launch_website()
gameday_links = vassar_athletics.get_links()
vassar_athletics.quit()
         
games = game_data(gameday_links)
game_day_data = games.get_data() 
game_day_data.index = range(0, len(game_day_data))
games.quit()

            

def subsets(df, word):
    search_idx = []
    
    for idx, val in enumerate(df['VCMS - Play Description']):
        try:
            if re.search(word, val).group() == word:
                search_idx.append(idx)
                
        except: 
            pass
    subset = df.iloc[search_idx]
    subset['Clock'] = [int(i.split(":")[0]) + 1 for i in subset['Clock']]

    return(subset)
    

class starters(): 
    
    def __init__(self, links):
        self.links = links
        self.driver = webdriver.Chrome("chromedriver")
        
    def get_starters(self):
        links = ['https://www.vassarathletics.com/' + i for i in self.links]
        
        #df = pd.DataFrame()
        
        for idx, val in enumerate(links):
            self.driver.get(val)
            
            starters = self.driver.find_element_by_id('individual-stats')
            side = self.driver.find_element_by_class_name('box-score-header')
            side = pd.read_html(side.get_attribute('innerHTML'))[0]
            try: 
                vassar_index = [idx for idx, val in enumerate(side['Team']) if val.strip().lower().find('vas') >= 0][0]
            except: 
                vassar_index = [idx for idx, val in enumerate(side['Team']) if val.strip().lower().find('vcms') >= 0][0]

            if vassar_index == 1: 
                vassar_index = 2
            else: 
                pass
            starters = starters.get_attribute('innerHTML')
            
            
            if idx == 0: 
                df = pd.read_html(starters)[vassar_index]
            else: 
                df1 = pd.read_html(starters)[vassar_index]
                df = pd.concat([df, df1])
        return(df, vassar_index)
    
    def quit(self):
        self.driver.quit()
        
starters_test = starters(gameday_links)     
starters_df = starters_test.get_starters()[0]
starters_df['subset_index'] = starters_df.index 
starters_test.quit()

starters_df_test = starters_df[starters_df['subset_index'] <= 12]

## We need to clean out the player name ### 

regex = re.compile('[^a-zA-Z ]')
starters_df_test['Player'] = [regex.sub('', str(i)) for i in starters_df_test['Player']]
starters_df_test['Player'] = starters_df_test['Player'].apply(lambda x: x.strip())

def clean_player_name(df):
    try: 
        return df['Player'].split('  ')[0]
    except:
        return df['Player']
    
starters_df_test['Player'] = starters_df_test.apply(clean_player_name, axis = 1)

starters_df_test.reset_index(inplace = True)
starters_df_test = starters_df_test.drop(['index'], axis = 1)

starters_df_test  = starters_df_test[starters_df_test['Player'] != 'nan']       
starters_df_test['Date'] = list(np.repeat(list(df['Date'].unique()), 11)) 
starters_df_test = starters_df_test[['Player', 'Date']]   
starters_df_test['Clock'] = '00:00'


df = game_day_data[pd.notnull(game_day_data['VCMS - Play Description'])]


goals = subsets(df, 'GOAL')

subs = subsets(df, 'substitution')
into = []
out = []
for idx, val in enumerate(subs['VCMS - Play Description']):
    
    sub_stats = (val.split(':')[1].strip('.').strip().split('for'))
    into.append(sub_stats[0])
    out.append(sub_stats[1])

subs['Sub In'] = into
subs['Sub Out'] = out


#subs.to_csv('subs.csv', index = False)    
   