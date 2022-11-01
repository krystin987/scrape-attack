from . import local_parse

n = 7

def transform_html_to_kwic(article, articleId, url, rss_topic, directory):
    text = local_parse.stripTags(article).lower()
    fullwordlist = ('# ' * (n//2)).split()
    fullwordlist += local_parse.stripNonAlphaNum(text)
    fullwordlist += ('# ' * (n//2)).split()
    ngrams = local_parse.getNGrams(fullwordlist, n)
    worddict = local_parse.nGramsToKWICDict(ngrams)

    # output KWIC and wrap with html
    target = f'{rss_topic}'
    outstr = '<pre>'
    if target in worddict:
        for k in worddict[target]:
            outstr += local_parse.prettyPrintKWIC(k)
            outstr += '<br />'
    else:
        outstr += 'Keyword not found in source'

    outstr += '</pre>'
    local_parse.wrapStringInHTMLMac(articleId, url, outstr, rss_topic, "kwic", directory)