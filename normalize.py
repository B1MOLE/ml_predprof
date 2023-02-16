from nltk.corpus import stopwords
from nltk.corpus import words
import nltk
import re

def normalize(string):
    stop_words = set(stopwords.words('english'))
    words = set(nltk.corpus.words.words())
    lower_string = string.lower()
    no_number_string = re.sub(r'\d+', '', lower_string)
    no_punc_string = re.sub(r'[^\w\s]', '', no_number_string)
    no_wspace_string = no_punc_string.strip()
    lst_string = [no_wspace_string][0].split()
    no_stpwords_string = ""
    for i in lst_string:
        if not i in stop_words:
            no_stpwords_string += i + ' '
    no_stpwords_string = no_stpwords_string[:-1]
    " ".join(w for w in nltk.wordpunct_tokenize(no_stpwords_string) if w.lower() in words or not w.isalpha())

    return no_stpwords_string