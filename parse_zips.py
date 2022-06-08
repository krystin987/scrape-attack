from zipfile import ZipFile
from pathlib import Path
import webbrowser



def main(file_to_unzip):
    unzip_directory = Path(f"./unzipped_web_data/")
    with ZipFile(file_to_unzip, 'r') as zip_ref:
        zip_ref.extractall(unzip_directory)

main()

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