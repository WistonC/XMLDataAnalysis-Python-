import time
import urllib
import xml.dom.minidom
from urllib import request
from xml.dom.minidom import Document

# In this file, we are bulk searching the PMId by Article Title in ArticleTitles.xml
# Initialize URL and header
url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0'}

# Load cleaned local XML file
LocalXML = xml.dom.minidom.parse("ArticleTitles.xml")
PubmedArticleSet = LocalXML.documentElement

# Get Article from loaded file
Articles = PubmedArticleSet.getElementsByTagName("Article")

# Crate now XML doc
NewXMLDoc = Document()
# Crate now root element
PAS = NewXMLDoc.createElement('PubmedArticleSet')
NewXMLDoc.appendChild(PAS)

count = 1
# Get Article title and search it on the url specified
for Article in Articles:
    # Get Article Titles Elements
    ArticleTitle = Article.getElementsByTagName("ArticleTitle")[0]

    # Replace backspace by + for HTTP request
    UrlData = ArticleTitle.childNodes[0].data.replace(" ", "+")
    # Start HTTP request
    request = urllib.request.Request(url + UrlData + '&field=title&sort=relevance', headers=header)
    response = urllib.request.urlopen(request)
    # Get XML from HTTP server
    IdCollection = xml.dom.minidom.parseString(response.read()).documentElement

    # Get PMId from NCBI server
    # Only proceed when we get a result
    if IdCollection.getElementsByTagName("Count")[0].childNodes[0].data != '0':
        # Create PMId Element in XMLDoc to save PMId
        PMid = NewXMLDoc.createElement('PMId')
        IdListSize = IdCollection.getElementsByTagName("Count")[0].childNodes[0].data
        eId = IdCollection.getElementsByTagName("Id")[0].childNodes[0].data
        print('Id is ' + eId)
        # Save PMId to the XMLDoc
        PMid.appendChild(NewXMLDoc.createTextNode(eId))

        # Create PubmedArticle and ArticleTitle element in XMLDoc
        A = NewXMLDoc.createElement('PubmedArticle')
        AT = NewXMLDoc.createElement('ArticleTitle')

        # Copy Data to the XMLDoc
        AT.appendChild(NewXMLDoc.createTextNode(ArticleTitle.childNodes[0].data))
        A.appendChild(PMid)
        A.appendChild(AT)
        PAS.appendChild(A)

        # Completion prompt
        print('Element NO.' + str(count) + ' processed' + '\n')

        # Wait 0.2 seconds
        time.sleep(0.2)
        count +=1
    # If we do not get a result
    else:
        if count > 500:
            break
        print('Unknown Id, skipped' + '\n')
        count += 1
        continue

# Write data to local files
file = open('Demo.xml', 'w')  # (Change 'Demo.xml' to the filename you want to use)
NewXMLDoc.writexml(file, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
file.close()
