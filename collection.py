#Imports modules

#Imports pandas
import pandas as pd

#Imports scraping functionality
from scraper import Scraper

#Imports multithreading
from concurrent.futures import ThreadPoolExecutor

#Class for running all scrapers
class ScrapeManager():
    
    def __init__(self, amount):
        '''Initalizes the scraping manager'''
        
        #Reads cities from a cities file
        with open('cities.txt', 'r') as f:
            self.cities = f.read().splitlines()
        
        #Saves the amount of cars to be scraped per city
        self.amount = amount
        
    def run_scraping(self):
        '''Runs the scraping for all cities'''

        self.scrapers = [Scraper(city, self.amount) for city in self.cities]
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(self.run_scraper, scraper) for scraper in self.scrapers]
    
            # Wait for all threads to complete
            for future in futures:
                if future.exception() is not None:
                    print(f"Error in {future.result().location}: {future.exception()}")
                    future.result().exit()
    
    def run_scraper(self, scraper):
        '''Runs the scraper for a city'''
        
        print(f'Running scraper in {scraper.location}')

        try:
            scraper.run_all()
        except Exception as e:
            #print(f"Error in {scraper.location}: {e}")
            print(f'Error in {scraper.location}')
    
x = ScrapeManager(20)
x.run_scraping()
