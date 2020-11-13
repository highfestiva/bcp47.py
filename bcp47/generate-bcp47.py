#!/usr/bin/env python3
# coding=utf-8

from PyPDF2 import PdfFileReader
import os
import requests


url = 'https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-LCID/[MS-LCID].pdf'


def extract_phrases(i, step, phrases):
    ps = []
    while i > 0 and i < len(phrases):
        p = phrases[i].strip()
        pl = p.lower()
        if 'version' in pl or 'release' in pl or 'windows' in pl:
            if step < 0 and pl in ('release', 'windows'): # uh-oh, previous word was version of release
                ps = ps[:-1]
            break
        if p:
            ps.append(p)
        i += step
    if step < 0:
        ps = reversed(ps)
    return ps


def generate_page(phrases):
    name_tag = []
    for i,phrase in enumerate(phrases):
        if phrase.startswith('0x'):
            names = extract_phrases(i-1, -1, phrases)
            tags = extract_phrases(i+1, +1, phrases)
            name = ' - '.join(names)
            name = name.replace(' - (', ' (') # proper parenthesis
            name = name.replace(' - - - ', '-') # dash
            tag = ''.join(tags)
            name_tag.append((name, tag))
            print('.', flush=True, end='')
    return name_tag


def join_phrases(phrases):
    '''PyDFP2 generator output separates cells with a single space line, but none for word split.
       This joins phrases only separated by a single linefeed.'''
    complete_phrases = []
    last_ps = ''
    for phrase in phrases:
        ps = phrase.strip()
        if ps and last_ps:
            complete_phrases[len(complete_phrases)-1] += ps
        elif ps:
            complete_phrases.append(phrase)
        last_ps = ps
    return complete_phrases


def write_output(name_tag):
    with open('bcp47.py', 'wt', encoding='utf-8') as w:
        print('# generated file', file=w)
        print('# coding=utf-8', file=w)
        print('languages = {', file=w)
        name_tag = [v for i,v in sorted(enumerate(name_tag), key=lambda ee: ee[0] - (1+len(ee[1][1])/20 if ee[1][0]==name_tag[ee[0]-1][0] and len(ee[1][1])<len(name_tag[ee[0]-1][1]) else 0.0))]
        namecache = set()
        for name,tag in name_tag:
            if name in namecache:
                name += ', ' + tag.split('-')[-1]
            assert name not in namecache
            namecache.add(name)
            print('    "%s": "%s",' % (name, tag), file=w)
        print('}', file=w)
        print(file=w)
        print('tags = {v:k for k,v in languages.items()}', file=w)


# download and write local file
if not os.path.exists('.buffer.pdf'):
    print('Downloading the original masterpiece from Ms.Gates.')
    r = requests.get(url, stream=True)
    with open('.buffer.pdf', 'wb') as w:
        for chunk in r.iter_content(1024):
            w.write(chunk)

# open locally stored file and parse that
name_tag = [] # keeps name+tag tuples
with open('.buffer.pdf', 'rb') as r:
    reader = PdfFileReader(r)
    for page in reader.pages:
        phrases = page.extractText().splitlines()
        if 'Language' not in phrases:
            continue
        phrases = join_phrases(phrases)
        name_tag += generate_page(phrases)
write_output(name_tag)
print('file generation complete')
