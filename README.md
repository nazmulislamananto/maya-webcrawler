# Maya WebCrawler  

A webcrawler to crawl [Maya Apa](https://maya.com.bd/) and fetch Question and Answers with appropriate tags all in a CSV. It already has fetched from ques 0 to 60,000. You want to crawl more? Do this -

### Run  

`./maya_selenium/bruteForce/dataCollect.py startingIdentifier endingIdentifier numberOfThreadsPreferred`

### Prerequisites  

chromedriver, google chrome, selenium module

### Keep in mind  

Number of threads should be kept under 12 because ThreadPoolExecutor
isn't allowing to run more than 12 drivers simultaneously. May be this was just my machine and won't be a problem on a different machine.

### Tools

You can connect multiple CSVs into one using `./maya_selelnium\bruteForce\tools\csvFileAttacher.py`  

### Wrapper  

`./maya_selelnium\bruteForce\wrapper\wrapper.py` wraps the whole functionality of `dataCollect.py` into one. Might have to hard code values rather than passing them as command line arguments while using this.