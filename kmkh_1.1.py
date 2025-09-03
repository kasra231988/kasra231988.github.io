# zimbra_spam_filter.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from fastapi import FastAPI, Request
import uvicorn

# =============================
# 1. ساخت دیتاست نمونه (300 ردیف)
# =============================
spam_texts = [
    "Congratulations! You won a free lottery ticket.",
    "Claim your free prize now!!!",
    "You have been selected for a cash reward.",
    "Win big money today, click here!",
    "Urgent! Update your bank details immediately."
] * 60  # 300 spam

ham_texts = [
    "Hi John, are we still meeting tomorrow?",
    "Please find the attached project report.",
    "Let's have lunch at 1pm.",
    "Your order has been shipped and will arrive soon.",
    "Thanks for your help yesterday."
] * 60  # 300 ham

data = pd.DataFrame({
    "text": spam_texts + ham_texts,
    "label": [1] * 300 + [0] * 300
})

# =============================
# 2. آموزش مدل
# =============================
X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.2, random_state=42
)
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
clf = LogisticRegression()
clf.fit(X_train_tfidf, y_train)

# ذخیره مدل
joblib.dump(clf, "spam_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

# =============================
# 3. API برای استفاده در Zimbra
# =============================
app = FastAPI()
clf = joblib.load("spam_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

@app.post("/predict/")
async def predict(request: Request):
    email_raw = await request.body()
    email_text = email_raw.decode("utf-8", errors="ignore")

    X = vectorizer.transform([email_text])
    prediction = clf.predict(X)[0]

    # خروجی برای Zimbra -> با هدر
    if prediction == 1:
        return {"header": "X-Spam-ML-Score: yes"}
    else:
        return {"header": "X-Spam-ML-Score: no"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
