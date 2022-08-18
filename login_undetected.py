def zoomFlow(driver, username, password):
    driver.get("https://zoom.us/signin/")
    driver.delete_all_cookies()
    # driver.refresh()
    driver.find_element(By.ID, "email").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    time.sleep(5)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    time.sleep(5)
    # driver.get("https://us04web.zoom.us/recording")

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import undetected_chromedriver as uc
    import time
    import yaml

    conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
    xemail = conf['zoom2']['email']
    xpass = conf['zoom2']['password']

    options = uc.ChromeOptions()

    driver = uc.Chrome(options=options)
    
    zoomFlow(
        driver,
        xemail,
        xpass
    )

    time.sleep(10)