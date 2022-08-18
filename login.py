from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import yaml

conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
xemail = conf['zoom']['email']
xpass = conf['zoom']['password']

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# ("/Users/Pasha/Documents/sandboxxx/pscript/chromedriver")

def login(url, usernameId, username, passwordId, password):
    driver.get(url)
    driver.find_element(By.ID, usernameId).send_keys(username)
    driver.find_element(By.ID, passwordId).send_keys(password)
    driver.find_element(By.ID, passwordId).send_keys(Keys.RETURN)
    driver.set_script_timeout(5000)
    driver.refresh()
    driver.implicitly_wait(5)
    driver.find_element(By.ID, usernameId).send_keys(username)
    driver.find_element(By.ID, passwordId).send_keys(password)
    driver.find_element(By.ID, passwordId).submit()
    # driver.find_element(By.ID, passwordId).send_keys(Keys.RETURN);
    # driver.find_element_by_id(submit_buttonId).click()

login(
    "https://zoom.us/signin",
    "email",
    xemail,
    "password",
    xpass
)