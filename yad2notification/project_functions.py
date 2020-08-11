from twilio.rest import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time


# send massage to client
# return True if massage sent
# Error if not
def send_massage(msg, phone):
    account_sid = 'ACd75121056db21981c932136355c6895e'
    auth_token = 'aa348d6120f843f93aca411b9fa7e7fd'
    client = Client(account_sid, auth_token)

    try:
        client.messages.create(
                                      from_='whatsapp:+14155238886',
                                      body=msg,
                                      to='whatsapp:'+phone
                                  )
        return True

    except Exception as e:
        print("Error: {0}".format(e))


# set new clear string
def stinger(string):
    string = string.split("\n")
    if len(string) > 4:
        string.pop(1)
    name = string[0]
    place = string[1]
    price = string[2]
    print(string)
    return name, price, place


# get contact information
def get_contact(result, driver):
    wait = WebDriverWait(driver, 120)
    result.click()
    time.sleep(8)
    span = wait.until(presence_of_element_located((By.CSS_SELECTOR, "#lightbox_contact_seller_0 > span:nth-child(2)")))
    span.click()
    time.sleep(8)
    wait.until(presence_of_element_located((By.ID, "lightbox_phone_number_0")))
    try:
        number = driver.find_element_by_id("lightbox_phone_number_0").text
    except Exception as e:
        number = "number have not found. " + str(e)
        print(number)
    try:
        name = driver.find_element_by_class_name("name").text
    except Exception as e:
        name = "number have not found. " + str(e)
        print(name)

    return name, number
