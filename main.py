import requests
import time
from bs4 import BeautifulSoup
import os
import tweepy
from decouple import config
from datetime import date
from secrets import *
from apscheduler.schedulers.blocking import BlockingScheduler

def tweet():
    url= 'https://www.worldometers.info/coronavirus/country/india/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    new_cases = soup.find('li',class_='news_li').find_all('strong')[0].text[:7]
    new_deaths = soup.find('li',class_='news_li').find_all('strong')[1].text[:5]

    #print('New cases : '+ new_cases)
    #print('New deaths : '+ new_deaths)

    total_cases = soup.find('div',class_='maincounter-number').find_all('span')[0].text
    #total_deaths = soup.find('div',class_='maincounter-number').find_all('span')[3].text


    to_tweet = ''

    to_tweet +=(f"Covid cases as of {str(date.today())} \n")
    to_tweet +=("New Cases : "+new_cases+'\n')
    to_tweet +=("New Deaths : "+new_deaths+'\n')
    to_tweet+=("Total Cases : "+total_cases+'\n')
    to_tweet+=('\n')
    to_tweet+=("#covid #StaySafeStayHome #StayHome #MoHFW")


    consumer_key = config('C_key')
    consumer_secret = config('C_secret')
    access_token = config('A_key')
    access_token_secret = config('A_secret')

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    auth.secret = True
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    api.update_status(status =to_tweet)

scheduler = BlockingScheduler()
scheduler.add_job(tweet,'cron',month='5-7',day_of_week='mon-sun', hour='20',minute='32',timezone='Asia/Kolkata')
scheduler.start()


