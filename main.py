from selenium import webdriver
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

def startFlow(CURRENT_ACCOUNT, index):
    DRIVER = webdriver.Chrome(ChromeDriverManager().install())
    DRIVER.implicitly_wait(constants.IDLE_FOR_ELEMENT_TO_BE_FOUND)
    DRIVER.get(INSTAGRAM_MAINPAGE_URL)

    try:
        usernameInput = DRIVER.find_element_by_xpath(INPUT_USERNAME)
        usernameInput.clear()
        usernameInput.send_keys(CURRENT_ACCOUNT.username)

        passwordInput = DRIVER.find_element_by_xpath(INPUT_PASSWORD)
        passwordInput.clear()
        passwordInput.send_keys(CURRENT_ACCOUNT.password)

        DRIVER.find_element_by_xpath(BUTTON_LOGIN).click()

        DRIVER.find_element_by_xpath(BUTTON_DONTSAVE).click()
    except:
        input("login failed, enter something to exit.")

        DRIVER.quit()

    COUNT = 0;
    
    while True:
        shuffledACCOUNTS = constants.ACCOUNTS.copy()
        random.shuffle(shuffledACCOUNTS)
        
        for ACCOUNT in shuffledACCOUNTS:

            try:
                DRIVER.get(INSTAGRAM_MAINPAGE_URL + ACCOUNT)
            except:
                print(f'page opening failed for:"{INSTAGRAM_MAINPAGE_URL}{ACCOUNT}"')
            
                time.sleep(constants.IDLE_FOR_UNHANDLED_BAN)

            try:
                DRIVER.find_element_by_xpath(BUTTON_OPENUNFOLLOW).click()

                DRIVER.find_element_by_xpath(BUTTON_UNFOLLOW).click()
            except:
                print(f'follow failed for:"{ACCOUNT}"')
                    
                time.sleep(constants.IDLE_FOR_UNHANDLED_BAN)  

            try:
                DRIVER.find_element_by_xpath(BUTTON_FOLLOW).click()
            except:
                print(f'follow failed for:"{ACCOUNT}"')
            
                time.sleep(constants.IDLE_FOR_UNHANDLED_BAN)

            time.sleep(constants.IDLE_FOR_PER_ACCOUNT + (random.uniform(0, 1) * constants.CONSTANT_IDLE_RANDOM_MULTIPILER_FOR_PER_ACCOUNT))
    
        WAIT_FOR = constants.IDLE_FOR_PER_ITERATE + (random.uniform(0, 1) * constants.CONSTANT_IDLE_RANDOM_MULTIPILER_FOR_PER_ITERATE)
        
        COUNT += 1
        
        NOW = datetime.now()
        
        START_TIME = timedelta(seconds=WAIT_FOR)
        
        print(f'Iterate ended for:Thread-{index}. Total:{COUNT}. Ended at:{NOW}. Gonna Start at:{START_TIME}')
        
        time.sleep(WAIT_FOR)

for i in range(len(constants.TEST_ACCOUNTS)):
    threading.Thread(target=startFlow, args=(constants.TEST_ACCOUNTS[i], i)).start()