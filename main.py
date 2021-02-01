from constants import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os

INPUT_USERNAME = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input"
INPUT_PASSWORD = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input"
BUTTON_LOGIN = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button"
BUTTON_DONTSAVE = "/html/body/div[1]/section/main/div/div/div/div/button"
BUTTON_OPENUNFOLLOW = "//*[@id='react-root']/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button"
BUTTON_UNFOLLOW = "//*[text()='Unfollow']"
BUTTON_FOLLOW = "//*[text()='Follow']"
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
FOLLOW_ACCOUNT_PAGE = "https://www.instagram.com/cristiano"
PAGE = "https://www.instagram.com"

driver = webdriver.Chrome(ChromeDriverManager().install())

try:
    driver.implicitly_wait(10)
    driver.get(PAGE)

    usernameInput = driver.find_element_by_xpath(INPUT_USERNAME)
    usernameInput.clear()
    usernameInput.send_keys(USERNAME)

    passwordInput = driver.find_element_by_xpath(INPUT_PASSWORD)
    passwordInput.clear()
    passwordInput.send_keys(PASSWORD)

    driver.find_element_by_xpath(BUTTON_LOGIN).click()

    driver.find_element_by_xpath(BUTTON_DONTSAVE).click()

    driver.get(FOLLOW_ACCOUNT_PAGE)

    try:
        driver.find_element_by_xpath(BUTTON_OPENUNFOLLOW).click()

        unfollowButton = driver.find_element_by_xpath(BUTTON_UNFOLLOW).click()
        print("Unfollow success")
    except:
        print("Unfollow failed")

    try:
        driver.find_element_by_xpath(BUTTON_FOLLOW).click()
        print("Follow success")
    except:
        print("Follow failed")
except:
    print("Something went wrong")
    driver.quit()

driver.quit()