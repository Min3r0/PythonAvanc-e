import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("morpion_dataset.csv")
X = df.drop("best_move", axis=1)
y = df["best_move"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "morpion_model.pkl")
print("✅ Nouveau modèle entraîné et sauvegardé avec succès.")