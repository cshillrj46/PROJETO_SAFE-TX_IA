# In progress...
# 🛡️ SafeTX — AI-powered Crypto Transaction Shield

**SafeTX** is a modern, AI-driven browser extension designed to protect crypto users from scams and malicious transactions in real time.  
Built with security in mind, it introduces an intelligent **delay system** combined with fraud detection to stop risky transactions before they hit the blockchain.

---

## 🚨 Problem

In the Web3 world, one click can cost thousands.  
Phishing links, fake dApps, and social engineering are everywhere — and traditional wallet tools offer no second chance.

---

## ✅ Our Solution

SafeTX integrates directly with your wallet to provide:
- ⏱️ **Delay Buffer** for all transactions (customizable)
- 🧠 **AI-based risk classification** of each transaction
- 🔁 **Manual reclassification** for users and analysts
- 📬 **Email and webhook alerts** for high-risk operations
- 📈 **Full transaction history** with audit logs
- 👥 B2B-ready SDKs (coming soon)

---

## 🧠 Powered by AI

SafeTX uses a trained machine learning model to classify transactions as:
- `safe`
- `suspicious`
- `fraudulent`

It learns continuously based on user feedback and manual reclassifications, improving over time.  
Algorithms used include `RandomForestClassifier` and `SMOTE` balancing for high accuracy.

---

## 💻 Tech Stack

- **Backend**: FastAPI + Scikit-learn + PostgreSQL  
- **Frontend**: React + Tailwind CSS  
- **Notifications**: Email (SMTP) and Webhooks  
- **Language**: Python 3.11

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL running
- [MetaMask](https://metamask.io/) or compatible wallet (for frontend demo)

### Clone and Run

```bash
git clone https://github.com/cshillrj46/SafeTX.git
cd SafeTX
