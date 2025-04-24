# File: backend/webhook.py

import requests

WEBHOOK_URL = "http://localhost:9000/alert"  # Altere para o seu destino real

def send_webhook(payload: dict):
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"[Webhook] Status: {response.status_code}")
    except Exception as e:
        print(f"[Webhook] Failed to send: {e}")
