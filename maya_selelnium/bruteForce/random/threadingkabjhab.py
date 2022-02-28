START = 301201
END = 301300
THREADS = 10

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--log-level=3')

    return options

def customizeCapabilities():
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True

    return caps

def initializeDriver():
    # Initializing the browser
    options = customizeOptions()
    caps = customizeCapabilities()
    driver = webdriver.Chrome(options=options, desired_capabilities=caps, executable_path='C:\\Python\\Drivers\\chromedriver.exe')
    # # driver.maximize_window()
    # time.sleep(0.5)

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

        url = 'https://maya.com.bd/question/' + str(i)

        try:
            # if the script faces error while trying, retry 9 more times
            for retryCounter in range(0,10):
                try:
                    driver.get(url)
                    # driver.implicitly_wait(0.5)  # should be calibrating this according to my net speed
                    break
                except Exception as e:
                    errorMessage = '\nError Loading '+url+'\n'+str(e).strip()+'\nretrying('+str(retryCounter+1)+') ...\n'
                    logFileHandler.writelines(errorMessage)
                    logFileHandler.flush()
                    print(errorMessage)
                    driver.close()
                    time.sleep(2)
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

            # Log the result
            logLock.acquire()
            logFileHandler.writelines(str(i)+'\n')
            logFileHandler.flush()
            logLock.release()
            print(i)


        except:
            logLock.acquire()
            logFileHandler.writelines(str(i)+' NOT FOUND'+'\n')
            logFileHandler.flush()
            logLock.release()
            print(i, ' NOT FOUND')

        # reload the window after every 50 requests
        # otherwise the program will run out of memory
        if i%30 == 0:
            driver.close()
            if i != end:
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
    print('page crawled : ', count)

startTime = time.perf_counter()

# Initializing the csv file and writing the headers
keys = ['tag', 'ques', 'ans']
csvFileName = 'dataFrom'+str(START)+'to'+str(END)+'.csv'
# csvFileName = 'ques_and_ans.csv'
csvFileHandler = open(csvFileName,'a',encoding='utf-8',newline='\n')
csvHandler = csv.DictWriter(csvFileHandler, fieldnames = keys)
csvHandler.writeheader()

# Initializing the log file
logFileName = 'historyFrom'+str(START)+'to'+str(END)+'.log'
# logFileName = 'bruteForceQuesAns.log'
logFileHandler = open(logFileName,'a')

# creating lock object for each shared resource
# though Rlock is not that much required here
csvLock = threading.RLock()
logLock = threading.RLock()

with futures.ThreadPoolExecutor() as executor:
    eachThread = int((END-START+1)/THREADS)
    ranges = [(x, x+eachThread-1) for x in range(START, END+1, eachThread)]
    executor.map(fetchData, ranges)

csvFileHandler.close()
logFileHandler.close()

check()

endTime = time.perf_counter()
print('Job done.',START,'to',END,'in',endTime-startTime,'second(s)')