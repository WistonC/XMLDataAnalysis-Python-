import threading
import time
import urllib
import xml.dom.minidom
from urllib import request
from urllib.error import HTTPError

class RequestThread(threading.Thread):
    def __init__(self, name, delay, article_titles, api_key):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay
        self.article_titles = article_titles
        self.api_key = api_key

    def run(self):
        print("Starting Thread：" + self.name)
        get_data_from_url(self.name, self.delay, self.article_titles, self.api_key)
        print(self.name + " completed!")


def get_data_from_url(thread_name, delay, articles, api_key):
    # Initialize URL and header
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='
    header_list = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0'},
                   {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'},
                   {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00'}, {
                       'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}]
    i = 0
    while i < len(articles):
        time.sleep(delay)
        article_titles = articles[i].getElementsByTagName("ArticleTitle")[0]
        pm_id = articles[i].getElementsByTagName("PMID")[0]
        # Replace space by + for HTTP request
        url_title = article_titles.childNodes[0].data.replace(" ", "+")
        # Initialize HTTP request
        if i % 4 == 0:
            request_data = urllib.request.Request(
                url + url_title + '&field=title&sort=relevance&api_key=' + api_key,
                headers=header_list[0])
        elif i % 4 == 1:
            request_data = urllib.request.Request(
                url + url_title + '&field=title&sort=relevance&api_key=' + api_key,
                headers=header_list[1])
        elif i % 4 == 2:
            request_data = urllib.request.Request(
                url + url_title + '&field=title&sort=relevance&api_key=' + api_key,
                headers=header_list[2])
        else:
            request_data = urllib.request.Request(
                url + url_title + '&field=title&sort=relevance&api_key=' + api_key,
                headers=header_list[3])
        try:
            # Start HTTP request
            response = urllib.request.urlopen(request_data)
        # If we got HTTPError (Too many request), retry
        except HTTPError:
            print("HTTPError Occurred")
            continue
        else:
            # Extract data from xml file we downloaded from the url
            search_result = xml.dom.minidom.parseString(response.read()).documentElement
            search_result_count = int(search_result.getElementsByTagName("Count")[0].childNodes[0].data)

            # When we get only one PMId, we write that PMId directly to the XMLDoc
            if search_result_count == 1:
                e_id = search_result.getElementsByTagName("Id")[0].childNodes[0].data
            # When we get 2 PMId, check whether the ArticleTitle includes Re: "
            elif search_result_count == 2:
                if article_titles.childNodes[0].data.startswith("Re: \""):
                    e_id = search_result.getElementsByTagName("Id")[0].childNodes[0].data
                else:
                    e_id = search_result.getElementsByTagName("Id")[1].childNodes[0].data
            elif search_result_count > 2:
                e_id = search_result.getElementsByTagName("Id")[0].childNodes[0].data
            # If we do not get a result
            else:
                # print('Id is Unknown')
                e_id = "10901322"
            if i == int(len(articles)*0.25):
                print(thread_name + " 25% completed")
            if i == int(len(articles)*0.5):
                print(thread_name + " 50% completed")
            if i == int(len(articles)*0.75):
                print(thread_name + " 75% completed")
            # Write PMId we gathered from URL to the XMLDoc
            pm_id.childNodes[0].data = e_id
            i += 1


# Main Thread
# In this file, we are bulk searching the PMId by Article Title in ArticleTitles.xml

# Load cleaned local XML file
start_time = time.time()
LocalXML = xml.dom.minidom.parse("ArticleTitlesNO.xml")

# Get Articles from loaded file
Article = LocalXML.documentElement.getElementsByTagName("PubmedArticle")

# Set api_key
api1 = 'e41512ec43b51bb7d149b5a0b9c66be4c708'
api2 = '20877e9a0a8272f86468204498af28e29e08'
api3 = '0a393a37683f8b907e1458233a8b1ce41708'
api4 = '775593f434775130f6a9cf8fc7bc9515e408'

# # Create threads
thread1 = RequestThread("Thread-1", 0, Article[0:int(len(Article) / 4)], api1)
thread2 = RequestThread("Thread-2", 0, Article[int(len(Article) / 4):int((len(Article) / 4)) * 2], api2)
thread3 = RequestThread("Thread-3", 0, Article[int((len(Article) / 4)) * 2:int((len(Article)) / 4) * 3], api3)
thread4 = RequestThread("Thread-4", 0, Article[int((len(Article) / 4)) * 3:len(Article)], api4)

# Start threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

# Write the data to local xml file
file = open('5_result.xml', 'w')  # (Change '5_result.xml' to the filename you want to use)
LocalXML.writexml(file, encoding='utf-8')
del LocalXML
file.close()

end_time = time.time()
print("Main thread completed. Time cost: " + str(int(int(end_time - start_time) / 60)) + " minutes " + str(
    int(end_time - start_time) % 60) + " seconds ")
