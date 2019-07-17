#%%
import time
from selenium import webdriver
from pyutils import get_auth
from selenium.webdriver.common.keys import Keys
import os

script_dir = os.getcwd()

if 'win' in str(sys.platform):
    driver_path = script_dir + '\chromedrivers\win_chromedriver.exe'
else:
    driver_path = script_dir + '/chromedrivers/mac_chromedriver'


#%%
def login():
    EID = get_auth()[0]
    PWD = get_auth()[1]

    U_Box = driver.find_element_by_name('userID')
    P_Box = driver.find_element_by_name('password')

    U_Box.send_keys(EID)
    P_Box.send_keys(PWD)

    driver.find_element_by_name('submitButton').click()

#%%

driver = webdriver.Chrome(executable_path=driver_path)

#%%
driver.get('https://newjetnet.aa.com/')

login()

#%%
driver.find_element_by_link_text('Travel Planner').click()

#%%

driver.switch_to.window(driver.window_handles[0])

driver.close()

driver.switch_to.window(driver.window_handles[0])

time.sleep(5)

#%%

origin = driver.find_element_by_name('origin')
dest = driver.find_element_by_name('destination')

nr_type = driver.find_element_by_name('type')
send = driver.find_element_by_class_name('btn.btn-primary')

#%%

nr_type.send_keys(Keys.BACKSPACE*10 + 'Space')
origin.send_keys(Keys.BACKSPACE*10 + 'DFW')
dest.send_keys(Keys.BACKSPACE*10 + 'CDG')

#%%
send.click()
#%%

time.sleep(5)

print(driver.page_source.encode("utf-8"))