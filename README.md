# BCP47
Language tags are not your everyday ISO standard, but instead composed of an ISO-639 language code, and an ISO-3166 country/region code
(and occationally an ISO-15924 script tag for the written language).

## Easy installation

```bash
$ pip install bcp47
```


## Example

```python
>>> import bcp47
>>> [v for k,v in bcp47.languages.items() if 'English' in k]
['en', 'en-AS', 'en-AI', 'en-AG', 'en-AU', 'en-AT', 'en-BS', 'en-BB', 'en-BE', 'en-BZ', 'en-BM', 'en-BW', 'en-IO', ...]
```

Enjoy!
