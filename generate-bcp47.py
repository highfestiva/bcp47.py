#!/usr/bin/env python3
# coding=utf-8

from PyPDF2 import PdfFileReader
import requests


url = 'https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-LCID/[MS-LCID].pdf'


def extract_phrases(i, step, phrases):
    ps = []
    while i > 0 and i < len(phrases):
        p = phrases[i].strip()
        pl = p.lower()
        if 'version' in pl or 'release' in pl or 'windows' in pl:
            break
        if p:
            ps.append(p)
        i += step
    if step < 0:
        ps = reversed(ps)
    return ps


def generate_page(phrases, w):
    for i,phrase in enumerate(phrases):
        if phrase.startswith('0x'):
            names = extract_phrases(i-1, -1, phrases)
            tags = extract_phrases(i+1, +1, phrases)
            name = ' - '.join(names)
            tag = ''.join(tags)
            print('.', flush=True, end='')
            print('    "%s": "%s",' % (name, tag), file=w)


# download and write local file
if True:
    r = requests.get(url, stream=True)
    with open('.buffer.pdf', 'wb') as w:
        for chunk in r.iter_content(1024):
            w.write(chunk)

# open locally stored file and parse that
with open('bcp47.py', 'wt', encoding='utf-8') as w:
    print('# generated file', file=w)
    print('# coding=utf-8', file=w)
    print('languages = {', file=w)
    with open('.buffer.pdf', 'rb') as r:
        reader = PdfFileReader(r)
        for page in reader.pages:
            phrases = page.extractText().splitlines()
            if 'Language' not in phrases:
                continue
            generate_page(phrases, w)
    print('}', file=w)
    print('file generation complete')
