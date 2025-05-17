# drop_transactions.py
# drop_transactions.py
from backend.database import TransactionRecord, engine

TransactionRecord.__table__.drop(engine)
print("Tabela 'transactions' excluída com sucesso.")
