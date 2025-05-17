# File: backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.database import TransactionRecord, SessionLocal, init_db, ReclassificationLog
from backend.webhook import send_webhook
from backend.email_service import send_email_alert
from backend.ai_model import predict_risk

from datetime import datetime

app = FastAPI()
init_db()

# === CORS Setup ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Risk Level Enum ===
class RiskLevel(str, Enum):
    safe = "safe"
    suspicious = "suspicious"
    high_risk = "high-risk"

# === Input Model ===
class TransactionInput(BaseModel):
    sender: str
    recipient: str
    amount_eth: float

# === Analyze Transaction ===
@app.post("/analyze", response_model=RiskLevel)
def analyze_transaction(tx: TransactionInput):
    db = SessionLocal()
    print("[DEBUG] Analisando transação com regra + IA")

    # 1. Regra fixa
    if tx.amount_eth > 25:
        risk = RiskLevel.high_risk
        print(f"[DEBUG] Valor alto. Classificado como: {risk}")
    else:
        # 2. Modelo IA
        predicted = predict_risk(tx.sender, tx.recipient, tx.amount_eth)
        predicted = (predicted or "").strip().lower()
        print(f"[DEBUG] IA previu: {predicted}")

        valid_values = {rl.value for rl in RiskLevel}
        if predicted not in valid_values:
            print("[ERRO] Previsão inválida da IA. Usando 'suspicious'")
            risk = RiskLevel.suspicious
        else:
            risk = RiskLevel(predicted)

    # 3. Gravar no banco
    tx_record = TransactionRecord(
        sender=tx.sender,
        recipient=tx.recipient,
        amount_eth=tx.amount_eth,
        risk=risk,
        timestamp=datetime.utcnow()
    )
    db.add(tx_record)
    db.commit()

    # 4. Notificações
    if risk == RiskLevel.high_risk:
        send_webhook({
            "sender": tx.sender,
            "recipient": tx.recipient,
            "amount_eth": tx.amount_eth,
            "risk": risk
        })

        send_email_alert(
            recipient_email="cristianohill35@gmail.com",
            subject="🚨 SafeTX Alert: High-Risk Transaction Detected",
            content=(
                f"A high-risk transaction was detected:\n\n"
                f"Sender: {tx.sender}\n"
                f"Recipient: {tx.recipient}\n"
                f"Amount (ETH): {tx.amount_eth}\n"
                f"Risk Level: {risk}"
            )
        )

    return risk

# === Get Transaction History ===
@app.get("/history")
def get_history():
    db = SessionLocal()
    records = db.query(TransactionRecord).order_by(TransactionRecord.id).all()
    return JSONResponse(content=[
        {
            "id": r.id,
            "sender": r.sender,
            "recipient": r.recipient,
            "amount_eth": r.amount_eth,
            "risk": r.risk,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.timestamp else "N/A"
        } for r in records
    ])

# === Manual Reclassification ===
class ReclassificationInput(BaseModel):
    new_risk: RiskLevel
    reason: str
    reclassified_by: str

@app.patch("/reclassify/{tx_id}")
def reclassify_transaction(tx_id: int, payload: ReclassificationInput):
    db = SessionLocal()
    tx = db.query(TransactionRecord).filter(TransactionRecord.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    log = ReclassificationLog(
        transaction_id=tx.id,
        old_risk=tx.risk,
        new_risk=payload.new_risk,
        reason=payload.reason,
        reclassified_by=payload.reclassified_by
    )
    db.add(log)
    tx.risk = payload.new_risk
    db.commit()

    return {"status": "reclassified", "tx_id": tx.id}

# === Get Reclassification Logs ===
@app.get("/reclassifications")
def get_reclassifications():
    db = SessionLocal()
    logs = db.query(ReclassificationLog).all()
    return [
        {
            "id": r.id,
            "tx_id": r.transaction_id,
            "old_risk": r.old_risk,
            "new_risk": r.new_risk,
            "reason": r.reason,
            "reclassified_by": r.reclassified_by
        } for r in logs
    ]
