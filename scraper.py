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

        #Important element names
        location_btn_class = 'x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x1q0g3np.x87ps6o.x1lku1pv.x78zum5.x1a2a7pz.x1xmf6yo'
        location_input_class = 'x1i10hfl.xggy1nq.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w.x76ihet.xwmqs3e.x112ta8.xxxdfa6.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb.x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3.x15h3p50.x10emqs4'
        first_choice_class = 'x9f619.x1n2onr6.x1ja2u2z.x78zum5.x1r8uery.x1iyjqo2.xs83m0k.xeuugli.x1qughib.x6s0dn4.xozqiw3.x1q0g3np.xykv574.xbmpl8g.x4cne27.xifccgj'
        apply_button_class = 'x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.xl56j7k.x6s0dn4.xozqiw3.x1q0g3np.xi112ho.x17zwfj4.x585lrc.x1403ito.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.xn6708d.x1ye3gou.xtvsq51.x1r1pt67'

        #Brings the driver to the facebook marketplace home if it is on a different page
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
        
        #Waits for the driver to load the first result
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, first_choice_class)))

        #Selects the first result from the result list
        first_result = self.driver.find_element(By.CLASS_NAME, first_choice_class)
        actions.move_to_element(first_result).click(first_result).perform()

        #Clicks the apply button
        apply_button = self.driver.find_element(By.CLASS_NAME, apply_button_class)
        actions.move_to_element(apply_button).click(apply_button).perform()
    
    def input_search(self, search = 'cars'):
        '''Inputs the desired seach terms and searches'''

        #Important element names
        search_bar_class = 'x1i10hfl.xggy1nq.x1s07b3s.x1kdt53j.x1yc453h.xhb22t3.xb5gni.xcj1dhv.x2s2ed0.xq33zhf.xjyslct.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.xnwf7zb.x40j3uw.x1s7lred.x15gyhx8.x9f619.xzsf02u.xdl72j9.x1iyjqo2.xs83m0k.xjb2p0i.x6prxxf.xeuugli.x1a2a7pz.x1n2onr6.x15h3p50.xm7lytj.xsyo7zv.xdvlbce.x16hj40l.xc9qbxq.xo6swyp.x1ad04t7.x1glnyev.x1ix68h3.x19gujb8'

        #Brings the driver to the facebook marketplace home if it is on a different page
        if 'https://www.facebook.com/marketplace/' not in str(self.driver.current_url):
            self.driver.get('https://www.facebook.com/marketplace/')
        
        #Selects the search bar
        search_bar = self.driver.find_element(By.CLASS_NAME, search_bar_class)
        actions = ActionChains(self.driver)
        actions.move_to_element(search_bar).click(search_bar).perform()

        #Enters the search into the search bar
        search_bar.send_keys(Keys.DELETE) 
        search_bar.send_keys(search)
        search_bar.send_keys(Keys.ENTER)


        

x = Scraper()
x.login()
x.input_location()
x.input_search()
time.sleep(3)
x.quit()