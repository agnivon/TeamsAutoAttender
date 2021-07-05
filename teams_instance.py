# import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import time
from datetime import datetime
# from multiprocessor import get_discord_message
from image_processor import check_present_msg
from LOCATORS import *
import os
from logger import ActivityLogger

opt = Options()
opt.add_argument("--headless")
opt.add_argument("--mute-audio")
opt.add_argument("--disable-infobars")
opt.add_argument("--window-size=1920,1080")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})

URL = "https://teams.microsoft.com"
gen_mapping = {'class 6A SS': 'ma\'am', 'CV-18CV653-OSHA-6th SEM (CSE, ECE, CH, AE & AS)': 'sir', '6A Web': 'ma\'am',
               'CGV- VI A Section': 'sir', 'CGV Lab- VI A Section': 'sir', '6th Sem_DMDW_18CS641': 'ma\'am',
               '6 SEM MAD LAB': 'ma\'am'}
alt_mapping = {'6A Web': '6A AND 6B Web'}


class TeamsInstance:
    def __init__(self, ign, email, passwd, att_token):
        self.logger = ActivityLogger(ign + ' instance')
        self.driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=opt,
                                       service_log_path='NUL')
        # driver = webdriver.Chrome(chrome_options=opt,service_log_path='NUL')
        self.ign = ign
        self.attendance_token = att_token
        self.creds = {'email': email, 'passwd': passwd}
        self.logger.log_event_info("{} teams instance created".format(self.ign))

    def find_element(self, locator, locator_type='xpath', element_name='Element'):
        logger = self.logger
        driver = self.driver
        element = None
        try:
            element = None
            if locator_type == 'xpath':
                element = driver.find_element_by_xpath(locator)
            elif locator_type == 'cname':
                element = driver.find_element_by_class_name(locator)
            elif locator_type == 'css':
                element = driver.find_element_by_css_selector(locator)
        except NoSuchElementException as e:
            logger.log_event_error('{} click intercepted.'.format(element_name), e)
            self.screenshot('Error', '{}-{}'.format(element_name, 'NoSuchElementException'))
        except Exception as e:
            logger.log_event_error('Exception Occured for element {}'.format(element_name), e)
            self.screenshot('Error', '{}-{}'.format(element_name, 'Exception'))
        finally:
            return element

    def click_element(self, locator, locator_type='xpath', element_name='Element', tries=1, retry_interval=0):
        logger = self.logger
        while tries > 0:
            try:
                element = self.find_element(locator, locator_type, element_name)
                if not element:
                    tries -= 1
                    continue
                element.click()
            except ElementNotInteractableException as e:
                logger.log_event_error('{} not interactable.'.format(element_name), e)
                self.screenshot('Error', '{}-{}'.format(element_name, 'ElementNotInteractableException'))
            except ElementClickInterceptedException as e:
                logger.log_event_error('{} click intercepted.'.format(element_name), e)
                self.screenshot('Error', '{}-{}'.format(element_name, 'ElementClickInterceptedException'))
            except StaleElementReferenceException as e:
                logger.log_event_error('{} is stale.'.format(element_name), e)
                self.screenshot('Error', '{}-{}'.format(element_name, 'StaleElementReferenceException'))
            except Exception as e:
                logger.log_event_error('Exception Occured for element {}'.format(element_name), e)
                self.screenshot('Error', '{}-{}'.format(element_name, 'StaleElementReferenceException'))
            else:
                break
            tries -= 1
            time.sleep(retry_interval)
            if tries <= 0:
                return False
        return True

    def login(self):
        driver = self.driver
        creds = self.creds
        logger = self.logger
        k = 3
        nist = 3  # Not Interactable Sleep Time
        while k >= 0:
            try:
                driver.get(URL)
                WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
                logger.log_event_info('Navigated to webpage')

                if "login.microsoftonline.com" in driver.current_url:
                    # login required
                    logger.log_event_info("Logging in")
                    email_field = driver.find_element_by_xpath(EMAIL_FIELD)
                    # email_field.click()
                    email_field.send_keys(creds['email'])
                    logger.log_event_info('Entered email')
                    time.sleep(nist)
                    driver.find_element_by_xpath(EMAIL_NEXT_BUTTON).click()  # Next button
                    time.sleep(nist)
                    password_field = driver.find_element_by_xpath(PASSWD_FIELD)
                    password_field.click()
                    password_field.send_keys(creds['passwd'])
                    logger.log_event_info('Entered password')
                    time.sleep(1)
                    driver.find_element_by_xpath(SIGNIN_BUTTON).click()  # Sign in button
                    time.sleep(1)
                    driver.find_element_by_xpath(REM_LOGIN_BUTTON).click()  # remember login
                    time.sleep(1)
                    for element in driver.find_elements_by_link_text('Use the web app instead'):
                        element.click()
            except TimeoutException as e:
                logger.log_event_error('Operation timed out. Retrying. {} atempts left'.format(k))
                logger.logger.exception(e)
                k -= 1
                time.sleep(20)
            except Exception as e:
                logger.log_event_error('Exception Occured')
                logger.logger.exception(e)
                k = -1
            else:
                break
        if k < 0:
            logger.log_event_error('Failed login. Terminating login proceedure')
        else:
            # print(get_discord_message())
            time.sleep(10)
            logger.log_event_info('Successfully logged in')
            self.take_screenshot('Images/Test/{}-login.png'.format(self.ign))
        return

    # noinspection PyUnusedLocal
    def join_class(self, class_name, start_time, end_time):
        driver = self.driver
        logger = self.logger
        discord_message = lambda status: (self.ign, class_name, status, start_time, end_time)

        k = 3
        while k >= 0:
            try:
                channel_found = False
                time.sleep(10)
                classes_available = driver.find_elements_by_class_name("name-channel-type")
                for channel in classes_available:
                    if class_name.lower() in channel.get_attribute('innerHTML').lower().replace('amp;', ''):
                        channel.click()
                        channel.click()
                        logger.log_event_info('Attempting to join {} class'.format(class_name))
                        channel_found = True
                        break
                if not channel_found:
                    raise NoSuchElementException('Channel not found')
                time.sleep(5)
                # self.take_screenshot("before_join.jpg")
                joinbtn = driver.find_element_by_class_name("ts-calling-join-button")
                joinbtn.click()

            except NoSuchElementException as e:
                # join button not found
                # refresh every minute until found
                self.take_screenshot('Images/Test/{}-phase1.png'.format(self.ign))
                logger.log_event_error('Join button or channel not found. Retrying. {} attempts left'.format(k))
                logger.logger.exception(e)
                k -= 1
                driver.refresh()
                time.sleep(10)
            except ElementNotInteractableException as e:
                self.take_screenshot('Images/Test/{}-phase1.png'.format(self.ign))
                logger.log_event_error('Join button or channel not interactable. Retrying. {} attempts left'.format(k))
                logger.logger.exception(e)
                k -= 1
            except NoSuchWindowException as e:
                self.take_screenshot('Images/Test/{}-phase1.png'.format(self.ign))
                logger.log_event_error('Window not found. Retrying. {} attempts left'.format(k))
                logger.logger.exception(e)
                driver.refresh()
                k -= 1
            except Exception as e:
                self.take_screenshot('Images/Test/{}-phase1.png'.format(self.ign))
                logger.log_event_error('Exception Occured. Retrying. {} attempts left'.format(k))
                logger.logger.exception(e)
                driver.refresh()
                time.sleep(10)
                k -= 1
            else:
                break
        if k < 0:
            logger.log_event_error('Failed to join {} class. Terminating join proceedure'.format(class_name),
                                   discord=discord_message("Failed"))
            if class_name in alt_mapping:
                self.join_class(alt_mapping[class_name], start_time, end_time)
            return

        time.sleep(5)
        k = self.final_join_proc()

        if k < 0:
            logger.log_event_error('Failed to join {} class. Terminating join proceedure'.format(class_name),
                                   discord=discord_message("Failed"))
            return
        else:
            logger.log_event_info('Class {} joined successfully'.format(class_name),
                                  discord=discord_message("Joined"))
            status_check = 0
            for tries in range(3):
                time.sleep(10)
                status_check = len(driver.find_elements_by_xpath(CHAT_BUTTON))
                if status_check:
                    break
            logger.log_event_info('0: Maybe Lobby 1: Joined:-{}'.format(status_check), discord=discord_message(status_check))

        self.leave_class(class_name, start_time, end_time)
        return

    def leave_class(self, class_name, start_time, end_time):
        # now schedule leaving class
        driver = self.driver
        logger = self.logger
        '''
        cross_button = driver.find_elements_by_css_selector(MIC_MUTED_CROSS)
        if cross_button:
            cross_button[0].click()
        '''
        time.sleep(10)
        self.take_screenshot('Images/Test/{}-class.png'.format(self.ign))
        discord_message = lambda status: (self.ign, class_name, status, start_time, end_time)
        tmp = "%H:%M"
        class_running_time = (datetime.strptime(end_time, tmp) - datetime.now()).seconds
        # self.screenshot_recon_suspend(class_running_time, class_name)
        # window = random.randint(180, 240)
        # self.simple_suspend(class_running_time, class_name, window)
        window1 = 420
        window2 = 180
        posted = self.attendance_suspend(class_running_time - window2, class_name, window1)
        if not posted:
            time1 = time.time()
            attendance_message = '{} {}'.format('1MJ18CS010 present', gen_mapping.get(class_name, ''))
            self.post_message(attendance_message)
            time2 = time.time()
            seconds = window2 - (time2 - time1)
        else:
            seconds = window2
        self.enter_sleep(seconds, 'final')

        k = 2
        while k >= 0:
            try:
                # driver.find_element_by_class_name("ts-calling-screen").click()
                driver.find_element_by_xpath(TEAMS_BUTTON).click()  # come back to homepage
                time.sleep(1)
                driver.find_element_by_xpath(HANGUP_BUTTON).click()
            except ElementNotInteractableException as e:
                logger.log_event_error('Element not interactable. {} attempts left'.format(k))
                logger.logger.exception(e)
                k -= 1
                time.sleep(3)
            except NoSuchElementException as e:
                logger.log_event_error('Element does not exist')
                logger.logger.exception(e)
                k = -1
            except NoSuchWindowException as e:
                logger.log_event_error('Window not found. Retrying. {} attempts left'.format(k))
                logger.logger.exception(e)
                driver.refresh()
                k = -1
            except Exception as e:
                logger.log_event_error("Exception Occured")
                logger.logger.exception(e)
                k = -1
            else:
                break

        if k < 0:
            driver.refresh()
        logger.log_event_info('Class {} left'.format(class_name), discord=discord_message("Left"))
        # print(discord_message("Left"))
        return

    def final_join_proc(self, k=3, rejoin=0):
        driver = self.driver
        logger = self.logger
        while k >= 0:
            try:
                if rejoin:
                    driver.find_element_by_xpath(REJOIN_BUTTON).click()
                    time.sleep(2)
                continue_button = driver.find_elements_by_css_selector(CONTINUE_BUTTON)
                if continue_button:
                    continue_button[0].click()
                time.sleep(1)
                webcam = driver.find_element_by_xpath(WEBCAM_TOGGLE)
                if webcam.get_attribute('title') == 'Turn camera off':
                    webcam.click()
                    logger.log_event_info('Turned camera off')
                time.sleep(1)

                microphone = driver.find_element_by_xpath(MIC_TOGGLE)
                if microphone.get_attribute('title') == 'Mute microphone':
                    microphone.click()
                    logger.log_event_info('Turned microphone off')
                time.sleep(1)

                joinnowbtn = driver.find_element_by_xpath(JOIN_NOW_BUTTON)
                joinnowbtn.click()
            except ElementNotInteractableException as e:
                self.take_screenshot('Images/Test/{}-phase2.png'.format(self.ign))
                logger.log_event_error('Element not interactable. {} attempts left'.format(k))
                logger.logger.exception(e)
                k -= 1
                time.sleep(5)
            except NoSuchElementException as e:
                self.take_screenshot('Images/Test/{}-phase2.png'.format(self.ign))
                # self.take_screenshot("join.jpg")
                logger.log_event_error('Element does not exist')
                logger.logger.exception(e)
                k -= 1
            except Exception as e:
                self.take_screenshot('Images/Test/{}-phase2.png'.format(self.ign))
                logger.log_event_error('Exception Occured')
                logger.logger.exception(e)
                k = -1
            else:
                break
        return k

    def discord_attendance_prompt(self, class_running_time):
        while class_running_time:
            message = ''
            if message:
                self.post_message(message)
                break
            time.sleep(0.5)
            class_running_time -= 0.5

    def simple_suspend(self, class_running_time, class_name, window=60):
        logger = self.logger
        if window >= class_running_time:
            return
        logger.log_event_info('Entering simple sleep')
        time.sleep(class_running_time - window)
        logger.log_event_info('Waking up. Posting in {} class'.format(class_name))
        start_time = time.time()
        attendance_message = '{} {}'.format('1MJ18CS010 present', gen_mapping.get(class_name, ''))
        self.post_message(attendance_message)
        end_time = time.time()
        logger.log_event_info('Entering final simple sleep')
        seconds = window - (end_time - start_time)
        if seconds > 0:
            time.sleep(seconds)
        logger.log_event_info('Waking up from simple sleep')

    def screenshot_recon_suspend(self, class_running_time, class_name, window=600, freq=15):
        logger = self.logger
        driver = self.driver
        if window >= class_running_time:
            return
        self.enter_sleep(class_running_time - window, 'initial')
        self.logger.log_event_info('Starting screenshot recon')
        seconds = window
        try:
            user_img_dir = 'Images/{}/Recon/{}'.format(self.ign, class_name)
            if not os.path.isdir(user_img_dir):
                os.makedirs(user_img_dir)
            self.take_screenshot('Images/Test/{}-screcon.png'.format(self.ign))
            driver.find_element_by_xpath(CHAT_BUTTON).click()
            while seconds > 0:
                current_time = datetime.now().isoformat()
                filename = '{}-{}.png'.format(class_name, current_time)
                self.take_screenshot(os.path.join(user_img_dir, filename))
                logger.log_event_debug('Screenshot {} recorded'.format(filename))
                if seconds >= freq:
                    seconds -= freq
                    time.sleep(freq)
                else:
                    break
            driver.find_element_by_xpath(CHAT_BUTTON).click()
        except ElementNotInteractableException as e:
            logger.log_event_error('Chat button not interactable.')
            logger.logger.exception(e)
        except NoSuchElementException as e:
            logger.log_event_error('Chat button does not exist')
            logger.logger.exception(e)
        except Exception as e:
            logger.log_event_error("Chat button Exception Occured")
            logger.logger.exception(e)
        finally:
            if seconds > 0:
                self.enter_sleep(seconds, 'intermediate')
        return

    def attendance_suspend(self, class_running_time, class_name, window=600, freq=15):
        logger = self.logger
        # driver = self.driver
        if window >= class_running_time:
            return
        self.enter_dis_sleep(class_running_time - window, 'initial')
        logger.log_event_info('Starting attendance scan')
        seconds = window
        posted = False
        try:
            user_img_dir = 'Images/{}/AttSShots'.format(self.ign)
            if not os.path.isdir(user_img_dir):
                os.makedirs(user_img_dir)
            self.click_chat_button()
            filename = '{}-screenshot-attscn.png'.format(class_name)
            filepath = os.path.join(user_img_dir, filename)
            while seconds > 0:
                # current_time = datetime.now().isoformat()
                self.take_screenshot(filepath)
                logger.log_event_debug('Attendance Scan Screenshot {} recorded'.format(filename))
                start_time = time.time()
                check_status, pick, Mpy = check_present_msg(filepath, 1)
                img_proc_time = time.time() - start_time
                if check_status:
                    logger.log_event_info('{} Attendance detected'.format(class_name))
                    start_time = time.time()
                    attendance_message = '{} {}'.format('1MJ18CS010 present', gen_mapping.get(class_name, ''))
                    posted = self.post_message(attendance_message, 0)
                    posting_time = time.time() - start_time
                    total_time = img_proc_time + posting_time
                    if total_time <= seconds:
                        seconds -= total_time
                    posted = True
                    break
                if seconds >= freq:
                    seconds -= freq
                    if img_proc_time <= freq:
                        time.sleep(freq - img_proc_time)
                else:
                    break
            # driver.find_element_by_xpath(CHAT_BUTTON).click()
            self.click_chat_button()
            '''for f in os.listdir(user_img_dir):
                os.remove(os.path.join(user_img_dir, f))'''
        except ElementNotInteractableException as e:
            logger.log_event_error('Chat button not interactable.')
            logger.logger.exception(e)
        except NoSuchElementException as e:
            logger.log_event_error('Chat button does not exist')
            logger.logger.exception(e)
        except Exception as e:
            logger.log_event_error("Chat button Exception Occured")
            logger.logger.exception(e)
        finally:
            if seconds > 0:
                self.enter_sleep(seconds, 'intermediate')
        return posted

    def post_message(self, message, chat_button_use=1):
        driver = self.driver
        logger = self.logger
        posted = False
        try:
            self.take_screenshot('Images/Test/{}-msgpost1.png'.format(self.ign))
            # webdriver.ActionChains(driver).move_to_element(chat_button).perform()
            if chat_button_use:
                self.click_chat_button()
            time.sleep(1)
            chatbox_field = driver.find_element_by_css_selector(CHATBOX_FIELD)
            for i in range(3):
                try:
                    chatbox_field.click()
                except ElementClickInterceptedException:
                    time.sleep(1)
                else:
                    break
            chatbox_field.send_keys(message)
            self.take_screenshot('Images/Test/{}-msgpost2.png'.format(self.ign))
            try:
                driver.find_element_by_xpath(CHATBOX_SEND).click()
            except ElementClickInterceptedException:
                chatbox_field.send_keys(Keys.ENTER)
            time.sleep(1)
            logger.log_event_info('Message posted')
            self.take_screenshot('Images/Test/{}-msgpost3.png'.format(self.ign))
            if chat_button_use:
                self.click_chat_button()
            self.take_screenshot('Images/Test/{}-msgpost4.png'.format(self.ign))
            posted = True
        except ElementNotInteractableException as e:
            logger.log_event_error('Element not interactable.')
            logger.logger.exception(e)
        except NoSuchElementException as e:
            logger.log_event_error('Element does not exist')
            logger.logger.exception(e)
        except Exception as e:
            logger.log_event_error("Exception Occured")
            logger.logger.exception(e)
        return posted

    def enter_sleep(self, seconds, phase=''):
        self.logger.log_event_info('Entering {} sleep'.format(phase))
        time.sleep(seconds)
        self.logger.log_event_info('Waking up from {} sleep'.format(phase))

    def enter_dis_sleep(self, seconds, phase='', freq=15):
        self.logger.log_event_info('Entering {} sleep'.format(phase))
        while seconds > 0:
            start_time = time.time()
            rejoin_button = self.driver.find_elements_by_xpath(REJOIN_BUTTON)
            if rejoin_button:
                self.final_join_proc(rejoin=1)
            end_time = time.time()
            total_time = end_time - start_time
            if freq <= seconds:
                if freq >= total_time:
                    seconds -= freq
                    time.sleep(freq - total_time)
                else:
                    if total_time <= seconds:
                        seconds -= total_time
                    else:
                        seconds = 0
                        break
            else:
                if total_time <= seconds:
                    seconds -= total_time
                break
        if seconds > 0:
            time.sleep(seconds)
        self.logger.log_event_info('Waking up from {} sleep'.format(phase))

    def click_chat_button(self):
        driver = self.driver
        logger = self.logger
        success = False
        try:
            self.take_screenshot('Images/Test/{}-chat_button.png'.format(self.ign))
            driver.find_element_by_xpath(CHAT_BUTTON).click()
            '''chat_button = driver.find_elements_by_xpath(CHAT_BUTTON)
            if chat_button:
                chat_button[0].click()
            else:
                driver.find_element_by_xpath(TEAMS_BUTTON).click()
                driver.find_element_by_xpath(CALLING_MONITOR).click()
                driver.find_element_by_xpath(CHAT_BUTTON).click()'''
            success = True
        except ElementNotInteractableException as e:
            logger.log_event_error('Element not interactable.')
            logger.logger.exception(e)
        except NoSuchElementException as e:
            logger.log_event_error('Element does not exist')
            logger.logger.exception(e)
        except ElementClickInterceptedException as e:
            logger.log_event_error('Element click intercepted.')
            logger.logger.exception(e)
        except Exception as e:
            logger.log_event_error("Exception Occured")
            logger.logger.exception(e)
        return success

    def take_screenshot(self, filepath, enabled=1):
        if enabled:
            self.driver.save_screenshot(filepath)

    def screenshot(self, foldername, filename):
        filepath = os.path.join(self.ign, foldername)
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        self.driver.save_screenshot(os.path.join(filepath, filename))

    def kill(self):
        self.driver.quit()
