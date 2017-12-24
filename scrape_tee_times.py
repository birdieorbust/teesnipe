import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
from datetime import timedelta, date
from bs4 import BeautifulSoup
class TeeSnipe(object):


	def __init__(self):
		logging.debug("initializing webdriver")
		self.driver=webdriver.Firefox()
		self.base_url="https://www.brsgolf.com/studleywood/"


	def login(self):
		logging.debug("loggin in")
		login_path='https://www.brsgolf.com/studleywood/member/login'
		self.driver.get(login_path)
		login_form=self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/table/tbody/tr/td/blockquote/table/tbody/tr[3]/td/form')
		user_name=self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/table/tbody/tr/td/blockquote/table/tbody/tr[3]/td/form/table/tbody/tr[2]/td[2]/input')
		password=self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/table/tbody/tr/td/blockquote/table/tbody/tr[3]/td/form/table/tbody/tr[3]/td[2]/input')
		user_name.send_keys('')
		password.send_keys('')
		#submit form
		self.driver.find_element_by_xpath('//*[@id="header"]/div[2]/table/tbody/tr/td/blockquote/table/tbody/tr[3]/td/form/table/tbody/tr[4]/td/input').click()

	def scrape_tee_times(self):
		logging.debug("SCRAPING TEE TIMES")
		#self.driver.get(self.base_url+'members_booking.php?operation=member_day&d_date=2017-12-28&course_id1=1')
		def daterange(start_date, end_date):
			for n in range(int ((end_date - start_date).days)):
				yield start_date + timedelta(n)

		start_date = date(2017,12,25)
		end_date = date(2017, 12, 26)

		for single_date in daterange(start_date, end_date):
			date_string=single_date.strftime("%Y-%m-%d")
			logging.debug("Scraping"+date_string)
			self.driver.get(self.base_url+'members_booking.php?operation=member_day&d_date='+date_string+'&course_id1=1')
			table=pd.read_html(self.driver.find_element_by_css_selector('.table_white_text').get_attribute('outerHTML'),header=1)
			#table['Date']=pd.to_datetime(single_date)
			print(table)
			


	def quit(self):
		self.driver.quit()

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	teesnipe=TeeSnipe()
	teesnipe.login()
	teesnipe.scrape_tee_times()
	teesnipe.quit()