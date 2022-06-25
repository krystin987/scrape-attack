import locationtagger
import nltk
from numpy import place
import spacy
  
# essential entity models downloads

def extract_location(article_text):
    # might want to run these as part as automation
    # nltk.downloader.download('maxent_ne_chunker', quiet=True)
    # nltk.downloader.download('words', quiet=True)
    # nltk.downloader.download('treebank', quiet=True)
    # nltk.downloader.download('maxent_treebank_pos_tagger', quiet=True)
    # nltk.downloader.download('punkt', quiet=True)
    # nltk.download('averaged_perceptron_tagger', quiet=True)
    
    # extracting entities
    place_entity = locationtagger.find_locations(text = article_text)

    return {
        "features": {
            "countries": place_entity.countries,
            "regions": place_entity.regions,
            "cities": place_entity.cities
        }
    }
    
    # # getting all countries
    # print("The countries in text : ")
    # print(place_entity.countries)
    
    # # getting all states
    # print("The states in text : ")
    # print(place_entity.regions)
    
    # # getting all cities
    # print("The cities in text : ")
    # print(place_entity.cities)

