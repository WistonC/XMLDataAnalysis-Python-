import time
import urllib
import xml.dom.minidom
from urllib import request

# In this file, we are evaluating the data we are gathering from server
# Initialize URL and header
url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id='
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0'}

# Load cleaned local XML file
LocalXML = xml.dom.minidom.parse("Demo.xml")
PubmedArticleSet = LocalXML.documentElement

# Get Article from loaded file
Articles = PubmedArticleSet.getElementsByTagName("PubmedArticle")

# count means number of runs,
# ok means number of correct
count = 0
ok = 0

# Get Article titles by PMId
for Article in Articles:
    # Load Article Titles Elements
    PMId = Article.getElementsByTagName("PMId")[0].childNodes[0].data

    # Start HTTP request
    request = urllib.request.Request(url + PMId, headers=header)
    response = urllib.request.urlopen(request)

    # Get Item element from XML that include ArticleTitle by PMId from url specified
    TitleCollection = xml.dom.minidom.parseString(response.read()).documentElement
    TC = TitleCollection.getElementsByTagName("Item")
    for Title in TC:
        if Title.hasChildNodes():
            if Title.attributes.item(0).value == 'Title':
                result = Title.childNodes[0].data == Article.getElementsByTagName("ArticleTitle")[0].childNodes[0].data
                if result:
                    ok += 1
    count += 1
    time.sleep(0.2)

print("Process completed")
print("Accuracy: " + str(ok / count))
