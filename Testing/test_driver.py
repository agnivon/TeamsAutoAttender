import os
import time
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from LOCATORS import *

opt = Options()
opt.add_argument("--headless")
opt.add_argument("--disable-infobars")
opt.add_argument("--window-size=1920,1080")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
# opt.add_argument("--mute-audio")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})

URL = "https://teams.microsoft.com"
email = '1mj18cs010@mvjce.edu.in'
passwd = 'Fuckmvj6ever'

driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=opt,
                          service_log_path='NUL')


def login():
    creds = {'email': email, 'passwd': passwd}
    k = 3
    nist = 3  # Not Interactable Sleep Time
    while k >= 0:
        try:
            driver.get(URL)
            WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

            if "login.microsoftonline.com" in driver.current_url:
                # login required
                email_field = driver.find_element_by_xpath(EMAIL_FIELD)
                # email_field.click()
                email_field.send_keys(creds['email'])
                time.sleep(nist)
                driver.find_element_by_xpath(EMAIL_NEXT_BUTTON).click()  # Next button
                time.sleep(nist)
                password_field = driver.find_element_by_xpath(PASSWD_FIELD)
                password_field.click()
                password_field.send_keys(creds['passwd'])
                time.sleep(1)
                driver.find_element_by_xpath(SIGNIN_BUTTON).click()  # Sign in button
                time.sleep(1)
                driver.find_element_by_xpath(REM_LOGIN_BUTTON).click()  # remember login
                time.sleep(1)
                for element in driver.find_elements_by_link_text('Use the web app instead'):
                    element.click()
        except TimeoutException:
            k -= 1
            time.sleep(20)
        except ElementNotInteractableException:
            k -= 1
            nist += 1
        except ElementClickInterceptedException:
            k -= 1
            nist += 1
        except NoSuchElementException:
            k -= 1
            time.sleep(10)
        except Exception:
            k = -1
        else:
            break
    if k < 0:
        pass
    else:
        # print(get_discord_message())
        time.sleep(10)
