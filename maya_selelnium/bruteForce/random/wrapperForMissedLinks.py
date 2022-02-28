THREADS = 20

import sys

pagesNotFound = list()
for fname in sys.argv[1:]:
    with open(fname, 'r') as f:
        for line in f:
            if 'NOT FOUND' in line:
                print(line, end='')
                identifier = line.split(' ')[0]
                print(identifier, end='\n')
                pagesNotFound.append(identifier)
            elif 'failed to load' in line:
                print(line, end='')
                identifier = line.split(' ')[5].split('/')[4]
                print(identifier, end='\n')
                pagesNotFound.append(identifier)
        f.close()

print(pagesNotFound)
totalWork = len(pagesNotFound)
print('\n',totalWork,'\n')

#---------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent import futures
import threading
import time
import csv

def customizeOptions():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--log-level=3')
    return options

def customizeCapabilities():
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    return caps

def initializeDriver():
    options = customizeOptions()
    caps = customizeCapabilities()
    driver = webdriver.Chrome(options=options, desired_capabilities=caps, executable_path='C:\\Python\\Drivers\\chromedriver.exe')
    # # driver.maximize_window()
    time.sleep(0.5)
    return driver


def fetchDataFromUrl(driverNumber):

    global csvHandler
    global logFileHandler
    global listLock
    global csvLock
    global logLock

    driver = initializeDriver()
    print('driver', driverNumber, 'initiated')
    workCount = 0

    while True:
        listLock.acquire()
        if len(pagesNotFound) == 0:
            listLock.release()
            break
        identifier = pagesNotFound[0]
        pagesNotFound.pop(0)
        listLock.release()

        url = 'https://maya.com.bd/question/' + identifier
        print('task initiated : fetch from', url)

        try:
            # if the script faces error while trying, retry 9 more times
            for retryCounter in range(0,10):
                try:
                    driver.get(url)
                    driver.implicitly_wait(0.5)  # should be calibrating this according to my net speed
                    break
                except Exception as e:
                    errorMessage = '\nError Loading '+url+'\n'+str(e).strip()+'\nretrying('+str(retryCounter+1)+') ...\n'
                    logFileHandler.writelines(errorMessage)
                    logFileHandler.flush()
                    print(errorMessage)
                    driver.close()
                    time.sleep(5)
                    driver = initializeDriver()

            # this would fail on a 500/404 status_code page
            ques = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/div[2]/a/b').text

            try:
                # tag = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/div[1]/p/a').text
                tagFinder = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/div[1]')
                tagElementList = tagFinder.find_elements_by_tag_name('p')
                tagList = []
                for tagElement in tagElementList:
                    tagName = tagElement.find_elements_by_tag_name('a')[0].text
                    tagList.append(tagName)
                tag = ','.join(tagList)
                if tag == '':
                    tag = 'NO TAG'
            except:
                tag = 'NO TAG'

            try:
                ans = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/div[4]/div/div/p').text
            except:
                ans = 'NO ANS'

            # Write into the csv
            quesAns = {'tag': tag, 'ques': ques, 'ans': ans}
            csvLock.acquire()
            csvHandler.writerow(quesAns)    # writerows -> list of dictionaries, writerow -> dictionary
            csvFileHandler.flush()
            csvLock.release()

            print('task completed. fetched from', url)
            workCount+=1


        except:
            logLock.acquire()
            logFileHandler.writelines(identifier+' NOT FOUND\n')
            logFileHandler.flush()
            logLock.release()
            print('ERROR', url, 'NOT FOUND. task NOT completed !')


    driver.quit()
    print('driver', driverNumber, 'terminated with a workcount of', workCount)

def check():
    count = 0
    with open(csvFileName, 'r', encoding='utf-8') as f:
        for line in f:
            if len(line) > 2:
                count+=1
        f.close()
    print('data collected : ', count-1) # excluding the header
    count = 0
    with open(logFileName, 'r') as f:
        for line in f:
            count+=1
        f.close()
    print('page missed : ', count)

startTime = time.perf_counter()

# Initializing the csv file and writing the headers
keys = ['tag', 'ques', 'ans']
csvFileName = 'wrapper.csv'
csvFileHandler = open(csvFileName,'a',encoding='utf-8',newline='\n')
csvHandler = csv.DictWriter(csvFileHandler, fieldnames = keys)
csvHandler.writeheader()

# Initializing the log file
logFileName = 'wrapper.log'
logFileHandler = open(logFileName,'a')

# creating lock object for each shared resource
# though Rlock is not that much required here
listLock = threading.RLock()
csvLock = threading.RLock()
logLock = threading.RLock()

with futures.ThreadPoolExecutor() as executor:
    driverNumberList = [list(range(0,THREADS))]
    executor.map(fetchDataFromUrl, driverNumberList)

csvFileHandler.close()
logFileHandler.close()

check()

endTime = time.perf_counter()
print('Job done.',totalWork,'in',endTime-startTime,'second(s)')