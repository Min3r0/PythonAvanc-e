import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Charger le dataset
df = pd.read_csv("morpion_dataset.csv")
X = df.drop("best_move", axis=1)
y = df["best_move"]

# Entraîner un modèle RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Sauvegarder le modèle
joblib.dump(model, "morpion_model.pkl")
print("✅ Nouveau modèle entraîné et sauvegardé avec succès.")
