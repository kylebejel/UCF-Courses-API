import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import string
import time

root_link = "https://www.ucf.edu/catalog/undergraduate/"
base_link = "https://www.ucf.edu/catalog/undergraduate/#/courses?group="
links = ["COP - Computer Programming","CNT - Computer Networks","CIS - Computer and Information Systems","CAP - Computer Applications"]

binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)

soup_bowl = []
atags = []
course_soup_bowl = []
headers = []

fp = open('out.txt', 'w', encoding='utf8')
outlines = []

head_count = 0

for l in links:
    new_link = base_link+l
    driver.get(new_link)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    soup_bowl.append(soup)
    time.sleep(2)

for soup in soup_bowl:
    for a in soup.find_all('h3',class_="style__item___N3dlN"):
        for a2 in a.find_all('a'):
            atags.append(a2.get('href'))

for tag in atags:
    driver.get(root_link + tag)
    time.sleep(5)
    course_html = driver.page_source
    course_soup = BeautifulSoup(course_html,'lxml')
    head = course_soup.find('div',class_="course-view__itemDetailContainer___2tFFK")
    head = head.find('h2')
    headers.append(head.text)
    outlines.append(headers[head_count] + '\n')
    head_count+=1
    for d in course_soup.find_all('div',class_="course-view__pre___2VF54"):
        outlines.append(d.text + '\n')
    outlines.append('\n')

driver.close()
fp.writelines(outlines)
fp.close()
