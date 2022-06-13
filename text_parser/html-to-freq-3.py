# html-to-freq-3.py
import text_parser.local_parse as local_parse

# create sorted dictionary of word-frequency pairs
url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
text = local_parse.webPageToText(url)
fullwordlist = local_parse.stripNonAlphaNum(text)
wordlist = local_parse.removeStopwords(fullwordlist, local_parse.stopwords)
dictionary = local_parse.wordListToFreqDict(wordlist)
sorteddict = local_parse.sortFreqDict(dictionary)

# compile dictionary into string and wrap with HTML
outstring = ""
for s in sorteddict:
    outstring += str(s)
    outstring += "<br />"
local_parse.wrapStringInHTMLMac("html-to-freq-3", url, outstring)