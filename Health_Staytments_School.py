 #-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import time
from datetime import datetime
import time
from argparse import ArgumentParser
import os
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

parser = ArgumentParser()
parser.add_argument("-s", "--school", dest="schoolCode")
parser.add_argument("-u", "--user", dest="userCode")
parser.add_argument("-p", "--pass", dest="SitePassword")
parser.add_argument("-k", "--kid", dest="KidCovid")


args = parser.parse_args()
schoolCode = args.schoolCode
userCode = args.userCode
SitePassword = args.SitePassword
KidCovid = args.KidCovid
option = webdriver.ChromeOptions()
option.add_argument("-incognito")
option.add_argument("--headless")
option.add_argument("disable-gpu")
option.add_argument("--no-sandbox")
option.add_argument('--start-maximized')
option.add_argument("--disable-dev-shm-usage")
option.add_argument("--window-size=800,600")

def fullpage_screenshot():
    print(browser)
    browser.set_window_size(800, 600) #the trick
    time.sleep(2)
    image = "/opt/Approval_form.png"
    browser.save_screenshot(image)
    browser.close()
print("Strating process")

browser = webdriver.Chrome(executable_path="/opt/chromedriver-85.0.4183.87/chromedriver", options=option)
browser.get("https://web.mashov.info/students/login")
browser.find_element(By.ID, "mat-input-3").click()
browser.find_element(By.ID, "mat-input-3").send_keys(schoolCode)
browser.find_element(By.ID, "mat-input-3").send_keys(Keys.ENTER)
browser.find_element(By.ID, "mat-select-0").click()
browser.find_element(By.XPATH,'//mat-option[@tabindex="0"]').click()
browser.find_element(By.ID, "mat-input-0").send_keys(userCode)
browser.find_element(By.ID, "mat-input-4").send_keys(SitePassword)
browser.find_element(By.CSS_SELECTOR, ".mshv-primary").click()
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.splash-purple')))
#time.sleep( 5 )
browser.get("https://web.mashov.info/students/main/covidClearance")
browser.find_element(By.ID, "mat-checkbox-1").click()
browser.find_element(By.ID, "mat-checkbox-2").click()
browser.find_element(By.CSS_SELECTOR, ".mat-primary > .mat-button-wrapper").click()
fullpage_screenshot()

