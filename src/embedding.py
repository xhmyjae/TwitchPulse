import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import pickle
import os

def generate_embeddings(texts, model_name='distiluse-base-multilingual-cased-v2'):
    """
    Génère des embeddings avec sentence-transformers.
    
    Args:
        texts (list): Liste de textes à encoder
        model_name (str): Nom du modèle à utiliser
        
    Returns:
        numpy.ndarray: Matrice d'embeddings
    """
    try:
        model = SentenceTransformer(model_name)
        embeddings = model.encode(texts, show_progress_bar=True)
        return embeddings
    except Exception as e:
        print(f"Erreur lors du chargement du modèle {model_name}: {e}")
        print("Utilisation du modèle par défaut...")
        model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
        embeddings = model.encode(texts, show_progress_bar=True)
        return embeddings

def reduce_dimensions(embeddings, n_components=50):
    """
    Réduit la dimensionnalité des embeddings avec PCA.
    
    Args:
        embeddings (numpy.ndarray): Matrice d'embeddings
        n_components (int): Nombre de composantes
        
    Returns:
        numpy.ndarray: Embeddings réduits
    """
    pca = PCA(n_components=min(n_components, embeddings.shape[1]))
    reduced_embeddings = pca.fit_transform(embeddings)
    print(f"Variance expliquée: {pca.explained_variance_ratio_.sum():.3f}")
    return reduced_embeddings, pca

def save_embeddings(embeddings, filename):
    """
    Sauvegarde les embeddings.
    
    Args:
        embeddings (numpy.ndarray): Matrice d'embeddings
        filename (str): Nom du fichier
    """
    # Créer le dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    # Sauvegarder les embeddings
    np.save(f'data/{filename}_embeddings.npy', embeddings)
    print(f"Embeddings sauvegardés dans data/{filename}_embeddings.npy")

def load_embeddings(filename):
    """
    Charge les embeddings.
    
    Args:
        filename (str): Nom du fichier
        
    Returns:
        numpy.ndarray: Matrice d'embeddings
    """
    embeddings = np.load(f'data/{filename}_embeddings.npy')
    return embeddings

def create_embeddings_dataframe(df, model_name='distiluse-base-multilingual-cased-v2'):
    """
    Crée un DataFrame avec les embeddings.
    
    Args:
        df (pandas.DataFrame): DataFrame avec la colonne 'content'
        model_name (str): Nom du modèle à utiliser
        
    Returns:
        pandas.DataFrame: DataFrame avec les embeddings
    """
    texts = df['content'].tolist()
    embeddings = generate_embeddings(texts, model_name)
    
    # Créer un DataFrame avec les embeddings
    embedding_df = pd.DataFrame(embeddings)
    embedding_df.columns = [f'embedding_{i}' for i in range(embeddings.shape[1])]
    
    # Concaténer avec le DataFrame original
    result_df = pd.concat([df.reset_index(drop=True), embedding_df], axis=1)
    
    return result_df, embeddings
