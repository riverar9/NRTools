#%%
import time
import itineraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import sys
import pickle as pkl

#%%

def flight_checkin(listings):
    def wait_for(target):
        while not(target in str(driver.page_source.encode("utf-8"))):
            time.sleep(0.01)

    script_dir = os.getcwd()

    if 'darwin' == str(sys.platform):
        driver_path = script_dir + "/chromedrivers/mac_chromedriver"
    elif 'win' in str(sys.platform):
        driver_path = script_dir + "\chromedrivers\win_chromedriver.exe"
    else:
        raise Exception("App doesn't work for the current OS ({}).".format(str(sys.platform)))
        
    driver = webdriver.Chrome(executable_path=driver_path)

    for each in listings:
        driver.get('https://www.southwest.com/air/check-in/index.html')

        wait_for('<span class="submit-button--text">Check in</span>')

        conf_no_elemet = driver.find_element_by_id('confirmationNumber')
        fname_element = driver.find_element_by_id('passengerFirstName')
        lname_element = driver.find_element_by_id('passengerLastName')
        checkin1_element = driver.find_element_by_id('form-mixin--submit-button')

        conf_no_elemet.clear()
        fname_element.clear()
        lname_element.clear()

        conf_no_elemet.send_keys(each.confirmation_number)
        fname_element.send_keys(each.first_name)
        lname_element.send_keys(each.last_name)

        checkin1_element.click()
        time.sleep(1.5)

        checkin_early_string = "You're requesting to check in and print your boarding pass outside our permitted 24 hour check-in window. Please check in within 24 hours of your flight's scheduled departure."

        if checkin_early_string in str(driver.page_source.encode("utf-8")):
            while checkin_early_string in str(driver.page_source.encode("utf-8")):
                checkin1_element.click()
                time.sleep(0.25)
        
        final_conf_string = '<span class="confirmation-number--code">' + each.confirmation_number + '</span>'

        if final_conf_string in str(driver.page_source.encode("utf-8")):
            checkin2_element = driver.find_element_by_class_name('actionable actionable_button actionable_large-button actionable_no-outline actionable_primary button submit-button air-check-in-review-results--check-in-button'.replace(' ','.'))
            checkin2_element.click()

            wait_for('Security document issued.')

            driver.close()
        else:
            pkl.dump(driver.page_source.encode("utf-8"), open('/Exceptions/' + each.confirmation_number + '.txt','wb'))
            raise Exception("Unexpected scenerio. Saved in {}.".format(str(sys.platform)))