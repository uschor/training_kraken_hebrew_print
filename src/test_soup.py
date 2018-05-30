#!/usr/bin/python
# coding= utf-8

import codecs
import os
from bs4 import BeautifulSoup

i = 1

ketos_doc = codecs.open('output' + `i` + '.html', 'r', 'utf-8').read()

soup = BeautifulSoup(ketos_doc, 'html.parser')

text_file = codecs.open('out/' + `i` + '.txt' , 'r', 'utf-8')
line_num = 0
while True:
    line_text = text_file.readline()
    line_text = line_text.rstrip()
    if not line_text: break
    line_num += 1
    line = soup.find(id="line_" + `line_num`)
    if line:
        line.append(line_text)
        print(line)

output = codecs.open('output' + `i` + '_new.html', 'w', 'utf-8')
output.write(unicode(soup))
output.close()
text_file.close()

