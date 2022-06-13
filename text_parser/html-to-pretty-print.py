# html-to-pretty-print.py
import text_parser.local_parse as local_parse

# create dictionary of n-grams
n = 7
url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

text = local_parse.webPageToText(url)
fullwordlist = local_parse.stripNonAlphaNum(text)
ngrams = local_parse.getNGrams(fullwordlist, n)
worddict = local_parse.nGramsToKWICDict(ngrams)

print(worddict["black"])