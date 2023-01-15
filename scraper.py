#Import modules

#Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


#Pandas
import pandas as pd

#Geopy
from geopy.geocoders import Nominatim

#Python Built-In Modules
import time



class Scraper():

    def __init__(self):
        #Chrome driver setup
        self.driver = webdriver.Chrome(executable_path = '/Users/bhorowitz/Documents/chromedriver/chromedriver')

        #Login information - replace these later with username/password from tkinter
        self.username = '' 
        self.password = ''
        self.login_url = 'https://www.facebook.com'

        #Geolocator - Used to extract the zip code of a given location
        self.geolocator = Nominatim(user_agent='carsScraper')

    def login(self):
        '''Logs the web scraping bot into facebook marketplace'''
        
        #Loads the facebook login link
        self.driver.get(self.login_url)

        #Scrapes username and password fields
        username_field = self.driver.find_elements(By.NAME, 'email')[0]
        password_field = self.driver.find_elements(By.NAME, 'pass')[0]
        
        #Populates username and password fields with username and password information provided
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        #Waits .5 seconds and then logs in
        time.sleep(.5)
        password_field.send_keys(Keys.ENTER)

    def quit(self):
        '''Closes the page and exits driver'''

        self.driver.close()
        self.driver.quit()
    
    def get_zip(self, place = 'New Orleans'):
        '''Takes in a string containing a place, returns the zip code'''
        
        #Uses geopy to find location information
        #Location is converted to longitude and latitude in order to get an exact position
        location = self.geolocator.geocode(place)
        location = self.geolocator.reverse(f'{location.latitude}, {location.longitude}')
        
        #Converts location to string format for split
        location = str(location)

        #Splits location string and returns component containing zip code
        return location.split(',')[-2]

    def input_location(self):
        '''Brings bot to facebook marketplace page for cars in the provided location'''

        #Saves names of important elements as variables
        location_btn_class = 'x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x1q0g3np.x87ps6o.x1lku1pv.x78zum5.x1a2a7pz.x1xmf6yo'
        location_input_class = 'x1i10hfl.xggy1nq.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w.x76ihet.xwmqs3e.x112ta8.xxxdfa6.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb.x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3.x15h3p50.x10emqs4'

        #Brings the driver to the facebook marketplace home if they are on a different page
        if 'https://www.facebook.com/marketplace/' not in str(self.driver.current_url):
            self.driver.get('https://www.facebook.com/marketplace/')
        
        #Closes an alert, if one pops up
        time.sleep(3) #Waits 3 seconds for an alert to pop up
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
        except:
            pass

        #Waits for the driver to load the location button
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, location_btn_class)))  

        #Clicks the element used to select locations
        location_btn = self.driver.find_element(By.CLASS_NAME, location_btn_class)
        actions = ActionChains(self.driver)
        actions.move_to_element(location_btn).click(location_btn).perform()
        
        #If element isn't open, clicks it again
        try:
            actions.move_to_element(location_btn).click(location_btn).perform()
        except:
            pass

        #The assumption now is that the scraper has opened the window for selecting a location.

        #Waits for the driver to load the location input
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, location_input_class)))

        #Clicks the input box for inputting a zip code
        location_input = self.driver.find_element(By.CLASS_NAME, location_input_class)
        actions.move_to_element(location_input).click(location_input).perform()

        #Deletes the information in the box and replaces it with new zip code given by user
        location_input.send_keys(Keys.DELETE) 
        location_input.send_keys(self.get_zip()) #Put place informaion into these parentheses (must be taken as a parameter to input_location)

x = Scraper()
x.login()
x.input_location()
time.sleep(3)
x.quit()