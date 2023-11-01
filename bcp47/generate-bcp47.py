#!/usr/bin/env python3
# coding=utf-8

from PyPDF2 import PdfReader
import os
import requests


url = 'https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-LCID/[MS-LCID].pdf'
language_markers = [' Windows ', ' Release ']
bad_markers = ['release:', 'operating', 'server', 'first', 'supported']
join_markers = ['Pseudo', 'Standard']
languages = set()
countries = set()


def is_language_line(phrase):
    return any(lm in phrase for lm in language_markers) and not any(bm in phrase.lower() for bm in bad_markers)


def cleanup(word):
    if word:
        word = word.replace(' -', '-')
        if word.startswith('('):
            word = word.replace('(','').replace(')','')
    return word


def extract_phrase_name_tag(phrase):
    data = phrase
    for lm in language_markers:
        data = data.split(lm)[0].strip()
    data = data.replace('Latin', '(Latin)').replace('((','(').replace('))',')').replace('),', ') ')
    es = [w.strip() for w in data.split('  ') if w.strip()]
    words = []
    for e in es:
        if ' 0x' in e:
            words += e.split()
        else:
            words += [e]
    if len(words) >= 3 and words[1].startswith('('): # ['Javanese', '(Latin)', ...
        words = [' '.join(words[:2])] + words[2:]
    if len(words) == 3: # "Zulu South Africa  0x0435  zu-ZA"
        if words[0].split()[0] in languages and not words[0].endswith(')'):
            l,_,c = words[0].partition(' ')
            words = [l,c] + words[1:]
        if 'City' in words[0] and len(words[0].split()) == 3: # "Latin Vatican City"
            words = words[0].split(maxsplit=1) + words[1:]
    if len(words) == 5: # "Spanish  United  States  0x540A  es-US"
        if words[0] in languages:
            words = words[:1] + [' '.join(words[1:3])] + words[3:]
        elif ' '.join(words[:2]) in languages:
            words = [' '.join(words[:2])] + words[2:]
    if len(words) == 1: # "MA Release 10"
        lang,country,tag = None, None, None
    elif len(words) == 3 and words[1].startswith('0x'):
        lang,country,tag = words[0], None, words[2]
    elif len(words) == 4 and words[2].startswith('0x'):
        lang = words[0]
        country = words[1].replace(' -', '-')
        tag = words[3]
    else:
        assert False, f'unknown phrase "{phrase}", {words}'
    lang,country = cleanup(lang),cleanup(country)
    if tag:
        tag = tag.replace(' ', '')
    # print(f'"{phrase}", {words}') # debug
    languages.add(lang)
    countries.add(country)
    name = f'{lang} - {country}' if country else lang
    return name,tag


def generate_page(phrases):
    name_tag = []
    for i,phrase in enumerate(phrases):
        # print(i, phrase) # debug
        if is_language_line(phrase):
            name,tag = extract_phrase_name_tag(phrase)
            if name and tag:
                name_tag.append((name, tag))
            print('.', flush=True, end='')
    return name_tag


def join_phrases(phrases):
    '''Join lines when possibly appropriate...'''
    complete_phrases = []
    prev = ''
    for phrase in phrases:
        phrase = phrase.strip()
        if phrase.startswith('(') or phrase.partition(' ')[0].endswith(')') \
                or (len(phrase.split()) <= 4 and is_language_line(phrase)) \
                or (is_language_line(phrase) and not is_language_line(prev) and any(jm in prev for jm in join_markers)):
            complete_phrases[-1] += ' ' + phrase
        else:
            complete_phrases.append(phrase)
        prev = phrase
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
            assert name not in namecache, f'{name} already entered before'
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
    reader = PdfReader(r)
    for page in reader.pages:
        phrases = page.extract_text().splitlines()
        phrases = join_phrases(phrases)
        name_tag += generate_page(phrases)
write_output(name_tag)
print('file generation complete')
