from numpy import kaiser
import text_parser.local_parse as local_parse
import text_parser.get_keywords as get_keywords
import json

import os


from zipfile import ZipFile
from pathlib import Path




def main(file_to_unzip):
    path = Path(f"/tmp/unzip")
    with ZipFile(file_to_unzip, 'r') as zip_ref:
        zip_ref.extractall(path)
        for subdir, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(subdir, file)
                # print(subdir)

                with open(file_path) as f:
                    # mah_dump = json.dumps(get_keywords.get_key_words(f.read()))
                    get_keywords.get_key_words(f.read())
                    # dump = local_parse.nGramsToKWICDict(dump)
                    # print(dump)
                    # json.dump(json.dumps(get_keywords.get_key_words(f.read())),(f"{subdir}/meta2.json").open("w"))
                    # print(get_keywords.get_key_words(f.read()))
                    # with open(f"{subdir}/meta2.json", "a") as fl:
                    # json.dump(dict1, out_file, indent = 6)
                    # json.dump(mah_dump, subdir + "/metadata.json", indent = 2)
                    #     print(fl)
                        #  for row in get_keywords.get_key_words(f.read()):
                        # fl.write(' '.join([str(a) for a in row]) + '\n')


if __name__ == "__main__": #pattern for fetching positional arguments
    import sys
    _, *args = sys.argv
    main(args[0])

# webbrowser.open('http://www.python.org')

# f = open('GFG.html', 'w')
  
# # the html code which will go in the file GFG.html
# html_template = """<html>
# <head>
# <title>Title</title>
# </head>
# <body>
# <h2>Welcome To GFG</h2>
  
# <p>Default code has been loaded into the Editor.</p>
  
# </body>
# </html>
# """
  
# # writing the code into the file
# f.write(html_template)
  
# # close the file
# f.close()

