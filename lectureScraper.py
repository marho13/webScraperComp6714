import re
import requests
from bs4 import BeautifulSoup as bs
from os import path

htmlLink = "http://www.cse.unsw.edu.au/~cs6714/17s2/index.html"
htmlLink1 = "https://nlp.stanford.edu/IR-book/"
htmlLink2 = "http://ciir.cs.umass.edu/irbook/"
htmlLink3 = "https://web.stanford.edu/~jurafsky/slp3/"

def nameChecker(html, content, webLink):
    arr = ['cs6714', 'jurafsky', 'nlp.stanford', 'ciir.cs']
    for n in arr:
        name = re.search(html, n)
        if name != None and n == arr[0]:
            fileName = path.join("lectures/", webLink.get('href')[7:])
            with open(fileName, 'wb') as pdf:
                pdf.write(content.content)

        elif name != None and n == arr[1]:
            fileName = path.join("Book4/", webLink)
            with open(fileName, 'wb') as pdf:
                pdf.write(content.content)

        elif name != None and n == arr[2]:
            fileName = path.join("Book1/", webLink)
            with open(fileName, 'wb') as pdf:
                pdf.write(content.content)

        elif name != None and n == arr[3]:
            fileName = "Book2/SEIRiP.pdf"
            with open(fileName, 'wb') as pdf:
                pdf.write(content.content)

def Scraper(html):

    page = requests.get(html)
    c = page.content
    soup = bs(c, 'html.parser')


    baseSite = re.search(".edu", html).span()[1]
    if baseSite == None:
        baseSite = re.search(".au", html)

    for link in soup.find_all('a'):
        if link.get('href')[-4:] == '.pdf':
            print(link.get('href'))
            print(html[:baseSite])
            if re.search(".lect", link.get('href')):
                endLink =  html[:baseSite] + link.get('href')[1:]
                webLink = link.get('href')[1]
            else:
                webLink = link.get('href')
                endLink = html[:baseSite] + link.get('href')
            print(endLink)
            content = requests.get(endLink)
            if content.status_code == 200 and content.headers['content-type']=='application/pdf':
                nameChecker(html, content, webLink)

        elif link.get('href') == "/ccount/click.php?id=1":
            print(link.get('href'))
            print(html[:baseSite])
            endLink = path.join(html[:baseSite] + link.get('href'))
            content = requests.get(endLink)
            if content.status_code == 200 and content.headers['content-type'] == 'application/pdf':
                nameChecker(html, content, endLink)

Scraper(htmlLink)
Scraper(htmlLink1)
Scraper(htmlLink2)
Scraper(htmlLink3)