from logging import log
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import threading
import time
import random
import constants

INPUT_USERNAME = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input"
INPUT_PASSWORD = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input"
BUTTON_LOGIN = "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button"
BUTTON_DONTSAVE = "/html/body/div[1]/section/main/div/div/div/div/button"
BUTTON_OPENUNFOLLOW = "//*[@id='react-root']/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button"
BUTTON_UNFOLLOW = "//*[text()='Unfollow']"
BUTTON_FOLLOW = "//*[text()='Follow']"
INSTAGRAM_MAINPAGE_URL = "https://www.instagram.com/"

op = webdriver.ChromeOptions()
op.add_argument('--headless')

def checkIfElementExist(self, xpath):
    try:
        element = self.find_element_by_xpath(xpath)
        return True
    except NoSuchElementException:
        return False

def login(self, account):
    try:
        usernameInput = self.find_element_by_xpath(INPUT_USERNAME)
        usernameInput.clear()
        usernameInput.send_keys(account.username)

        passwordInput = self.find_element_by_xpath(INPUT_PASSWORD)
        passwordInput.clear()
        passwordInput.send_keys(account.password)

        self.find_element_by_xpath(BUTTON_LOGIN).click()

        self.find_element_by_xpath(BUTTON_DONTSAVE).click()

        print(f'logged as {account.username}')
        
        return True
    except:
        input(f'login failed for {account.username}, enter something to exit. at:{datetime.now()}')

        self.quit()

        return False

def triggerFollow(self, account, target):
    try:
        self.find_element_by_xpath(BUTTON_FOLLOW).click()

        print(f'follow successed for:"{target}" at:{datetime.now()} current_acount:{account}')

        time.sleep(constants.IDLE_FOR_COMMON_ACTIONS)
    except:
        print(f'follow failed for:"{target}" at:{datetime.now()} gonna wait:{constants.IDLE_FOR_UNHANDLED_BAN} seconds. current_acount:{account}')

        time.sleep(constants.IDLE_FOR_UNHANDLED_BAN)

def triggerUnfollow(self, account, target):
    try:
        self.find_element_by_xpath(BUTTON_OPENUNFOLLOW).click()

        self.find_element_by_xpath(BUTTON_UNFOLLOW).click()

        print(f'unfollow successed for:"{target}" at:{datetime.now()} current_account:{account}')
        
        time.sleep(constants.IDLE_FOR_COMMON_ACTIONS)
    except:
        print(f'unfollow failed for:"{target}" at:{datetime.now()} gonna wait:{constants.IDLE_FOR_UNHANDLED_BAN} seconds. current_acount:{account}')
                    
        time.sleep(constants.IDLE_FOR_UNHANDLED_BAN)

def startFlow(CURRENT_ACCOUNT, index):
    
    COUNT = 0;

    DRIVER = webdriver.Chrome(ChromeDriverManager().install(), options = op)
    DRIVER.implicitly_wait(constants.IDLE_FOR_ELEMENT_TO_BE_FOUND)
    DRIVER.get(INSTAGRAM_MAINPAGE_URL)

    if login(DRIVER, CURRENT_ACCOUNT) == False:
        return
    
    while True:
        shuffledACCOUNTS = constants.ACCOUNTS.copy()
        random.shuffle(shuffledACCOUNTS)
        
        for ACCOUNT in shuffledACCOUNTS:

            DRIVER.get(INSTAGRAM_MAINPAGE_URL + ACCOUNT)

            if checkIfElementExist(DRIVER, BUTTON_FOLLOW) == False:
                triggerUnfollow(DRIVER, CURRENT_ACCOUNT.username, ACCOUNT)
                triggerFollow(DRIVER, CURRENT_ACCOUNT.username, ACCOUNT)
            else:
                triggerFollow(DRIVER, CURRENT_ACCOUNT.username, ACCOUNT)

            time.sleep(constants.IDLE_FOR_PER_ACCOUNT + (random.uniform(0, 1) * constants.CONSTANT_IDLE_RANDOM_MULTIPILER_FOR_PER_ACCOUNT))
    
        WAIT_FOR = constants.IDLE_FOR_PER_ITERATE + (random.uniform(0, 1) * constants.CONSTANT_IDLE_RANDOM_MULTIPILER_FOR_PER_ITERATE)
        
        COUNT += 1
        
        NOW = datetime.now()
        
        START_TIME = timedelta(seconds=WAIT_FOR) + NOW
        
        print(f'Iterate ended for:Thread-{index}. Total:{COUNT}. Ended at:{NOW}. Gonna Start at:{START_TIME}')
        
        time.sleep(WAIT_FOR)

for i in range(len(constants.TEST_ACCOUNTS)):
    threading.Thread(target=startFlow, args=(constants.TEST_ACCOUNTS[i], i)).start()