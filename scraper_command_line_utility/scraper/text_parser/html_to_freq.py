# html-to-freq-3.py
import text_parser.local_parse as local_parse

# create sorted dictionary of word-frequency pairs
def frequency_html(text, articleId, url, rss_topic):
    # text = local_parse.stripTags(text).lower()
    fullwordlist = local_parse.stripNonAlphaNum(text)
    wordlist = local_parse.removeStopwords(fullwordlist, local_parse.stopwords)
    dictionary = local_parse.wordListToFreqDict(wordlist)
    sorteddict = local_parse.sortFreqDict(dictionary)

    # compile dictionary into string and wrap with HTML
    outstring = ""
    for s in sorteddict:
        outstring += str(s)
        outstring += "<br />"
    local_parse.wrapStringInHTMLMac(articleId, url, outstring, rss_topic, "freq")