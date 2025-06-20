import pandas as pd
from src.clean import clean_messages
from src.embedding import create_embeddings_dataframe

# Chargement du CSV
df = pd.read_csv("data/chat_messages_samueletienne.csv")

# Nettoyage de la colonne 'content'
df_cleaned = clean_messages(df)

# Embedding
df_with_embeddings, embeddings = create_embeddings_dataframe(
    df_cleaned, 
    model_name='paraphrase-multilingual-MiniLM-L12-v2'
)

# Sauvegarde propre
df_with_embeddings.to_csv("../data/chat_messages_samueletienne_clean.csv", index=False)

print("✅ Nettoyage terminé")