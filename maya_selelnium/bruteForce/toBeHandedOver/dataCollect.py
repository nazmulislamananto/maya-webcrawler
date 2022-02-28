# ./dataCollect.py startingIdentifier endingIdentifier numberOfThreadsPreferred

# prerequisites :
# chromedriver, google chrome, selenium module
# number of threads should be kept under 12 because ThreadPoolExecutor
# isn't allowing to run more than 12 drivers simultaneously.
# may be this won't be a problem on a different machine

CHROME_DRIVER_EXE_PATH = 'C:\\Python\\Drivers\\chrome\\chromedriver.exe'

import sys
try:
    START = int(sys.argv[1])
    END = int(sys.argv[2])
    THREADS = int(sys.argv[3])
except:
    START = 600001
    END = 700000
    THREADS = 12

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from concurrent import futures
import threading
import time
import csv

def customizeOptions():
    options = Options()
    # options.headless = True               # this works
    options.add_argument('--headless')      # this works too
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--log-level=3')

    return options

def customizeCapabilities():
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True

    return caps

def initializeDriver():
    # Initializing the Chrome headless browser
    options = customizeOptions()
    caps = customizeCapabilities()
    driver = webdriver.Chrome(options=options, desired_capabilities=caps, executable_path=CHROME_DRIVER_EXE_PATH)
    # driver.maximize_window()

    # Initializing the PhantomJS browser
    # driver = webdriver.PhantomJS(executable_path='C:\\Python\\Drivers\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    # driver.set_window_size(1120, 550)
    # phantomJS e jhamela ase dekhi

    return driver


def fetchData(arguments):
    start, end = arguments
    if end > END: end = END
    print('task initiated : crawl from ',start,'to',end,'(',end+1-start,')')

    global csvHandler
    global logFileHandler
    global csvLock
    global logLock

    driver = initializeDriver()

    for i in range(start, end+1):
        
        try:

            url = 'https://maya.com.bd/question/' + str(i)

            # retry 10 times in case of a network error
            for retryCounter in range(0,10):
                try:
                    driver.get(url)
                    break
                except Exception as e:
                    errorMessage = '\n'+str(i)+' NETWORK ERROR\n'+str(e).strip()+'\nretrying('+str(retryCounter+1)+') ...\n'
                    logFileHandler.writelines(errorMessage)
                    logFileHandler.flush()
                    print(errorMessage)

            # if the page doesn't exist
            if 'Error' in driver.title:
                
                # Log the exception
                logLock.acquire()
                logFileHandler.writelines(str(i)+' NOT FOUND\n')
                logFileHandler.flush()
                logLock.release()
                print('\n'+str(i)+' NOT FOUND\n')
                continue

            # if the page exists
            else:
                
                # this would wait for 10 seconds before throwing an exception
                quesElem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[3]/div[2]/a/b')))
                ques = quesElem.text
                # print('ques element detected on', i)

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

                print(i)

        except:

            # Log the exception
            logLock.acquire()
            logFileHandler.writelines(str(i)+' NOT FOUND UNKNOWN ERROR\n')
            logFileHandler.flush()
            logLock.release()
            print(i, ' NOT FOUND UNKNOWN ERROR')

        # reload the window after every 30 requests
        # otherwise the program will run out of memory
        if i%30 == 0:
            driver.close()
            if i != end:
                time.sleep(5)
                driver = initializeDriver()

    driver.quit()
    print('task completed. crawled from ',start,'to',end,'(',end+1-start,')')

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
    print('pages could not fetch : ', count)

startTime = time.perf_counter()

# Initializing the csv file and writing the headers
keys = ['tag', 'ques', 'ans']
csvFileName = 'dataFrom'+str(START)+'to'+str(END)+'.csv'
csvFileHandler = open(csvFileName,'a',encoding='utf-8',newline='\n')
csvHandler = csv.DictWriter(csvFileHandler, fieldnames = keys)
csvHandler.writeheader()

# Initializing the log file
logFileName = 'historyFrom'+str(START)+'to'+str(END)+'.log'
logFileHandler = open(logFileName,'a')

# creating lock object for each shared resource
# though Rlock is not that much required here
# a simple Lock would suffice
csvLock = threading.RLock()
logLock = threading.RLock()

# start given number (+1) of threads
with futures.ThreadPoolExecutor() as executor:
    eachThread = int((END-START+1)/THREADS)
    ranges = [(x, x+eachThread-1) for x in range(START, END+1, eachThread)]
    executor.map(fetchData, ranges)

csvFileHandler.close()
logFileHandler.close()

check()

endTime = time.perf_counter()
print('Job done.',START,'to',END,'in',endTime-startTime,'second(s)')