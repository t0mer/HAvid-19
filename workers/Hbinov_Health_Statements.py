# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
import time, os
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from loguru import logger
import helpers, yaml
configfile="/opt/dockerbot/config/config.yml"
original_configfile = r'/etc/config.yml'
def ReadConfig():
    with open(configfile, 'r') as stream:
        try:
            logger.info("Reading Configuration")
            list = yaml.safe_load(stream)
            return list
        except yaml.YAMLError as ex:
            logger.error("Error Reading Configuration, Msg: " + str(ex))
            return ""

def sign():
    list = ReadConfig()
    try:
        logger.info("Starting process")
        browser = helpers.GetBrowser()
       
        time.sleep(1)
        try:
            helpers.ping(browser, 'infogan')
        except:
            logger.debug('Unable to ping')

        browser.get(str(list['hbinov']['URL']))
        time.sleep(1)


        
        # #get needed elements
        Identity = '//*[@id="Identity"]' 
        Password = '//*[@id="Password"]' 
        Login = '//*[@id="login"]' 
        Full_Name = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div/div[3]/div/div[2]/div/input' 
        Mobile_Phone = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div/div[4]/div/div[2]/div/input'
        Worker_ID = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div/div[5]/div/div[2]/div/input'



        ######## Fill Login Details #####
        logger.info("Logging in")    
        #Fill Username
        browser.find_element_by_xpath(Identity).send_keys(str(list['hbinov']['USER_NAME']))
        #Fill Password
        browser.find_element_by_xpath(Password).send_keys(str(list['hbinov']['PASSWORD']))
        # #Login
        browser.find_element_by_xpath(Login).click() 
        time.sleep(2)
        logger.info("Logged in!")

        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[1]/a').click()
        time.sleep(1)


        # browser.find_element_by_id('ProjectId').send_keys("אדמה מכתשים - נאות חובב", Keys.ENTER)
       
        project = browser.find_element_by_xpath('//*[@id="ProjectId"]')
        browser.execute_script("arguments[0].setAttribute('value', 'אדמה מכתשים - נאות חובב')", project)
        helpers.fullpage_screenshot(browser,'/opt/dockerbot/images/test1.png')
        # project.click()
        # project.send_keys(Keys.ARROW_DOWN)
        # project.send_keys(Keys.RETURN)


        # review = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[2]/div/div/span/span/span[1]')
        # review.click()
        # review.send_keys(Keys.ARROW_DOWN)
        # review.send_keys(Keys.RETURN)

        # browser.find_element_by_xpath('//*[@id="setupSave"]').click()


        
        # helpers.largepage_screenshot(browser,'/opt/dockerbot/images/step_2.png')



        ######### Filling up the form ############


        # browser.find_element_by_xpath(Full_Name).clear()
        # browser.find_element_by_xpath(Full_Name).send_keys(str(list['hbinov']['NAME']))
        
        # browser.find_element_by_xpath(Mobile_Phone).clear()
        # browser.find_element_by_xpath(Mobile_Phone).send_keys(str(list['hbinov']['MOBILE']))
        
        # browser.find_element_by_xpath(Worker_ID).clear()
        # browser.find_element_by_xpath(Worker_ID).send_keys(str(list['hbinov']['ID']))
        
        # browser.find_element_by_xpath('//*[@id="466557"]').click()
        # browser.find_element_by_xpath('//*[@id="466559"]').click()
        # browser.find_element_by_xpath('//*[@id="466561"]').click()
        

        # browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div/div[10]/div/div[2]/div/div[1]').click()
        # time.sleep(1)

        # canvas = browser.find_element_by_class_name("sigCanvas")
        # drawing = ActionChains(browser)\
        #     .click_and_hold(canvas)\
        #     .move_by_offset(0, 0)\
        #     .move_by_offset(20, 32)\
        #     .move_by_offset(10, 25)\
        #     .release()
        # drawing.perform()

        # browser.find_element_by_xpath('/html/body/aside[2]/div/div/a[2]').click()
        
        # signiture = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div/div[10]/div/div[2]/div/div[2]/img')
        # with open('/opt/dockerbot/config/' + str(list['hbinov']['SIG_FILE']) , 'r') as file:
        #     data = file.read().replace('\n', '')
        #     browser.execute_script("arguments[0].setAttribute('src', '"+ data +"')", signiture);


        # browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div[3]/div/a').click()

        

        # helpers.log_browser(browser)
        # helpers.fullpage_screenshot(browser,'/opt/dockerbot/images/step2.png')
        
       
        return 1
    except Exception as ex:
        logger.error(str(ex))
        return 0