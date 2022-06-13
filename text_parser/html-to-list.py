#html-to-list1.py
import urllib.request, urllib.error, urllib.parse, text_parser.local_parse as local_parse

url = 'http://www.oldbaileyonline.org/print.jsp?div=t17800628-33'

response = urllib.request.urlopen(url)
html = response.read().decode('UTF-8')
text = local_parse.stripTags(html).lower()
wordlist = local_parse.stripNonAlphaNum(text)

print(wordlist)