#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver=webdriver.PhantomJS()
driver.get("https://www.yuque.com/login")

driver.find_element_by_id("login").send_keys("1968574010@qq.com")
driver.find_element_by_id("password").send_keys("LXQ1996@hacker")


driver.find_element_by_xpath("//button[@class='ant-btn btn-login ant-btn-primary ant-btn-lg ant-btn-block']").click()

time.sleep(3)

driver.save_screenshot("douban.png")
driver.quit()