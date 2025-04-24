# File: backend/train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Carregar os dados
df = pd.read_csv("transactions.csv")

# Preprocessamento
df["sender"] = df["sender"].astype(str)
df["recipient"] = df["recipient"].astype(str)

# Codificar os campos categóricos
encoder_sender = LabelEncoder()
encoder_recipient = LabelEncoder()
encoder_risk = LabelEncoder()

df["sender_encoded"] = encoder_sender.fit_transform(df["sender"])
df["recipient_encoded"] = encoder_recipient.fit_transform(df["recipient"])
df["risk_encoded"] = encoder_risk.fit_transform(df["risk"])

# Selecionar features e label
X = df[["sender_encoded", "recipient_encoded", "amount_eth"]]
y = df["risk_encoded"]

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Salvar modelo e encoders
joblib.dump(model, "risk_model.joblib")
joblib.dump(encoder_sender, "encoder_sender.joblib")
joblib.dump(encoder_recipient, "encoder_recipient.joblib")
joblib.dump(encoder_risk, "encoder_risk.joblib")

print("[✅] Modelo treinado e salvo com sucesso!")
