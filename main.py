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

def tweet_cases():
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

    to_tweet +=(f"Covid cases as of {str(date.today().strftime('%d %b, %Y'))} \n")
    to_tweet +=("New Cases : "+new_cases+'\n')
    to_tweet +=("New Deaths : "+new_deaths+'\n')
    to_tweet+=("Total Cases : "+total_cases+'\n')
    to_tweet+=('\n')
    to_tweet+=("#covid #StaySafeStayHome #StayHome #MoHFW")


    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    auth.secret = True
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    api.update_status(status =to_tweet)

def tweet_vaccine():
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    driver.get('https://www.pharmaceutical-technology.com/covid-19-vaccination-tracker/')

    total = driver.find_element_by_xpath('/html/body/main/div[1]/section[2]/div/div/div/div/div/article[2]/div/div/table/tbody/tr[3]/td[2]').text
    fully = driver.find_element_by_xpath('/html/body/main/div[1]/section[2]/div/div/div/div/div/article[2]/div/div/table/tbody/tr[3]/td[4]').text.strip()
    vaccines = driver.find_element_by_xpath('/html/body/main/div[1]/section[2]/div/div/div/div/div/article[2]/div/div/table/tbody/tr[3]/td[5]').text.strip()
    vaccine_txt = ''
    vaccine_txt +=(f"Vaccine data as of {str(date.today().strftime('%d %b, %Y'))} \n")
    vaccine_txt +=("Total doses administered :"+total+'\n')
    vaccine_txt +=("Fully vaccinated population :"+fully+'\n')
    vaccine_txt +=("Vaccines being used :"+vaccines+'\n')
    vaccine_txt +=("#vaccineIndia #StaySafeStayHome #StayHome #MoHFW ")
    
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    auth.secret = True
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    api.update_status(status =vaccine_txt)

def delhi_tweet():
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver.get('https://www.mygov.in/covid-19')
    soup = BeautifulSoup(driver.page_source)
    dom = etree.HTML(str(soup))
    total_C_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[2]/p')[0].text
    total_D_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[5]/p')[0].text

    new_C_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[2]/p/span')[0].text
    new_D_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[5]/p/span')[0].text

    death_R_D = dom.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[11]/div[2]/div/div/table/tbody/tr[7]/td[8]/p')[0].text


    delhi_det = ''
    delhi_det +=(f"#DELHI covid19 data till {str(date.today().strftime('%d %b, %Y'))}\n")
    delhi_det += ("Total cases :"+total_C_D+"\tNew cases :"+new_C_D+'\n')
    delhi_det += ("Total deaths :"+total_D_D+"\tNew deaths :"+new_D_D+'\n')
    delhi_det += ("Death Ratio :"+death_R_D )
    delhi_det +=("\n#covidDelhi #StaySafeStayHome #StayHome #MoHFW ")

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    auth.secret = True
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    api.update_status(status =delhi_det)







scheduler = BlockingScheduler()
scheduler.add_job(tweet_cases,'cron',month='5-7',day_of_week='mon-sun', hour='23',minute='40',timezone='Asia/Kolkata')
scheduler.add_job(tweet_vaccine,'cron',month='5-7',day_of_week='mon-sun', hour='00',minute='10',timezone='Asia/Kolkata')
scheduler.add_job(delhi_tweet,'cron',month='5-7',day_of_week='mon-sun', hour='21',minute='12',timezone='Asia/Kolkata')
scheduler.start()


