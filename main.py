import xlsparser
import scrapper
import logging as logger
from os import rename
import os
from dotenv import load_dotenv

load_dotenv()
logger.basicConfig(format='%(levelname)s %(module)s %(message)s', level=logger.DEBUG)

# Change logging level for some verbose modules
for module in ['selenium.webdriver.remote.remote_connection', 'selenium', 'urllib3.connectionpool']:
    logger.getLogger(module).setLevel(logger.INFO)

xls = scrapper.scrape_xlsx()

with open('new_edt.xlsx', 'wb') as file:
    file.write(xls)
    UES = 'gs11, gs15, gs21, gs16'
    calendar = xlsparser.make_ics(xls, UES)
    name = 'alt'
    print ("Y")

    with open(f'calendars/ssi-{name}.ics', 'w') as file:
        logger.info(f'Write on calendars/{name}.ics')
        file.write(calendar)
