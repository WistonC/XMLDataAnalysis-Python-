import xml.dom.minidom
from xml.dom.minidom import Document

# In this file, we are seperate the ArticleTitle data from SampleOrininalData.xml
# Load the XML file
LocalXML = xml.dom.minidom.parse("SampleOriginalData.xml")  # Change SimpleOriginalData.xml to your local filename
RootElement = LocalXML.documentElement

# Get Article from loaded file
Articles = RootElement.getElementsByTagName("Article")

# Crate now XML doc
NewXMLDoc = Document()
# Crate now root element
PAS = NewXMLDoc.createElement('PubmedArticleSet')
NewXMLDoc.appendChild(PAS)

# Get Article titles
count = 1
for Article in Articles:
    # Load Article Titles Elements
    ArticleTitle = Article.getElementsByTagName("ArticleTitle")[0]

    # Copy Article Title Data to created XML doc
    A = NewXMLDoc.createElement('Article')
    AT = NewXMLDoc.createElement('ArticleTitle')
    AT.appendChild(NewXMLDoc.createTextNode(ArticleTitle.childNodes[0].data))
    A.appendChild(AT)
    PAS.appendChild(A)
    print('Element NO.' + str(count) + ' processed')
    count += 1

# Save data to local file (if file does not exist, it will be created automatically)
file = open('ArticleTitles.xml', 'w')
NewXMLDoc.writexml(file, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
file.close()
