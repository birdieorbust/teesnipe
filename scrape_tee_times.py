import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
import configparser
import yaml
import numpy as np
from utility_functions.utilities import clean_table
from flask import Flask
from flask import request


class TeeSnipe(object):


	def __init__(self):
		logging.debug("initializing webdriver")
		with open("config.yml", 'r') as ymlfile:
			cfg = yaml.load(ymlfile)
		self.base_url=cfg['golf_club_details']['base_url']
		self.user=cfg['golf_club_details']['user']
		self.passw=cfg['golf_club_details']['pass']


	def login(self):
		self.driver=webdriver.Firefox()
		logging.debug("loggin in")
		login_path='https://www.brsgolf.com/studleywood/member/login'
		self.driver.get(login_path)
		login_form=self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/table/tbody/tr/td/blockquote/table/tbody/tr[3]/td/form')
		user_name=self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/table/tbody/tr/td/blockquote/table/tbody/tr[3]/td/form/table/tbody/tr[2]/td[2]/input')
		password=self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/table/tbody/tr/td/blockquote/table/tbody/tr[3]/td/form/table/tbody/tr[3]/td[2]/input')
		user_name.send_keys(self.user)
		password.send_keys(self.passw)
		#submit form
		self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/table/tbody/tr/td/blockquote/table/tbody/tr[3]/td/form/table/tbody/tr[4]/td/input').click()


	def scrape_tee_times(self,st,en):
		logging.debug("SCRAPING TEE TIMES")
		#self.driver.get(self.base_url+'members_booking.php?operation=member_day&d_date=2017-12-28&course_id1=1')
		def daterange(start_date, end_date):
			for n in range(int ((end_date - start_date).days)):
				yield start_date + timedelta(n)

		start_date = datetime.strptime(st,'%Y-%m-%d')
		end_date = datetime.strptime(en,'%Y-%m-%d')

		appended_data=[]
		for single_date in daterange(start_date, end_date):
			date_string=single_date.strftime("%Y-%m-%d")
			logging.debug("Scraping"+date_string)
			try:
				self.driver.get(self.base_url+'/members_booking.php?operation=member_day&d_date='+date_string+'&course_id1=1')
				temp_table=pd.read_html(self.driver.find_element_by_css_selector('.table_white_text').get_attribute('outerHTML'),header=0)
				temp_table=pd.concat(temp_table)
				temp_table['date']=date_string
				appended_data.append(temp_table)
			except TimeoutException as ex:
				logging.debug("DATE PASSED NOT FOUND MOVING ONTO NEXT DATE")
				pass
			except NoSuchElementException as ex:
				logging.debug("ELEMENT NOT FOUND ON PAGE CONTINUE TO NEXT DATE")
				pass


		appended_data=pd.concat(appended_data)
		appended_data=clean_table(appended_data)
		appended_data.to_csv("data/test_table.csv")
		return appended_data

	def maximum_bookable_date(self):
		dataframe=pd.read_csv("data/test_table.csv")
		dataframe['Live']=np.where(dataframe.Book.str.contains("Not Live Yet",na=False),1,0)
		max_index=dataframe.Live[dataframe.Live==1].index[0]
		max_date=dataframe.loc[max_index-2].date
		return max_date

			


	def quit(self):
		self.driver.quit()

logging.basicConfig(level=logging.DEBUG)
	
app=Flask(__name__)

@app.route('/scrape')
def scrape():
	start_date=request.args.get('start_date')
	end_date=request.args.get('end_date')
	teesnipe=TeeSnipe()
	teesnipe.login()
	teesnipe.scrape_tee_times(start_date,end_date)
	teesnipe.quit()
	return "Scraped Tee Times on Server and saved to CSV"

@app.route('/maximum_bookable_date')
def maximum_bookable_date():
	teesnipe=TeeSnipe()
	date=teesnipe.maximum_bookable_date()
	return date

@app.route('/do_something')
def do_something():
	return "HELLO WORLD FROM SAMS TEESNIPE APP"

if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True)