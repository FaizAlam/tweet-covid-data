from types import new_class
import requests
import time
from bs4 import BeautifulSoup
import os
import tweepy
from decouple import config
from datetime import date
from secrets import *
from apscheduler.schedulers.blocking import BlockingScheduler
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from lxml import etree

consumer_key = config('C_key')
consumer_secret = config('C_secret')
access_token = config('A_key')
access_token_secret = config('A_secret')


options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
driver.get('https://www.mygov.in/covid-19')
soup = BeautifulSoup(driver.page_source)
dom = etree.HTML(str(soup))

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



def tweet_cases():
    total_C_I = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[7]/div[4]/div[2]/div/span')[0].text
    new_C_I = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[7]/div[4]/div[2]/div/div[2]/div')[0].text.strip()

    total_D_I = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[7]/div[4]/div[5]/div/span')[0].text
    new_D_I = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[7]/div[4]/div[5]/div/div[2]/div')[0].text.strip()

    to_tweet = ''

    to_tweet +=(f"Covid cases as of {str(date.today().strftime('%d %b, %Y'))} \n")
    to_tweet +=("\n")
    to_tweet +=("New Cases : "+new_C_I+', Total Cases : '+ total_C_I+'\n')
    #to_tweet+=("Total Cases : "+ total_C_I+'\n')
    to_tweet +=("New Deaths : "+new_D_I+', Total Deaths : '+ total_D_I+'\n')
    #to_tweet+=("Total Deaths : "+ total_D_I+'\n')
    to_tweet+=('\n')
    to_tweet+=("#covid #StaySafeStayHome #StayHome #MoHFW")


    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    auth.secret = True
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    api.update_status(status =to_tweet)

    to_tweet=''

def tweet_vaccine():
    
    total_V_I = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[7]/div[2]/div[2]/div[1]/strong')[0].text
    new_V_I = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[7]/div[2]/div[2]/div[2]/strong')[0].text
    
    vaccine_txt = ''
    vaccine_txt +=(f"Vaccine data as of {str(date.today().strftime('%d %b, %Y'))} \n")
    vaccine_txt += ("\n")
    vaccine_txt +=("Total doses administered :"+ total_V_I+'\n')
    vaccine_txt +=("vaccine administered today :"+ new_V_I+'\n')
    vaccine_txt +=("Vaccines being used : Covishield, Covaxin\n")
    vaccine_txt +=('\n')
    vaccine_txt +=("#vaccineIndia #StaySafeStayHome #StayHome #MoHFW #covaxin #covishield")
    
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    auth.secret = True
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    api.update_status(status =vaccine_txt)
    vaccine_txt=''

def delhi_tweet():
    
    total_C_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[2]/p')[0].text
    total_D_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[5]/p')[0].text
    new_C_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[2]/p/span')[0].text
    new_D_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[5]/p/span')[0].text
    death_R_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[8]/p')[0].text


    delhi_det = ''
    delhi_det +=(f"#DELHI covid19 data till {str(date.today().strftime('%d %b, %Y'))}\n")
    delhi_det += ("\n")
    delhi_det += ("Total cases :"+total_C_D+",  New cases :"+ new_C_D+'\n')
    delhi_det += ("Total deaths :"+total_D_D+",  New deaths :"+ new_D_D+'\n')
    delhi_det += ("Death Ratio :"+death_R_D )
    delhi_det += ("\n")
    delhi_det +=("\n#covidDelhi #StaySafeStayHome #StayHome #MoHFW #delhicorona")

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    auth.secret = True
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    api.update_status(status =delhi_det)

    delhi_det=''







scheduler = BlockingScheduler()
scheduler.add_job(tweet_cases,'cron',month='5-7',day_of_week='mon-sun', hour='11',minute='30',timezone='Asia/Kolkata')
scheduler.add_job(tweet_vaccine,'cron',month='5-7',day_of_week='mon-sun', hour='11',minute='40',timezone='Asia/Kolkata')
scheduler.add_job(delhi_tweet,'cron',month='5-7',day_of_week='mon-sun', hour='11',minute='50',timezone='Asia/Kolkata')
scheduler.start()


