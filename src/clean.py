import pandas as pd
import re
import emoji
import string
from unidecode import unidecode
import spacy
import nltk
from nltk.corpus import stopwords

# DL les stop words FR
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Get les stop words FR
french_stop_words = set(stopwords.words('french'))

# Model Spacy FR
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    print("Modèle spaCy français non trouvé. Installation en cours...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "fr_core_news_sm"])
    nlp = spacy.load("fr_core_news_sm")

def clean_messages(df):
    """
    Nettoie les messages du chat Twitch en utilisant spaCy.
    
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
    
    # Lemmatisation avec Spacy
    def lemmatize_text(text):
        if not text.strip():
            return ""
        # Traiter texte
        doc = nlp(text)
        # Extraire les lemmes
        lemmas = [token.lemma_ for token in doc if not token.is_space and not token.is_punct]
        # Join lemmes en texte
        return ' '.join(lemmas)
    
    df['content'] = df['content'].apply(lemmatize_text)
    
    # Tokenization avec Spacy
    def process_with_spacy(text):
        if not text.strip():
            return ""
        doc = nlp(text)
        # Extraire les tokens et les lemmes
        tokens = [token.lemma_ for token in doc if not token.is_space and not token.is_punct]
        # Join les tokens en texte
        return ' '.join(tokens)
    
    df['content'] = df['content'].apply(process_with_spacy)
    
    return df

