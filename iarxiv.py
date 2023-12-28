from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import os
from datetime import datetime

from credentials_iarxiv import *
from dir_info import *
from date_info import *

wait_time = 20  # sec, wait for this long before pulling the abstracts
score_min = 0.15  # ignore papers below this score as they are likely less interesting

from_date = today
to_date = today

# The login URL
login_url = 'https://iarxiv.org/login'
savedir = datadir + today + '/txt/'

username_field_id = 'email'
password_field_id = 'password'

browser = webdriver.Firefox()
browser.get(login_url)

# content_login = browser.page_source
# print(content_login)

# Find the username field and enter the username
username_field = browser.find_element(By.NAME, username_field_id)
username_field.send_keys(username)

# Find the password field and enter the password
password_field = browser.find_element(By.NAME, password_field_id)
password_field.send_keys(password)

# Find the login button and click it
login_button = browser.find_element(By.XPATH, "//button[text()='Login']")
login_button.click()

time.sleep(wait_time)  # wait for the website to respond

if today != datetime.today().strftime('%Y-%m-%d'):
    # a different date than the default one
    date_fields = browser.find_elements(By.CLASS_NAME, 'input')

    from_date_field = date_fields[0]
    to_date_field = date_fields[1]

    from_date_field.clear()
    from_date_field.send_keys(from_date.replace('-', '/'))
    to_date_field.clear()
    to_date_field.send_keys(from_date.replace('-', '/'))

    search_button = browser.find_element(By.CLASS_NAME, 'button')
    search_button.click()

    time.sleep(wait_time)  # wait for the website to respond

content = browser.page_source
soup = BeautifulSoup(content, 'html.parser')

# identify each paper block
paper_blocks = soup.find_all('div', class_='paper-content')


def find_char_in_string(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


if len(paper_blocks) < 1:  # zero papers
    print('no papers on this date. Please enter a different date!')
    exit()

if not os.path.exists(savedir):
    os.makedirs(savedir, exist_ok=True)
    
ipaper = 0
for block in paper_blocks:
    score = float(block['affinity'])   # this is the score for this paper
    if score < score_min:
        break
    # Extract the title
    title_tag = block.find('h3', class_='paper-title')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    # print("Title:", title)

    # Iterate to find the next 'span' tags without a 'class'
    next_span = title_tag.find_next('span')
    while next_span.has_attr('class'):
        next_span = next_span.find_next('span')
    authors = next_span.get_text(strip=True).split(' - ')
    # note: authors is a list of strings

    # find the abstract
    abstract_div = block.find('div', class_='paper-abstract')
    abstract = abstract_div.get_text(strip=True) if abstract_div else "No abstract found"
    # replace "8×105" with '8*10^5'
    abstract = abstract.replace('\u00D7' + '10', '*10^').replace('\n', ' ')

    ipaper += 1
    with open(savedir + '%03d' % ipaper + '.txt', 'w') as f:
        f.write('title: ' + title + '\n')
        # only include the first <=2 authors
        f.write('authors: ' + ', '.join(authors[:2]) + '\n')
        f.write('abstract: ' + abstract + '\n')

print('Successfully pulled %d papers above score %.3f!' % (ipaper, score_min))
browser.quit()
