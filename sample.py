# import undetected_chromedriver as uc
# driver = uc.Chrome()
# driver.get("https://zoom.us/")

# if __name__ == '__main__':
#     import undetected_chromedriver.v2 as uc
#     driver = uc.Chrome()
#     driver.get('https://zoom.us/')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import yaml

conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
xemail = conf['zoom']['email']
xpass = conf['zoom']['password']

chrome_options = Options()
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(executable_path="/Users/Pasha/Documents/sandboxxx/pscript/chromedriver",options=chrome_options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# driver.get("https://www.reddit.com/login")
# driver.find_element(By.ID, "loginUsername").send_keys(conf['reddit']['username'])
# driver.find_element(By.ID, "loginPassword").send_keys(conf['reddit']['password'])
# driver.find_element(By.XPATH, "/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button").click()

driver.get("https://zoom.us/signin")
driver.find_element(By.ID, "email").send_keys(xemail)
time.sleep(2)
driver.find_element(By.ID, "password").send_keys(xpass)
time.sleep(2)
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
time.sleep(5)
driver.get("https://us04web.zoom.us/recording")

