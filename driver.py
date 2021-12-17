from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from constants import *
from time import sleep
from random import choice
from os import environ


def driver(i):
    # Create a new instance of the Chrome driver
    options = Options()
    options.binary_location = environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    bot = webdriver.Chrome(chrome_options=options)

    # Login to Twitter
    def login(i):
        try:
            bot.get("https://twitter.com/login")
            username = WebDriverWait(bot, 20).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username.clear()
            username.send_keys(Accounts["account{}".format(i)]["username"])
            sleep(1)
            username.send_keys(Keys.RETURN)
            password = WebDriverWait(bot, 20).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password.clear()
            password.send_keys(Accounts["account{}".format(i)]["password"])
            sleep(1)
            password.send_keys(Keys.RETURN)
            sleep(5)
            # If the bot finds the "Account" button, it means the login was successful
            if (bot.find_element(By.CSS_SELECTOR,
                                 '.css-18t94o4[data-testid="SideNav_AccountSwitcher_Button"]') is not None):
                return True
            else:
                return False
        except Exception:
            print("Login Failed for account{}".format(i))
            return False

    # Function to reply to the tweets
    def reply_to_tweets():
        tweets = set()
        try:
            query = "%20OR%20".join(Keywords)
            bot.get("https://twitter.com/search?q=(" + query + ")&src=typed_query&f=live")
            sleep(5)
            for _ in range(0, 1):
                bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                [
                    tweets.add(elem.get_attribute('href')) \
                    for elem in bot.find_elements(By.XPATH, "//a[@dir ='auto']")
                ]
            for tweet in tweets:
                try:
                    bot.get(tweet)
                    sleep(5)
                    reply_box = bot.find_element(By.CSS_SELECTOR,
                                                 '.public-DraftEditor-content[data-testid="tweetTextarea_0"]')
                    reply_box.send_keys(choice(Tweets))
                    sleep(2)
                    bot.find_element(By.CSS_SELECTOR, '.css-18t94o4[data-testid="tweetButtonInline"]').click()
                    sleep(TweetCooldown)
                    break
                except Exception as e:
                    print("Reply to Tweets Failed")
        except Exception:
            print("Reply Failed")

    if login(i):
        reply_to_tweets()
        bot.close()
        return True
    else:
        print("Login Failed")
        return False
