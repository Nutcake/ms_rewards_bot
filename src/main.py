import os
import random
import sys
import time

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import nltk
from nltk.corpus import words
from tqdm import tqdm

email = os.getenv("REWARDS_ACC_EMAIL")
passwd = os.getenv("REWARDS_ACC_PASS")

error = False


if email is None:
    print("Error: Environment variable 'REWARDS_ACC_EMAIL' has to be set")
    error = True

if passwd is None:
    print("Error: Environment variable 'REWARDS_ACC_PASS' has to be set")
    error = True

if error:
    print("Errors occured, quitting...")
    sys.exit(-1)

print("Downloading wordlist...")
nltk.download("words", quiet=True)


def is_in_docker():
    path = '/proc/self/cgroup'
    return os.path.exists('/.dockerenv') or os.path.isfile(path) and any('docker' in line for line in open(path))


def do_login(driver, email, passwd):
    try:
        uname_field = driver.find_element_by_xpath('//*[@id="i0116"]')
    except (StaleElementReferenceException, NoSuchElementException):
        print("Already logged in.")
        return

    uname_field.click()
    uname_field.clear()
    uname_field.send_keys(email)

    sing_in_btn = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
    sing_in_btn.click()

    time.sleep(1)

    pw_field = driver.find_element_by_xpath('//*[@id="i0118"]')
    pw_field.click()
    pw_field.clear()
    pw_field.send_keys(passwd)

    sing_in_btn = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
    sing_in_btn.click()

    time.sleep(1)

    sing_in_btn = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
    sing_in_btn.click()


wordlist = words.words()

print("Creating chrome session...")
options = Options()
options.headless = True

if is_in_docker():
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disk-cache-size=0")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-offline-load-stale-cache")

driver = webdriver.Chrome(options=options)


print("Logging in to MS Rewards...")
driver.get("https://rewards.microsoft.com")

try:
    btn = driver.find_element_by_xpath("//*[@id='raf-signin-link-id']")
    btn.click()
    time.sleep(2)
    do_login(driver, email, passwd)
except (StaleElementReferenceException, NoSuchElementException):
    print("Failed to log in, quitting...")
    sys.exit(-2)

print("Doing click-activities...")
cards = driver.find_elements_by_xpath("//*[@id='ma-card-link']")

for card in tqdm(cards):
    driver.execute_script("arguments[0].click();", card)
    time.sleep(2)

print("Doing desktop searches...")

for i in tqdm(range(30)):
    driver.get(f"https://www.bing.com/search?q="
               f"{random.choice(wordlist)}")
    time.sleep(random.random()+1.0)

driver.quit()

mobile_emu = {"deviceName": "Pixel 2"}

options.add_experimental_option("mobileEmulation", mobile_emu)
driver = webdriver.Chrome(options=options)

print("Doing mobile searches...")

for i in tqdm(range(20)):
    driver.get(f"https://www.bing.com/search?q={random.choice(wordlist)}")
    time.sleep(random.random()+1.0)

driver.quit()
vdisp.stop()

print("Done.")
