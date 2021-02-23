from re import TEMPLATE
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import random
import os

class IG_ACCOUNT:
    def __init__(myobj, username, password):
        myobj.username = username
        myobj.password = password

INPUT_USERNAME = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input"
INPUT_PASSWORD = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input"
BUTTON_LOGIN = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button"
BUTTON_DONTSAVE = "/html/body/div[1]/section/main/div/div/div/div/button"
BUTTON_OPENUNFOLLOW = "//*[@id='react-root']/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button"
BUTTON_UNFOLLOW = "//*[text()='Unfollow']"
BUTTON_FOLLOW = "//*[text()='Follow']"
TEST_ACCOUNTS = [ IG_ACCOUNT("", "") ]
INSTAGRAM_MAINPAGE_URL = "https://www.instagram.com/"
ACCOUNTS = [
    "cristiano", 
    "arianagrande"
]
IDLE_FOR_PER_ACCOUNT = 5
CONSTANT_IDLE_RANDOM_MULTIPILER_FOR_PER_ACCOUNT = 1
IDLE_FOR_PER_ITERATE = 300
CONSTANT_IDLE_RANDOM_MULTIPILER_FOR_PER_ITERATE = 10
IDLE_FOR_UNHANDLED_BAN = 600
IDLE_FOR_ELEMENT_TO_BE_FOUND = 10

def startFlow(account, index):
    print(account.username, account.password)
    DRIVER = webdriver.Chrome(ChromeDriverManager().install())
    DRIVER.implicitly_wait(IDLE_FOR_ELEMENT_TO_BE_FOUND)
    DRIVER.get(INSTAGRAM_MAINPAGE_URL)

    try:
        usernameInput = DRIVER.find_element_by_xpath(INPUT_USERNAME)
        usernameInput.clear()
        usernameInput.send_keys(account.username)

        passwordInput = DRIVER.find_element_by_xpath(INPUT_PASSWORD)
        passwordInput.clear()
        passwordInput.send_keys(account.password)

        DRIVER.find_element_by_xpath(BUTTON_LOGIN).click()

        DRIVER.find_element_by_xpath(BUTTON_DONTSAVE).click()
    except:
        input("login failed, enter something to exit.")

        DRIVER.quit()

    while True:
        shuffledACCOUNTS = random.shuffle(ACCOUNTS.copy())
        for ACCOUNT in shuffledACCOUNTS:

            try:
                DRIVER.get(INSTAGRAM_MAINPAGE_URL + ACCOUNT)
            except:
                print(f'page opening failed for:"{INSTAGRAM_MAINPAGE_URL}{ACCOUNT}"')
            
                time.sleep(IDLE_FOR_UNHANDLED_BAN)

            try:
                DRIVER.find_element_by_xpath(BUTTON_OPENUNFOLLOW).click()

                DRIVER.find_element_by_xpath(BUTTON_UNFOLLOW).click()
            except:
                print(f'follow failed for:"{ACCOUNT}"')
                    
                time.sleep(IDLE_FOR_UNHANDLED_BAN)  

            try:
                DRIVER.find_element_by_xpath(BUTTON_FOLLOW).click()
            except:
                print(f'follow failed for:"{ACCOUNT}"')
            
                time.sleep(IDLE_FOR_UNHANDLED_BAN)

            time.sleep(IDLE_FOR_PER_ACCOUNT + (random.uniform(0, 1) * CONSTANT_IDLE_RANDOM_MULTIPILER_FOR_PER_ACCOUNT))
    
        time.sleep(IDLE_FOR_PER_ITERATE + (random.uniform(0, 1) * CONSTANT_IDLE_RANDOM_MULTIPILER_FOR_PER_ITERATE))

for i in range(len(TEST_ACCOUNTS)):
    threading.Thread(target=startFlow, args=(TEST_ACCOUNTS[i], i)).start()