# [["{\"article_id\":", "\"1182049378567065283\",", "\"keywords\":", "[\"say\",", "\"attack\","], ["\"1182049378567065283\",", "\"keywords\":", "[\"say\",", "\"attack\",", "\"sheriffs\","], ["\"keywords\":", "[\"say\",", "\"attack\",", "\"sheriffs\",", "\"woman\","], ["[\"say\",", "\"attack\",", "\"sheriffs\",", "\"woman\",", "\"center\","], ["\"attack\",", "\"sheriffs\",", "\"woman\",", "\"center\",", "\"office\","], ["\"sheriffs\",", "\"woman\",", "\"center\",", "\"office\",", "\"family\","], ["\"woman\",", "\"center\",", "\"office\",", "\"family\",", "\"dog\","], ["\"center\",", "\"office\",", "\"family\",", "\"dog\",", "\"tennessee\","], ["\"office\",", "\"family\",", "\"dog\",", "\"tennessee\",", "\"70\","], ["\"family\",", "\"dog\",", "\"tennessee\",", "\"70\",", "\"county\","], ["\"dog\",", "\"tennessee\",", "\"70\",", "\"county\",", "\"yard\","], ["\"tennessee\",", "\"70\",", "\"county\",", "\"yard\",", "\"officials\","], ["\"70\",", "\"county\",", "\"yard\",", "\"officials\",", "\"dead\","], ["\"county\",", "\"yard\",", "\"officials\",", "\"dead\",", "\"dogs\","], ["\"yard\",", "\"officials\",", "\"dead\",", "\"dogs\",", "\"taken\","], ["\"officials\",", "\"dead\",", "\"dogs\",", "\"taken\",", "\"animal\"],"], ["\"dead\",", "\"dogs\",", "\"taken\",", "\"animal\"],", "\"title\":"], ["\"dogs\",", "\"taken\",", "\"animal\"],", "\"title\":", "\"Tennessee"], ["\"taken\",", "\"animal\"],", "\"title\":", "\"Tennessee", "woman,"], ["\"animal\"],", "\"title\":", "\"Tennessee", "woman,", "70,"], ["\"title\":", "\"Tennessee", "woman,", "70,", "found"], ["\"Tennessee", "woman,", "70,", "found", "dead"], ["woman,", "70,", "found", "dead", "in"], ["70,", "found", "dead", "in", "family"], ["found", "dead", "in", "family", "dog"], ["dead", "in", "family", "dog", "attack,"], ["in", "family", "dog", "attack,", "officials"], ["family", "dog", "attack,", "officials", "say\","], ["dog", "attack,", "officials", "say\",", "\"url\":"], ["attack,", "officials", "say\",", "\"url\":", "\"https://www.nbcnews.com/news/us-news/tennessee-woman-70-found-dead-family-dog-attack-officials-say-rcna32518\","], ["officials", "say\",", "\"url\":", "\"https://www.nbcnews.com/news/us-news/tennessee-woman-70-found-dead-family-dog-attack-officials-say-rcna32518\",", "\"domain\":"], ["say\",", "\"url\":", "\"https://www.nbcnews.com/news/us-news/tennessee-woman-70-found-dead-family-dog-attack-officials-say-rcna32518\",", "\"domain\":", "\"nbcnews.com\","], ["\"url\":", "\"https://www.nbcnews.com/news/us-news/tennessee-woman-70-found-dead-family-dog-attack-officials-say-rcna32518\",", "\"domain\":", "\"nbcnews.com\",", "\"authors\":"], ["\"https://www.nbcnews.com/news/us-news/tennessee-woman-70-found-dead-family-dog-attack-officials-say-rcna32518\",", "\"domain\":", "\"nbcnews.com\",", "\"authors\":", "[\"Marlene"], ["\"domain\":", "\"nbcnews.com\",", "\"authors\":", "[\"Marlene", "Lenthang\","], ["\"nbcnews.com\",", "\"authors\":", "[\"Marlene", "Lenthang\",", "\"Marlene"], ["\"authors\":", "[\"Marlene", "Lenthang\",", "\"Marlene", "Lenthang"], ["[\"Marlene", "Lenthang\",", "\"Marlene", "Lenthang", "Is"], ["Lenthang\",", "\"Marlene", "Lenthang", "Is", "A"], ["\"Marlene", "Lenthang", "Is", "A", "Breaking"], ["Lenthang", "Is", "A", "Breaking", "News"], ["Is", "A", "Breaking", "News", "Reporter"], ["A", "Breaking", "News", "Reporter", "For"], ["Breaking", "News", "Reporter", "For", "Nbc"], ["News", "Reporter", "For", "Nbc", "News"], ["Reporter", "For", "Nbc", "News", "Digital.\"],"], ["For", "Nbc", "News", "Digital.\"],", "\"summary\":"], ["Nbc", "News", "Digital.\"],", "\"summary\":", "\"A"], ["News", "Digital.\"],", "\"summary\":", "\"A", "70-year-old"], ["Digital.\"],", "\"summary\":", "\"A", "70-year-old", "woman"], ["\"summary\":", "\"A", "70-year-old", "woman", "in"], ["\"A", "70-year-old", "woman", "in", "Tennessee"], ["70-year-old", "woman", "in", "Tennessee", "has"], ["woman", "in", "Tennessee", "has", "died"], ["in", "Tennessee", "has", "died", "after"], ["Tennessee", "has", "died", "after", "she"], ["has", "died", "after", "she", "was"], ["died", "after", "she", "was", "attacked"], ["after", "she", "was", "attacked", "by"], ["she", "was", "attacked", "by", "a"], ["was", "attacked", "by", "a", "family"], ["attacked", "by", "a", "family", "dog,"], ["by", "a", "family", "dog,", "according"], ["a", "family", "dog,", "according", "to"], ["family", "dog,", "according", "to", "officials.\\nDebbie"], ["dog,", "according", "to", "officials.\\nDebbie", "Boyd"], ["according", "to", "officials.\\nDebbie", "Boyd", "was"], ["to", "officials.\\nDebbie", "Boyd", "was", "found"], ["officials.\\nDebbie", "Boyd", "was", "found", "dead"], ["Boyd", "was", "found", "dead", "suffering"], ["was", "found", "dead", "suffering", "\\u201cnumerous"], ["found", "dead", "suffering", "\\u201cnumerous", "dog"], ["dead", "suffering", "\\u201cnumerous", "dog", "bites\\u201d"], ["suffering", "\\u201cnumerous", "dog", "bites\\u201d", "on"], ["\\u201cnumerous", "dog", "bites\\u201d", "on", "Friday"], ["dog", "bites\\u201d", "on", "Friday", "at"], ["bites\\u201d", "on", "Friday", "at", "a"], ["on", "Friday", "at", "a", "home"], ["Friday", "at", "a", "home", "in"], ["at", "a", "home", "in", "Olympic"], ["a", "home", "in", "Olympic", "View"], ["home", "in", "Olympic", "View", "Court"], ["in", "Olympic", "View", "Court", "in"], ["Olympic", "View", "Court", "in", "Seymour,"], ["View", "Court", "in", "Seymour,", "the"], ["Court", "in", "Seymour,", "the", "Sevier"], ["in", "Seymour,", "the", "Sevier", "County"], ["Seymour,", "the", "Sevier", "County", "Sheriff\\u2019s"], ["the", "Sevier", "County", "Sheriff\\u2019s", "Office"], ["Sevier", "County", "Sheriff\\u2019s", "Office", "said.\\nTwo"], ["County", "Sheriff\\u2019s", "Office", "said.\\nTwo", "large"], ["Sheriff\\u2019s", "Office", "said.\\nTwo", "large", "Rottweiler"], ["Office", "said.\\nTwo", "large", "Rottweiler", "dogs"], ["said.\\nTwo", "large", "Rottweiler", "dogs", "were"], ["large", "Rottweiler", "dogs", "were", "found"], ["Rottweiler", "dogs", "were", "found", "fenced"], ["dogs", "were", "found", "fenced", "in"], ["were", "found", "fenced", "in", "the"], ["found", "fenced", "in", "the", "yard"], ["fenced", "in", "the", "yard", "of"], ["in", "the", "yard", "of", "the"], ["the", "yard", "of", "the", "home"], ["yard", "of", "the", "home", "that"], ["of", "the", "home", "that", "were"], ["the", "home", "that", "were", "\\u201csecured"], ["home", "that", "were", "\\u201csecured", "by"], ["that", "were", "\\u201csecured", "by", "family"], ["were", "\\u201csecured", "by", "family", "members\\u201d"], ["\\u201csecured", "by", "family", "members\\u201d", "before"], ["by", "family", "members\\u201d", "before", "first"], ["family", "members\\u201d", "before", "first", "responders"], ["members\\u201d", "before", "first", "responders", "arrived,"], ["before", "first", "responders", "arrived,", "officials"], ["first", "responders", "arrived,", "officials", "said.\\nThe"], ["responders", "arrived,", "officials", "said.\\nThe", "sheriff's"], ["arrived,", "officials", "said.\\nThe", "sheriff's", "office"], ["officials", "said.\\nThe", "sheriff's", "office", "said"], ["said.\\nThe", "sheriff's", "office", "said", "it"], ["sheriff's", "office", "said", "it", "was"], ["office", "said", "it", "was", "determined"], ["said", "it", "was", "determined", "the"], ["it", "was", "determined", "the", "dogs"], ["was", "determined", "the", "dogs", "were"], ["determined", "the", "dogs", "were", "in"], ["the", "dogs", "were", "in", "the"], ["dogs", "were", "in", "the", "home"], ["were", "in", "the", "home", "with"], ["in", "the", "home", "with", "the"], ["the", "home", "with", "the", "victim"], ["home", "with", "the", "victim", "at"], ["with", "the", "victim", "at", "the"], ["the", "victim", "at", "the", "time"], ["victim", "at", "the", "time", "of"], ["at", "the", "time", "of", "the"], ["the", "time", "of", "the", "attack,"], ["time", "of", "the", "attack,", "as"], ["of", "the", "attack,", "as", "was"], ["the", "attack,", "as", "was", "a"], ["attack,", "as", "was", "a", "small"], ["as", "was", "a", "small", "child"], ["was", "a", "small", "child", "who"], ["a", "small", "child", "who", "was"], ["small", "child", "who", "was", "uninjured.\\nThe"], ["child", "who", "was", "uninjured.\\nThe", "dogs"], ["who", "was", "uninjured.\\nThe", "dogs", "were"], ["was", "uninjured.\\nThe", "dogs", "were", "captured"], ["uninjured.\\nThe", "dogs", "were", "captured", "by"], ["dogs", "were", "captured", "by", "the"], ["were", "captured", "by", "the", "sheriff\\u2019s"], ["captured", "by", "the", "sheriff\\u2019s", "office"], ["by", "the", "sheriff\\u2019s", "office", "animal"], ["the", "sheriff\\u2019s", "office", "animal", "control"], ["sheriff\\u2019s", "office", "animal", "control", "division"], ["office", "animal", "control", "division", "and"], ["animal", "control", "division", "and", "and"], ["control", "division", "and", "and", "taken"], ["division", "and", "and", "taken", "to"], ["and", "and", "taken", "to", "an"], ["and", "taken", "to", "an", "animal"], ["taken", "to", "an", "animal", "housing"], ["to", "an", "animal", "housing", "facility,"], ["an", "animal", "housing", "facility,", "where"], ["animal", "housing", "facility,", "where", "they"], ["housing", "facility,", "where", "they", "will"], ["facility,", "where", "they", "will", "remain"], ["where", "they", "will", "remain", "until"], ["they", "will", "remain", "until", "a"], ["will", "remain", "until", "a", "probe"], ["remain", "until", "a", "probe", "is"], ["until", "a", "probe", "is", "completed.\"}"]]