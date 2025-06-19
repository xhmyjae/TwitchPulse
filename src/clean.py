import pandas as pd
import re
import emoji
import string
from unidecode import unidecode
from transformers import AutoTokenizer, AutoModel
import torch
import nltk
from nltk.corpus import stopwords

# DL les stop words français
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Get les stop words français
french_stop_words = set(stopwords.words('french'))

# Model BERT et tokenizer
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-french-europeana-cased")
model = AutoModel.from_pretrained("dbmdz/bert-base-french-europeana-cased")

def clean_messages(df):
    """
    Nettoie les messages du chat Twitch en utilisant BERT.
    
    Args:
        df (pandas.DataFrame): DataFrame contenant les messages à nettoyer
        
    Returns:
        pandas.DataFrame: DataFrame nettoyé
    """
    # Convertir la colonne content en string (pour etre sure que c'est un string)
    df['content'] = df['content'].astype(str)
    
    # Convertir en minuscules
    df['content'] = df['content'].str.lower()
    
    # Supprimer les accents
    df['content'] = df['content'].apply(lambda x: unidecode(x))
    
    # Supprimer les URLs
    df['content'] = df['content'].apply(lambda x: re.sub(r'http\S+|www\S+|https\S+', '', x, flags=re.MULTILINE))
    
    # Supprimer les mentions (@username)
    df['content'] = df['content'].apply(lambda x: re.sub(r'@\w+', '', x))
    
    # Supprimer les emojis
    df['content'] = df['content'].apply(lambda x: emoji.replace_emoji(x, ''))
    
    # Supprimer la ponctuation
    df['content'] = df['content'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
    
    # Supprimer les chiffres (a verifier si ca peut etre utile par moment, pour l'instant non)
    # df['content'] = df['content'].apply(lambda x: re.sub(r'\d+', '', x))
    
    # Supprimer les espaces multiples
    df['content'] = df['content'].apply(lambda x: re.sub(r'\s+', ' ', x).strip())
    
    # Supprimer les stop words
    def remove_stop_words(text):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in french_stop_words]
        return ' '.join(filtered_words)
    
    df['content'] = df['content'].apply(remove_stop_words)
    
    # Tokenization avec BERT
    def process_with_bert(text):
        # Tokenize le texte
        tokens = tokenizer.tokenize(text)
        # Rejoindre les tokens en texte
        return ' '.join(tokens)
    
    df['content'] = df['content'].apply(process_with_bert)
    
    return df

