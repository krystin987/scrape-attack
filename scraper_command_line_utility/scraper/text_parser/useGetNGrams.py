#useGetNGrams.py

import text_parser.local_parse as local_parse

wordstring = 'it was the best of times it was the worst of times '
wordstring += 'it was the age of wisdom it was the age of foolishness'
allMyWords = wordstring.split()

print(local_parse.getNGrams(allMyWords, 5))