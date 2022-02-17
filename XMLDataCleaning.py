import time
import xml.dom.minidom
from xml.dom.minidom import Document

# In this file, we are separate the ArticleTitle data from 4020a1-datasets.xml
start_time = time.time()
# Load the XML file
LocalXML = xml.dom.minidom.parse("4020a1-datasets.xml")

# Get ArticleTitle from loaded file
Articles = LocalXML.documentElement.getElementsByTagName("ArticleTitle")
del LocalXML
# Crate new XML doc
NewXMLDoc = Document()
# Crate root element
PAS = NewXMLDoc.createElement('PubmedArticleSet')
NewXMLDoc.appendChild(PAS)

# Write ArticleTitle to new XML doc
count = 1
for Article in Articles:
    A = NewXMLDoc.createElement('PubmedArticle')
    Id = NewXMLDoc.createElement('PMID')
    AT = NewXMLDoc.createElement('ArticleTitle')
    # Copy Article Title Data to created XML doc
    AT.appendChild(Article.childNodes[0])
    Id.appendChild(NewXMLDoc.createTextNode(str(count)))
    A.appendChild(Id)
    A.appendChild(AT)
    PAS.appendChild(A)
    count += 1

# Save data to local file (if file does not exist, it will be created automatically)
file = open('ArticleTitlesNO.xml', 'w')
NewXMLDoc.writexml(file, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
file.close()

end_time = time.time()
print("Main thread completed. Time cost: " + str(int(int(end_time - start_time) / 60)) + " minutes " + str(
    int(end_time - start_time) % 60) + " seconds ")
