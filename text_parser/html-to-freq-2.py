# html-to-freq-2.py

import urllib.request, urllib.error, urllib.parse
import text_parser.local_parse as local_parse

url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

response = urllib.request.urlopen(url)
html = response.read().decode('UTF-8')
text = local_parse.stripTags(html).lower()
fullwordlist = local_parse.stripNonAlphaNum(text)
wordlist = local_parse.removeStopwords(fullwordlist, local_parse.stopwords)
dictionary = local_parse.wordListToFreqDict(wordlist)
sorteddict = local_parse.sortFreqDict(dictionary)

for s in sorteddict: print(str(s))