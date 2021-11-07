# import libraries
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import urllib.request
import csv
import os

#next
def scrape_xlsx() :
    #emulate a login
    print(os.environ['ENT_USERNAME'])
    if(os.environ.get('COMMAND_EXECUTOR') is None):
        exit(-2)
    driver = webdriver.Remote(command_executor=os.environ['COMMAND_EXECUTOR'],
                              desired_capabilities=DesiredCapabilities.CHROME)
    driver.get('https://cas.utt.fr/cas/login?service=https%3A%2F%2Fmoodle.utt.fr%2Flogin%2Findex.php%3FauthCAS%3DCAS')

    # Fill the login form
    username = driver.find_element_by_id('username')
    username.send_keys(os.environ['ENT_USERNAME'])
    password = driver.find_element_by_id('password')
    password.send_keys(os.environ['ENT_PASSWORD'])
    submit = driver.find_element_by_class_name('btn-submit')
    submit.click()
    driver.set_page_load_timeout(30)

    # logger.debug('Callback fully loaded, get session cookies and quit')
    cookies = driver.get_cookies()
    print (cookies)
    driver.quit()

    # Starting a session
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    #TLS-Error ignore
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    response = session.get('https://moodle.utt.fr/course/view.php?id=1631', allow_redirects=True)
    # Find the link attributed to the schedule
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find(text="Emploi du temps M2 SSI").parent.parent['href']


    # Retrieve the file content
    response = session.get(f'{link}&redirect=1', allow_redirects=True)
    return response.content

if __name__ == '__main__':
    xlsx = scrape_xlsx()

    with open('new_edt.xlsx', 'wb') as file:
        file.write(xlsx)
