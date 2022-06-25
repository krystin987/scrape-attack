import text_parser.local_parse as local_parse

def get_key_words(input_text):
    # input_text = 'this test sentence has eight words in it'
    ngrams = local_parse.getNGrams(input_text.split(), 5)
    
    print(local_parse.nGramsToKWICDict(ngrams))

    return ngrams