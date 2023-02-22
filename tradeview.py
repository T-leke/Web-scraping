from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC1
from PIL import Image
import time
import sys
import clipboard
import pyperclip

url = "https://www.tradingview.com/chart/?symbol=BYBIT%3ABTCUSD"

chrome_driver_path = "C:/Users/OGIDAN TOLU/Desktop/SELF LEARN/selenium/chromedriver" #driver location on the laptop

chrome_options = Options() #instance of the option object
chrome_options.add_argument("--headless")


driver = webdriver.Chrome(
    executable_path = chrome_driver_path,
    options = chrome_options
)


driver.get(url)
time.sleep(3)

# ActionChains(driver).key_down(Keys.ALT).send_keys('s').perform() #click the screenshot button on tradeview
# driver.implicitly_wait(10)
element = driver.find_element_by_class_name("layout__area--center")

location = element.location
size = element.size


x = location['x']
y = location['y']
w = size['width']
h = size['height']
width = x + w
height = y + h

driver.get_screenshot_as_file("tradeview.png")

im = Image.open("tradeview.png")

im = im.crop((int(x), int(y), int(width), int(height)))
im.save('cropped_trade.png')

driver.close()
