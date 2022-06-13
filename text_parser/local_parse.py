import re, time, socket, os, datetime, math
import urllib.request, urllib.error, urllib.parse

from os.path import join as pjoin
from webbrowser import open_new_tab

stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

def stripTags(pageContents):
    pageContents = str(pageContents)
    startLoc = pageContents.find("<p>")
    endLoc = pageContents.rfind("<br/>")

    pageContents = pageContents[startLoc:endLoc]

    inside = 0
    text = ''

    for char in pageContents:
        if char == '<':
            inside = 1
        elif (inside == 1 and char == '>'):
            inside = 0
        elif inside == 1:
            continue
        else:
            text += char

    return text

# Given a text string, remove all non-alphanumeric
# characters (using Unicode definition of alphanumeric).

def stripNonAlphaNum(text):
    return re.compile(r'\W+', re.UNICODE).split(text)

def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist,wordfreq)))

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

# Given a URL, return string of lowercase text from page.

def webPageToText(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode('UTF-8')
    text = stripTags(html).lower()
    return text

# Given name of calling program, a url and a string to wrap,
# output string in html body with basic metadata and open in Firefox tab.

def wrapStringInHTMLMac(program, url, body):
    now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    filename = program + '.html'
    f = open(filename,'w')

    wrapper = """<html>
    <head>
    <title>%s output - %s</title>
    </head>
    <body><p>URL: <a href=\"%s\">%s</a></p><p>%s</p></body>
    </html>"""

    whole = wrapper % (program, now, url, url, body)
    f.write(whole)
    f.close()

    #Change the filepath variable below to match the location of your directory
    filename = 'file:///Users/krystinvilleneuve/programming-historian/python-html/' + filename

    open_new_tab(filename)

# Given a list of words and a number n, return a list
# of n-grams.

def getNGrams(wordlist, n):
    return [wordlist[i:i+n] for i in range(len(wordlist)-(n-1))]

# Given a list of n-grams, return a dictionary of KWICs,
# indexed by keyword.

def nGramsToKWICDict(ngrams):
    keyindex = len(ngrams[0]) // 2

    kwicdict = {}

    for k in ngrams:
        if k[keyindex] not in kwicdict:
            kwicdict[k[keyindex]] = [k]
        else:
            kwicdict[k[keyindex]].append(k)
    return kwicdict

# Given a KWIC, return a string that is formatted for
# pretty printing.

def prettyPrintKWIC(kwic):
    n = len(kwic)
    keyindex = n // 2
    width = 10

    outstring = ' '.join(kwic[:keyindex]).rjust(width*keyindex)
    outstring += str(kwic[keyindex]).center(len(kwic[keyindex])+6)
    outstring += ' '.join(kwic[(keyindex+1):])

    return outstring

#create URLs for search results pages and save the files
def getSearchResults(query, kwparse, fromYear, fromMonth, toYear, toMonth, entries):

    import urllib.request, math, os, re, time

    cleanQuery = re.sub(r'\W+', '', query)
    if not os.path.exists(cleanQuery):
        os.makedirs(cleanQuery)

    startValue = 0

    #Determine how many files need to be downloaded.
    pageCount = entries / 10
    pageCount = math.ceil(pageCount)

    for pages in range(1, pageCount +1):

        #each part of the URL. Split up to be easier to read.
        url = 'https://www.oldbaileyonline.org/search.jsp?gen=1&form=searchHomePage&_divs_fulltext='
        url += query
        url += '&kwparse=' + kwparse
        url += '&_divs_div0Type_div1Type=sessionsPaper_trialAccount'
        url += '&fromYear=' + fromYear
        url += '&fromMonth=' + fromMonth
        url += '&toYear=' + toYear
        url += '&toMonth=' + toMonth
        url += '&start=' + str(startValue)
        url += '&count=0'

        #download the page and save the result.
        response = urllib.request.urlopen(url)
        webContent = response.read().decode('UTF-8')
        filename = cleanQuery + '/' + 'search-result' + str(startValue)
        f = open(filename + ".html", 'w')
        f.write(webContent)
        f.close

        startValue = startValue + 10

        #pause for 3 seconds
        time.sleep(3)

def getIndivTrials(query):

    failedAttempts = []

    #import built-in python functions for building file paths


    cleanQuery = re.sub(r'\W+', '', query)
    searchResults = os.listdir(cleanQuery)

    urls = []

    #find search-results pages
    for files in searchResults:
        if files.find("search-result") != -1:
            f = open(cleanQuery + "/" + files, 'r')
            text = f.read().split(" ")
            f.close()

            #look for trial IDs
            for words in text:
                if words.find("browse.jsp?id=") != -1:
                    #isolate the id
                    urls.append(words[words.find("id=") +3: words.find("&")])

    for items in urls:
        #generate the URL
        url = "http://www.oldbaileyonline.org/print.jsp?div=" + items

        #download the page
        socket.setdefaulttimeout(10)
        try:
            response = urllib.request.urlopen(url)
            webContent = response.read().decode('UTF-8')

            #create the filename and place it in the new directory
            filename = items + '.html'
            filePath = pjoin(cleanQuery, filename)

            #save the file
            f = open(filePath, 'w')
            f.write(webContent)
            f.close
        except urllib.error.URLError:
            failedAttempts.append(url)

        #pause for 3 seconds
        time.sleep(3)

    print("failed to download: " + str(failedAttempts))