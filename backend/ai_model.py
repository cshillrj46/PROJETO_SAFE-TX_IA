# File: backend/ai_model.py

import joblib

model = joblib.load("risk_model.joblib")
encoder_sender = joblib.load("encoder_sender.joblib")
encoder_recipient = joblib.load("encoder_recipient.joblib")
encoder_risk = joblib.load("encoder_risk.joblib")

def predict_risk(sender: str, recipient: str, amount_eth: float) -> str:
    try:
        sender_encoded = encoder_sender.transform([sender])[0]
    except:
        sender_encoded = 0  # Valor neutro para desconhecido

    try:
        recipient_encoded = encoder_recipient.transform([recipient])[0]
    except:
        recipient_encoded = 0

    features = [[sender_encoded, recipient_encoded, amount_eth]]
    prediction = model.predict(features)[0]
    return encoder_risk.inverse_transform([prediction])[0]
