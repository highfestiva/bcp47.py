
countries = defaultdict(set)
for tag in tags:
    lang, _, country = tag.rpartition('-')
    if country.isupper() and 2 <= len(country) <= 3:
        countries[country].add(lang)
        countries[country].add(tag)
