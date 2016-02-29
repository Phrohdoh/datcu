import os

if 'DATCU_USERNAME' not in os.environ:
    raise Exception('DATCU_USERNAME cannot be unset or empty')

if 'DATCU_PASSWORD' not in os.environ:
    raise Exception('DATCU_PASSWORD cannot be unset or empty')

username = os.environ['DATCU_USERNAME']
password = os.environ['DATCU_PASSWORD']

import json

challenges = None

with open('challenges.json', 'r') as fo:
    challenges = json.load(fo)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from seleniumrequests import PhantomJS

p = PhantomJS(service_log_path=os.path.devnull)
p.set_window_size(1440, 900)
p.get('https://www.mydatcu.org/User/AccessSignin/Start')
p.find_element_by_name('UsernameField').send_keys(username + Keys.RETURN)
p.find_element_by_name('PasswordField').send_keys(password + Keys.RETURN)

# NOTE: This will obviously break if the site ever changes layout
challenge_xpath = "id('AccessForm')/div/div[1]/div[2]/table/tbody/tr[2]/td[2]"

while p.current_url == 'https://www.mydatcu.org/User/AccessSignin/Challenge':
    text = p.find_elements_by_xpath(challenge_xpath)
    if not text:
        raise Exception('No results found!')

    text = text[0].text.replace('explain', '').strip()
    if text not in challenges:
        raise Exception("Question '%s' is unanswered!" % text)

    p.find_element_by_name('Answer').send_keys(challenges[text] + Keys.RETURN)

# All Transactions
p.find_elements_by_xpath("id('MasterHeaderMenuSub')/a[3]")[0].click()

# Options
p.find_elements_by_xpath("id('MasterMain')/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td/span[1]")[0].click()

# Options > Download as CSV
r = p.request('GET', 'https://www.mydatcu.org/User/MainTransactions/List?csv=true')
if r.status_code != 200:
    raise Exception('Could not GET https://www.mydatcu.org/User/MainTransactions/List?csv=true')

with open('test.csv', 'w') as fo:
    fo.write(r.text)
    print("Wrote to test.csv")
