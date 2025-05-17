# File: backend/ai_model.py

import joblib
import os

# Caminhos corretos para a pasta backend
model_path = os.path.join(os.path.dirname(__file__), "risk_model.joblib")
encoder_sender_path = os.path.join(os.path.dirname(__file__), "encoder_sender.joblib")
encoder_recipient_path = os.path.join(os.path.dirname(__file__), "encoder_recipient.joblib")
encoder_risk_path = os.path.join(os.path.dirname(__file__), "encoder_risk.joblib")

# Carga dos arquivos
try:
    model = joblib.load(model_path)
    encoder_sender = joblib.load(encoder_sender_path)
    encoder_recipient = joblib.load(encoder_recipient_path)
    encoder_risk = joblib.load(encoder_risk_path)
    print("[IA] Modelos carregados com sucesso.")
except Exception as e:
    print(f"[IA] Erro ao carregar modelo ou encoders: {e}")
    model = None

def predict_risk(sender: str, recipient: str, amount_eth: float) -> str:
    if not model:
        print("[IA] Modelo indisponível.")
        return None

    try:
        sender_encoded = encoder_sender.transform([sender])[0]
    except:
        sender_encoded = 0

    try:
        recipient_encoded = encoder_recipient.transform([recipient])[0]
    except:
        recipient_encoded = 0

    features = [[sender_encoded, recipient_encoded, amount_eth]]

    try:
        prediction = model.predict(features)[0]
        label = encoder_risk.inverse_transform([prediction])[0]
        return str(label).strip().lower()
    except Exception as e:
        print(f"[IA] Erro na previsão: {e}")
        return None
