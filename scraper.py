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

    def __init__(self, place = 'New Orleans', amount = 30):
        #Chrome driver setup
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Chrome(executable_path = '/Users/bhorowitz/Documents/chromedriver/chromedriver', options = options)

        #Login information - replace these later with username/password from tkinter
        self.username = 'hhorowitz734@gmail.com' 
        self.password = 'ThisBotScrapes151!'
        self.login_url = 'https://www.facebook.com'

        #Geolocator - Used to extract the zip code of a given location
        self.geolocator = Nominatim(user_agent='carsScraper')

        #Location for car listings
        self.location = place
        
        #Amount of car listings to scrape
        self.num_cars = amount

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
    
    def get_zip(self):
        '''Takes in a string containing a place, returns the zip code'''
        
        #Uses geopy to find location information
        #Location is converted to longitude and latitude in order to get an exact position
        location = self.geolocator.geocode(self.location)
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
        time.sleep(1.5)

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
    
    def get_car_links(self):
        '''Gets num_cars amount of links for cars on the main page'''

        #Important element names
        car_link_element = 'x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.x1lku1pv'
        car_scroll_element = 'x1lliihq.x6ikm8r.x10wlt62.x1n2onr6'

        #Records variables for scrolling script
        cars_collected = 0

        #Scrolls to the bottom of the page until the number of cars collected is greater than cars requested
        while cars_collected < self.num_cars:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 15);")
            #Waits for page to load
            time.sleep(3)
            cars_collected = (len(self.driver.find_elements(By.CLASS_NAME, car_scroll_element)) - 14) // 3

        #Creates a list of the href elements of every car on page (Links for the cars)
        links = [link.get_attribute('href') for link in self.driver.find_elements(By.CLASS_NAME, car_link_element)]

        #Returns list of links
        return links
    
    def get_car_info(self, links):
        '''Gets car information from the provided list of facebook marketplace links'''

        #Important element names
        see_more_element = 'x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x1n2onr6.x87ps6o.x1lku1pv.x1a2a7pz'
        title_element = 'x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xtoi2st.x41vudc.xngnso2.x1qb5hxa.x1xlr1w8.xzsf02u'
        price_element = 'x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x3x7a5m.x1lkfr7t.x1lbecb7.x1s688f.xzsf02u'
        miles_element = 'x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u'
        location_element = 'x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f'
        misc_element = 'x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u'
        description_element = 'xz9dl7a.x4uap5.xsag5q8.xkhd6sd.x126k92a'

        #Creates a list to save listings
        listings = []

        #Iterates over the list of links
        for link in links:

            #Creates a Listing object to store the car information
            listing = Listing()
            
            #Loads the link
            self.driver.get(link)

            #Clicks the see more button to expand car information if it exists
            actions = ActionChains(self.driver)
            see_more_buttons = self.driver.find_elements(By.CLASS_NAME, see_more_element)
            for button in see_more_buttons:
                if 'see more' in button.get_attribute('innerHTML').lower():
                    actions.move_to_element(button).click(button).perform()
            
            #Gets the title --> FIX THIS
            try:
                title = self.driver.find_elements(By.CLASS_NAME, title_element)[1]
                listing.title = title.get_attribute('innerText')
            except:
                print('Could not retrieve title')
            
            #Gets the price of the car --> FIX THIS
            try:
                price = self.driver.find_elements(By.CLASS_NAME, price_element)[2]
                listing.price = price.get_attribute('innerText')
            except:
                print('Could not retrieve price')
            
            
            #Gets the location of the car
            try:
                location = self.driver.find_element(By.CLASS_NAME, location_element)
                listing.location = location.get_attribute('innerText')
            except:
                print('Could not retrieve location')
            
            #Gets the car's miscellanious information
            misc_webelements = self.driver.find_elements(By.CLASS_NAME, misc_element)

            for element in reversed(misc_webelements):
                try:
                    info = element.get_attribute('innerText')
                except:
                    print('Information could not be retrieved.')
                    info = ''
                if 'transmission' in info and len(info.split(' ')) == 2:
                    listing.transmission = info.split(' ')[0]
                elif 'Exterior color: ' in info or 'Interior color: ' in info:
                    listing.colors = info
                elif 'Fuel type: ' in info:
                    listing.fueltype = info.split(': ')[1]
                elif 'MPG' in info:
                    listing.mpg = info
                elif 'Driven ' in info and 'miles' in info:
                    listing.miles = info
            
            #Gets the car's description
            try:
                description = self.driver.find_element(By.CLASS_NAME, description_element)
                listing.description = description.get_attribute('innerText')
            except:
                print('Could not get description')
            

            #Gets the car's first picture
            try:
                listing.image = self.driver.find_elements(By.TAG_NAME, 'img')[0].get_attribute('src')
            except:
                print('Picture could not be retrieved')
            

            #Adds the url to the listing information
            listing.url = link

            print('Title: ', listing.title)
            print('Price: ', listing.price)
            print('Miles: ', listing.miles)
            print('Location: ', listing.location)
            print('Transmission: ', listing.transmission)
            print('Colors', listing.colors)
            print('Fueltype: ', listing.fueltype)
            print('MPG: ', listing.mpg)
            print('Description: ', listing.description)
            print('Image link: ', listing.image)
            print('Link: ', listing.url)
            print('--------------------------')

            listings.append(listing)
        
        return listings
    
    #Converts list of items into dataframe
    def listings_to_csv(self, listings):
        '''Converts list of listings into a CSV file'''

        #Converts items into columns for dataframe
        titles = [listing.title for listing in listings]
        prices = [listing.price for listing in listings]
        miles = [listing.miles for listing in listings]
        locations = [listing.location for listing in listings]
        transmissions = [listing.transmission for listing in listings]
        colors = [listing.colors for listing in listings]
        fueltype = [listing.fueltype for listing in listings]
        mpgs = [listing.mpg for listing in listings]
        descriptions = [listing.description for listing in listings]
        images = [listing.image for listing in listings]
        urls = [listing.url for listing in listings]
        
        #Creates a dictionary representing the dataframe
        cars_data = {'title': titles, 'price': prices, 'mile': miles, 'location': locations, 'transmission': transmissions,
            'color': colors, 'fueltype': fueltype, 'mpg': mpgs, 'description': descriptions, 'image': images, 'url': urls}

        #Creates the cars data frame and turns it into a csv file
        cars_df = pd.DataFrame(cars_data)

        try:
            # Try to read the existing CSV file
            existing_df = pd.read_csv(f'{self.location}.csv')

            # Append the new data to the existing data
            cars_df = existing_df.append(cars_df, ignore_index=True)
            cars_df.to_csv(f'data/{self.location}.csv', index=False, mode='a')

        except FileNotFoundError:

            # If the file does not exist, create a new one
            cars_df.to_csv(f'data/{self.location}.csv', index=True, mode='w')
        
        #Adds the information to the general database
        cars_df.to_csv('data/cars_data.csv', index = False, mode = 'a')
    
    def run_all(self):
        '''Runs all functions in proper consecutive order for a full scrape'''

        self.login()
        self.input_location()
        self.input_search()
        links = self.get_car_links()
        listings = self.get_car_info(links)
        self.listings_to_csv(listings)
        self.quit()


class Listing():

    def __init__(self):
        self.title = None
        self.price = None
        self.miles = None
        self.location = None
        self.transmission = None
        self.colors = None
        self.fueltype = None
        self.mpg = []
        self.image = None
        self.description = None
        self.url = None