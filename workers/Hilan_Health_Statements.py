# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
import time, os
from selenium.common.exceptions import InvalidSessionIdException
from loguru import logger
import helpers

# from workers import Hilan_Health_Statements


def sign(usr, passw, formUrl, Image):

    try:
        logger.info("Starting process")
        browser = helpers.GetBrowser()
        try:
            helpers.ping(browser, 'infogan')
        except:
            logger.debug('Unable to ping')

        browser.get(formUrl)
        helpers.log_browser(browser)
        #get needed elements
        employee_id = '//*[@id="user_nm"]'
        empoyee_pass = '//*[@id="password_nm"]'

        browser.find_element_by_xpath(employee_id).send_keys(usr)
        browser.find_element_by_xpath(empoyee_pass).send_keys(passw)

        #Login
        browser.find_element_by_xpath('//*[@type="submit"]').click()
        time.sleep(4)
        helpers.log_browser(browser)
        helpers.fullpage_screenshot(browser,Image)

        return 1
    except Exception as ex:
        logger.error(str(ex))
        return 0
