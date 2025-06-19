import pandas as pd
from src.clean import clean_messages

# Chargement du CSV
df = pd.read_csv("data/chat_messages_samueletienne.csv")

# Nettoyage de la colonne 'content'
df_cleaned = clean_messages(df)

# Sauvegarde propre
df_cleaned.to_csv("data/chat_messages_samueletienne_clean.csv", index=False)

print("✅ Nettoyage terminé")