# trial-content.py

import urllib.request, urllib.error, urllib.parse, text_parser.local_parse as local_parse

url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

response = urllib.request.urlopen(url)
HTML = response.read().decode('UTF-8')

print((local_parse.stripTags(HTML)))