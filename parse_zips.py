from numpy import kaiser
import text_parser.local_parse as local_parse
import text_parser.get_keywords as get_keywords

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
                with open(file_path) as f:
                    print(get_keywords.get_key_words(f.read()))


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