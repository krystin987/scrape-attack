# html-to-kwic.py

import text_parser.local_parse as local_parse

# create dictionary of n-grams
n = 7
url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

text = local_parse.webPageToText(url)
fullwordlist = ('# ' * (n//2)).split()
fullwordlist += local_parse.stripNonAlphaNum(text)
fullwordlist += ('# ' * (n//2)).split()
ngrams = local_parse.getNGrams(fullwordlist, n)
worddict = local_parse.nGramsToKWICDict(ngrams)

# output KWIC and wrap with html
target = 'black'
outstr = '<pre>'
if target in worddict:
    for k in worddict[target]:
        outstr += local_parse.prettyPrintKWIC(k)
        outstr += '<br />'
else:
    outstr += 'Keyword not found in source'

outstr += '</pre>'
local_parse.wrapStringInHTMLMac('html-to-kwic', url, outstr)