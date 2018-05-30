#!/usr/bin/python
# coding= utf-8

import json
import codecs
import os
import errno    
from bs4 import BeautifulSoup

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def fill_ketos(ketos_file_name, text_file_name, output_file_name):
    ketos_doc = codecs.open(ketos_file_name, 'r', 'utf-8').read()
    soup = BeautifulSoup(ketos_doc, 'html.parser')

    text_file = codecs.open(text_file_name, 'r', 'utf-8')
    line_num = 0
    while True:
        line_text = text_file.readline()
        line_text = line_text.rstrip()
        if not line_text: break
        line_num += 1
        line = soup.find(id="line_" + `line_num`)
        if line:
            line.append(line_text)

    output = codecs.open(output_file_name, 'w', 'utf-8')
    output.write(unicode(soup))
    output.close()
    text_file.close()

def generate_images(bible_book_file, work_dir):
    mkdir_p(work_dir)
    json_string = codecs.open(bible_book_file, 'r', 'utf-8').read()
    parsed_json = json.loads(json_string)

    chapters = parsed_json['text']
    for i in range(len(chapters)):
        print('Working on chapter ' + `i`)

        image_text_file_name = work_dir + '/image_' + `i` + '.txt'
        image_file_name = work_dir + '/image' + `i` + '.png'
        text_file_name = work_dir + '/text_' + `i` + '.txt'
        ketos_file_name = work_dir + '/ketos_' + `i` + '.html'
        ketos_filled_file_name = work_dir + '/ketos_filled_' + `i` + '.html'

        image_text_file = codecs.open(image_text_file_name , 'w', 'utf-8')
        text_file = codecs.open(text_file_name , 'w', 'utf-8')

        # Prepare a file per chapter, according to this answer https://unix.stackexchange.com/a/138809
        image_text_file.write('text 30,150 "')
        chapter = chapters[i]
        for line in chapter:
            line = line.replace(u'\u05be', ' ')
            text_file.write(line)
            text_file.write('\n')

            words = line.split()
            for n in range(len(words) - 1, -1, -1):
                image_text_file.write(words[n][::-1])
                image_text_file.write(' ')
            image_text_file.write('\n')
        image_text_file.write('"')
        image_text_file.close()
        text_file.close()
    
        print("\tGenerating image")
        os.system('convert -size 4000x5000 xc:white -font "Arial" -pointsize 64 -fill black -draw @' + image_text_file_name + ' '  + image_file_name)

        print("\tRunning Ketos")
        os.system('ketos transcribe -o ' + ketos_file_name + ' ' + image_file_name)

        fill_ketos(ketos_file_name, text_file_name, ketos_filled_file_name)

generate_images('Genesis - he - Tanach with Text Only.json', 'work')
#generate_images('3_chapters.json', 'work')
