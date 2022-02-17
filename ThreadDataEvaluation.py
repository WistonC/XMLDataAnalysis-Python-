import threading
import time
import urllib
import xml.dom.minidom
from urllib import request
from urllib.error import HTTPError

class RequestThread(threading.Thread):
    def __init__(self, thread_id, name, delay, article_titles, api_key):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.delay = delay
        self.ArticleTitles = article_titles
        self.api_key = api_key

    def run(self):
        print("Starting Thread：" + self.name)
        get_data_from_url(self.name, self.delay, self.ArticleTitles, self.api_key)
        print("Thread: " + self.name + " completed!")


def get_data_from_url(thread_name, delay, articles, api_key):
    ok = 0
    # Initialize URL and header
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id='
    header_list = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0'},
                   {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'},
                   {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00'}, {
                       'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}]
    count = 0
    i = 0
    while i < len(articles):
        time.sleep(delay)
        article_titles = articles[i].getElementsByTagName("ArticleTitle")[0].childNodes[0].data
        pm_id = articles[i].getElementsByTagName("PMID")[0].childNodes[0].data
        # Replace space by + for HTTP request
        # Start HTTP request
        if count % 4 == 0:
            request = urllib.request.Request(url +
                                             pm_id + '&api_key=' + api_key,
                                             headers=header_list[0])
        elif count % 4 == 1:
            request = urllib.request.Request(url +
                                             pm_id + '&api_key=' + api_key,
                                             headers=header_list[1])
        elif count % 4 == 2:
            request = urllib.request.Request(url +
                                             pm_id + '&api_key=' + api_key,
                                             headers=header_list[2])
        else:
            request = urllib.request.Request(url +
                                             pm_id + '&api_key=' + api_key,
                                             headers=header_list[3])
        try:
            response = urllib.request.urlopen(request)
        # If we got HTTPError (Too many request), retry
        except HTTPError:
            print("HTTPError Occurred")
            continue
        else:
            # Get Item element from XML that include ArticleTitle by PMId from url specified
            TitleCollection = xml.dom.minidom.parseString(response.read()).documentElement
            TC = TitleCollection.getElementsByTagName("Item")
            del TitleCollection
            for Title in TC:
                if Title.hasChildNodes():
                    if Title.attributes.item(0).value == 'Title':
                        result = Title.childNodes[0].data == \
                                 article_titles
                        if result:
                            ok += 1
                        else:
                            print(
                                str(result) + ": " + article_titles)
            count += 1
            # time.sleep(0.09)
            i += 1


# Main Thread
# In this file, we are bulk searching the PMId by Article Title in ArticleTitles.xml
# Load cleaned local XML file
start_time = time.time()
LocalXML = xml.dom.minidom.parse("group5_result.xml")
PubmedArticleSet = LocalXML.documentElement
# Get ArticleTitles from loaded file
Article = PubmedArticleSet.getElementsByTagName("PubmedArticle")
api1 = 'e41512ec43b51bb7d149b5a0b9c66be4c708'
api2 = '20877e9a0a8272f86468204498af28e29e08'
api3 = '0a393a37683f8b907e1458233a8b1ce41708'
api4 = '775593f434775130f6a9cf8fc7bc9515e408'
# Create thread
thread1 = RequestThread(1, "Thread-1", 0, Article[0:int(len(Article) / 4) + 1], api1)
thread2 = RequestThread(2, "Thread-2", 0, Article[int(len(Article) / 4) + 1:int((len(Article) / 4)) * 2 + 2], api2)
thread3 = RequestThread(3, "Thread-3", 0, Article[int((len(Article) / 4)) * 2 + 2:int((len(Article)) / 4) * 3 + 3],
                        api3)
thread4 = RequestThread(4, "Thread-4", 0, Article[int((len(Article) / 4)) * 3 + 3:len(Article)], api4)

# Start thread
thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

end_time = time.time()

print("Main thread completed. " + str(int(end_time - start_time)))
