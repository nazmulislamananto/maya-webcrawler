from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True               # this works
# options.add_argument('--headless')      # this works too
driver3 = webdriver.Chrome(options=options)
# driver3 = webdriver.Chrome()
url = 'https://maya.com.bd/question/0'
for retryCounter in range(0,10):
    try:
        driver3.get(url)
        break
    except Exception as e:
        # print(e)
        # print(type(e))
        print('\nError loading ', url)
        print(str(e).strip())
        print('retrying ('+str(retryCounter+1)+') ...\n')
        driver3.quit()
        time.sleep(5)
        driver3 = webdriver.Chrome(options=options)
# try:
#     ques = WebDriverWait(driver3, 5).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[3]/div[2]/a/b'))
#     )
# except:
#     pass
# print(ques.text)


# tagFinder = driver3.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/div[1]')
# # print(tagFinder)
# tagElementList = tagFinder.find_elements_by_tag_name('p')
# # print(tagElementList)
# tagList = []
# for tagElement in tagElementList:
#     tagName = tagElement.find_elements_by_tag_name('a')[0].text
#     print(tagName)
#     tagList.append(tagName)
# tag = ','.join(tagList)
# if tag == '':
#     tag = 'NO TAG'

# print(tag)

print(driver3.title)

driver3.close()


# tag = list()
# tag.append(driver3.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/div[1]/p[1]/a'))
# tag.append(driver3.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/div[1]/p[2]/a'))



# import requests

# response = requests.get('https://maya.com.bd/question/33')
# # print(response.headers)
# print(response.status_code)

# import datetime
# now = datetime.datetime.now()
# # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# # print("date and time =", dt_string)
# print(str(now)+' maerebap')

# from browsermobproxy import Server
# server = Server('f:\\maya\ webcrawler\\browsermob-proxy-py\\browsermobproxy')
# server.start()
# proxy = server.create_proxy()

# from selenium import webdriver
# profile  = webdriver.ChromeProfile()
# profile.set_proxy(proxy.selenium_proxy())
# driver = webdriver.Chrome(Chrome_profile=profile)


# proxy.new_har("google")
# driver.get("http://www.google.co.uk/")
# proxy.har # returns a HAR JSON blob

# server.stop()
# driver.quit()

# from selenium import webdriver
# import json
# driver = webdriver.PhantomJS(executable_path=r"your_path")
# har = json.loads(driver.get_log('har')[0]['message']) # get the log
# print('headers: ', har['log']['entries'][0]['request']['headers'])

# from selenium import webdriver  # Import from seleniumwire
# import time

# Create a new instance of the Chrome driver
# browserProfile = webdriver.ChromeProfile()
# browserProfile.set_preference('permissions.default.stylesheet', 2)
# browserProfile.set_preference('permissions.default.image', 2)
# browserProfile.set_preference("permissions.default.script", 2)
# browserProfile.set_preference("javascript.enabled", False)
# driver = webdriver.Chrome()

# Go to
# url = 'https://maya.com.bd/question/46578'
# driver.get(url)
# time.sleep(10)

# driver.execute_script('''var queries = ['link[rel=stylesheet][href]', 'style'];
# for (var i = 0; i < queries.length; i++) {
#     var remove = document.querySelectorAll(queries[i]);
#     for (var j = 0; j < remove.length; j++) {
#         remove[j].outerHTML = '';
#     }
# }
# var inline = document.querySelectorAll('*[style]');
# for (var i = 0; i < inline.length; i++) {
#     inline[i].removeAttribute('style');
# }''')



# Access requests via the `requests` attribute
# for request in driver.requests:
#     if request.response:
#         # print(
#         #     request.path,
#         #     request.response.status_code,
#         #     request.response.headers['Content-Type']
#         # )
#         if request.path == url:
#             if request.response.status_code == 200:
#                 print('found')
#                 break
#             else:
#                 print('not found')
#                 break
#             break
