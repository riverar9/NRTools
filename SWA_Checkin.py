#%%
import time
from selenium import webdriver
#from pyutils import get_auth
from selenium.webdriver.common.keys import Keys

#%%

def wait_for(target):
    while not(target in str(driver.page_source.encode("utf-8"))):
        time.sleep(0.01)

driver = webdriver.Chrome(executable_path=r'C:/webdrivers/chromedriver.exe')

#%%
driver.get('https://www.southwest.com/air/check-in/index.html')

Checkin_Element = '<span class="submit-button--text">Check in</span>'

wait_for(Checkin_Element)

#%%

PNR_No = 'TWITR7'
First_Name = 'Richie'
Last_Name = 'Rivera'

PNR = driver.find_element_by_id('confirmationNumber')
FName = driver.find_element_by_id('passengerFirstName')
LName = driver.find_element_by_id('passengerLastName')

checkin = driver.find_element_by_id('form-mixin--submit-button')

PNR.clear()
FName.clear()
LName.clear()

PNR.send_keys(PNR_No)
FName.send_keys(First_Name)
LName.send_keys(Last_Name)

checkin.click()

#%%

find_conf= '<span class="confirmation-number--code">' + PNR_No + '</span>'

wait_for(find_conf)

checkin_final = driver.find_element_by_class_name('actionable actionable_button actionable_large-button actionable_no-outline actionable_primary button submit-button air-check-in-review-results--check-in-button'.replace(' ','.'))

checkin_final.click()
