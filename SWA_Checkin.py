#%%
import time
import itineraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os
import sys
import pickle as pkl


#%%

def flight_checkin(listings):
    def wait_for(target):
        condition_met = 0
        while not(condition_met):
            for each in target:
                if each in str(driver.page_source.encode("utf-8")):
                    condition_met = 1

    script_dir = os.getcwd()

    if 'darwin' == str(sys.platform):
        driver_path = script_dir + r"/chromedrivers/mac_chromedriver"
    elif 'win' in str(sys.platform):
        driver_path = script_dir + r"\chromedrivers\win_chromedriver.exe"
    else:
        raise Exception("App doesn't work for the current OS ({}).".format(str(sys.platform)))

    checkin_link = 'https://www.southwest.com/air/check-in/index.html'

    for each in listings:
        driver = webdriver.Chrome(executable_path=driver_path)
        print("Checking into flight:\t{}".format(each.confirmation_number))
        driver.get(checkin_link)

        wait_for(['<span class="submit-button--text">Check in</span>'])

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

        while not ((each.checkin_datetime - datetime.now()).total_seconds() < 1):
            time.sleep(.01)

        checkin1_element.click()

        wait_for_strings = ["Online check-in not valid at this time.",\
            '<span class="confirmation-number--code">' + each.confirmation_number + '</span>',\
            "We are unable to retrieve your reservation.",\
            "Sorry, your itinerary is ineligible for check in online.",\
            "We do not allow online check-in within one hour from a flight's departure. Please proced to the airport to checkin for this flight.",\
            "We are unable to retrieve your reservation.",\
            "Flight in the past."]

        moved_on = False
        try:
            while not(moved_on):
                wait_for(wait_for_strings)

                if wait_for_strings[4] in str(driver.page_source.encode("utf-8")):
                    moved_on = True
                    print("Flight within one hour, can't do it boss.")

                if wait_for_strings[0] in str(driver.page_source.encode("utf-8")): #checks if this case is the attempted to early case
                    while wait_for_strings[0] in str(driver.page_source.encode("utf-8")):
                        try:
                            checkin1_element.click()
                        except:
                            pass

                if (wait_for_strings[1] in str(driver.page_source.encode("utf-8"))\
                    or wait_for_strings[3] in str(driver.page_source.encode("utf-8"))\
                    or wait_for_strings[2] in str(driver.page_source.encode("utf-8"))\
                    or wait_for_strings[5] in str(driver.page_source.encode("utf-8"))\
                    or wait_for_strings[6] in str(driver.page_source.encode("utf-8"))):
                    moved_on = True


            if wait_for_strings[1] in str(driver.page_source.encode("utf-8")):
                checkin2_element = driver.find_element_by_class_name('actionable actionable_button actionable_large-button actionable_no-outline actionable_primary button submit-button air-check-in-review-results--check-in-button'.replace(' ','.'))
                checkin2_element.click()

                wait_for(['Security document issued.'\
                    ,'Interisland Carryon Restrictions'])

                print("Completed checking into:\t{}".format(each.confirmation_number))
                driver.close()
            else:
                pkl.dump(driver.page_source.encode("utf-8"), open(each.confirmation_number + '_issue.txt','wb'))
                print("Unexpected scenerio. Saved as {}.".format(each.confirmation_number + '_issue.txt'))
                driver.close()
        except:
            pass

#%%
