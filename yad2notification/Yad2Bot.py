import project_functions as func
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.firefox.options import Options
import random
import threading

# =====================================================================================


class Yad2Bot(object):

    def __init__(self, url, phone):

        self.count = 0
        self.error = ""
        self.url = ""
        self.phone = phone
        self.posts = []
        self.exit = False
        self.options = Options()
        self.options.headless = True
        self.driver = ""
        self.url = url

    def start_search(self):
        self.driver = webdriver.Firefox(options=self.options)
        t = threading.Thread(target=self.post_notify())
        t.start()

    # Notification about new post in search
    def post_notify(self):
        while True:
            # flag for stoping the thread
            if self.exit:
                print("search stopped")
                break
            else:
                options = Options()
                options.headless = True
                with self.driver as driver:

                    wait = WebDriverWait(driver, 60)

                    # taking the first result
                    while True:
                        try:
                            driver.get(self.url)
                            wait.until(presence_of_element_located((By.ID, "feed_item_0")))
                            i = 0
                            while i < 5:
                                result = driver.find_element_by_css_selector(
                                    "#feed_item_{0} > div:nth-child(1) > div:nth-child(1)".format(i))
                                if "עסקי" in result.text:
                                    i += 1
                                else:
                                    break
                            old = result.text
                            print("old: " + old)
                        except Exception as e:
                            print("Error section 1:{0}".format(e))
                            break

                        # checking for update
                        while True:
                            try:
                                n = random.randint(60, 120)
                                time.sleep(n)
                                driver.refresh()
                                wait.until(presence_of_element_located((By.ID, "feed_item_0")))
                                i = 0
                                # skip adds
                                while i < 5:
                                    result = driver.find_element_by_css_selector(
                                        "#feed_item_{0} > div:nth-child(1) > div:nth-child(1)".format(i))
                                    if "עסקי" in result.text:
                                        i += 1
                                    else:
                                        break
                                new = result.text
                                print("new: " + new)
                                name, price, place = func.stinger(result.text)
                            except Exception as e:
                                print("Error section 2: {0}".format(e))
                                break

                            if new != old:
                                try:
                                    # taking contact name and phone number
                                    driver.refresh()
                                    result = driver.find_element_by_css_selector(
                                        "#feed_item_{0} > div:nth-child(1) > div:nth-child(1)".format(i))
                                    contact, number = func.get_contact(result, driver)
                                    # send massage

                                    func.send_massage(
                                        "מוצר חדש שעלול לעניין אותך נכנס\nהמוצר: {0}\nמיקום: {2}\nמחיר: {1}\nאיש קשר: {4} - {5}\nלצפייה: {3}".format(name, price, place, self.url, contact, number),
                                        self.phone)

                                    print("massage sent")

                                    self.posts.append([name.replace(",", ""), place.replace(",", ""),
                                                       price.replace(",", ""), contact.replace(",", ""),
                                                       number.replace(",", ""), self.url])

                                except Exception as execpt:
                                    print("Error section 3 (massage not sent): {0}".format(execpt))
                                    break
                                break

    # return all new posts found
    def get_all(self):
        return str(self.posts)

    # stop search
    def stop(self):
        self.exit = True
        time.sleep(5)
        try:
            self.driver.close()
        except Exception as e:
            print(e)
# ----------------------------------------------
