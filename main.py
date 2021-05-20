import requests
import time
from bs4 import BeautifulSoup
import os
import tweepy
import os
import environ
from datetime import date
from secrets import *
environ.Env.read_env()

url= 'https://www.worldometers.info/coronavirus/country/india/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
new_cases = soup.find('li',class_='news_li').find_all('strong')[0].text[:7]
new_deaths = soup.find('li',class_='news_li').find_all('strong')[1].text[:5]

    #print('New cases : '+ new_cases)
    #print('New deaths : '+ new_deaths)

total_cases = soup.find('div',class_='maincounter-number').find_all('span')[0].text
    #total_deaths = soup.find('div',class_='maincounter-number').find_all('span')[3].text

filename = str(date.today())
    #print('Total cases : '+ total_cases)
f = open(f"{filename}.txt", "x")
f.write(f"Covid cases as of {str(date.today())} \n")
f.write("New Cases : "+new_cases+'\n')
f.write("New Deaths : "+new_deaths+'\n')
f.write("Total Cases : "+new_deaths)
f.write("\n")
f.write("#covid #StaySafeStayHome #StayHome #MoHFW")
f.close()

C_key =os.environ.get('C_key')
C_secret =os.environ.get('C_secret')
A_Key = os.environ.get('A_key')
A_secret = os.environ.get('A_secret')

auth = tweepy.OAuthHandler(C_key,C_secret)
auth.set_access_token(A_Key,A_secret)
auth.secret = True
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
filename=open(f"{filename}.txt",'r')
text=filename.read()
    # update the status
api.update_status(status =text)





