# File: backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from fastapi.responses import JSONResponse
from backend.database import TransactionRecord, SessionLocal, init_db
from backend.webhook import send_webhook
from backend.email_service import send_email_alert
from fastapi import HTTPException
from backend.database import ReclassificationLog
from backend.ai_model import predict_risk

app = FastAPI()
init_db()

# Enum for risk levels
class RiskLevel(str, Enum):
    safe = "safe"
    suspicious = "suspicious"
    high_risk = "high-risk"

# Input model for transaction analysis
class TransactionInput(BaseModel):
    sender: str
    recipient: str
    amount_eth: float

# Analyze transaction and classify its risk level
@app.post("/analyze", response_model=RiskLevel)
def analyze_transaction(tx: TransactionInput):
    db = SessionLocal()

    # Step 1: Determine risk level
    predicted = predict_risk(tx.sender, tx.recipient, tx.amount_eth)
    risk = RiskLevel(predicted)

    # Step 2: Save to database
    db.add(TransactionRecord(
        sender=tx.sender,
        recipient=tx.recipient,
        amount_eth=tx.amount_eth,
        risk=risk
    ))
    db.commit()

    # Step 3: Send webhook if high-risk
    if risk == RiskLevel.high_risk:
        send_webhook({
            "sender": tx.sender,
            "recipient": tx.recipient,
            "amount_eth": tx.amount_eth,
            "risk": risk
        })

        send_email_alert(
            recipient_email="cristianohill35@gmail.com",  # 🔁 pode ser o mesmo que enviou
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

# Return transaction history
@app.get("/history")
def get_history():
    db = SessionLocal()
    records = db.query(TransactionRecord).all()
    return JSONResponse(content=[
        {
            "id": r.id,
            "sender": r.sender,
            "recipient": r.recipient,
            "amount_eth": r.amount_eth,
            "risk": r.risk
        } for r in records
    ])

class ReclassificationInput(BaseModel):
    new_risk: RiskLevel
    reason: str
    reclassified_by: str

@app.patch("/reclassify/{tx_id}")
def reclassify_transaction(tx_id: int, payload: ReclassificationInput):
    db = SessionLocal()

    # Buscar transação
    tx = db.query(TransactionRecord).filter(TransactionRecord.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Salvar log da reclassificação
    log = ReclassificationLog(
        transaction_id=tx.id,
        old_risk=tx.risk,
        new_risk=payload.new_risk,
        reason=payload.reason,
        reclassified_by=payload.reclassified_by
    )
    db.add(log)

    # Atualizar o risco da transação original
    tx.risk = payload.new_risk
    db.commit()

    return {"status": "reclassified", "tx_id": tx.id}

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
