import os
#import nltk

from epub_conversion.utils import open_book, convert_epub_to_lines
from bs4 import BeautifulSoup
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        return tag

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        return tag

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        self.data = data

book = open_book('data/books/TheFoodLab.epub')

lines = convert_epub_to_lines(book)

#with open('f.txt', 'w') as f:
#    for l in lines:
#        f.write(l+'\n')

#lines = ''.join(lines)
#soup = BeautifulSoup(lines, 'html.parser')
#soup = BeautifulSoup(soup, 'html.parser')

start = False
end = False

parser = MyHTMLParser()

for line in lines:

    if 'recipe_rt' in line:
        parser.feed(line)
        title = parser.data.title()
        print(title)

        exit()
exit()

