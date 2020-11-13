# BCP47
Language tags are not your everyday ISO standard, but instead composed of an ISO-639 language code, and an ISO-3166 country/region code
(and occationally an ISO-15924 script tag for the written language).

The file is generated from Microsoft's seminal piece, [MS-LCID].pdf.


## Easy installation

```bash
$ pip install bcp47
```


## Example

```python
>>> import bcp47

>>> 'dje' in bcp47.tags and 'es-DO' in bcp47.tags
True

>>> [v for k,v in bcp47.languages.items() if 'English' in k]
['en', 'en-AS', 'en-AI', 'en-AG', 'en-AU', 'en-AT', 'en-BS', 'en-BB', 'en-BE', 'en-BZ', 'en-BM', 'en-BW', 'en-IO', ...]
```


## Discontentment

This package only lists the most common language codes. If you want a package to parse, validate and simplify full BCP47 language tags,
have a look at [langcodes](https://github.com/LuminosoInsight/langcodes) or [langtags](https://github.com/jsommers/langtags).

The BCP47 standard is 84 pages catering to specificity (such as `de-CH-1996` and `zh-CN-a-myext-x-private`) while this package currently
does not. Instead a highly pragmatic approach is used (some say [overly simplified](https://github.com/highfestiva/bcp47.py/issues/2))
where only the most common 900 or so language codes are listed, such as `fo-DK` and `iu-Cans-CA`.

Microsoft's language codes are used to ensure some level of pragmatism, [KISS](https://en.wikipedia.org/wiki/KISS_principle). Validation you
will have to do yourself, see above for a trivial example.

Enjoy at the best of your ability!
