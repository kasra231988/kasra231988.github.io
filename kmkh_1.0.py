# spam_filter.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
from fastapi import FastAPI
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
] * 60  # 5 * 60 = 300 spam samples

ham_texts = [
    "Hi John, are we still meeting tomorrow?",
    "Please find the attached project report.",
    "Let's have lunch at 1pm.",
    "Your order has been shipped and will arrive soon.",
    "Thanks for your help yesterday."
] * 60  # 5 * 60 = 300 ham samples

data = pd.DataFrame({
    "text": spam_texts + ham_texts,
    "label": [1] * 300 + [0] * 300  # 1=spam, 0=ham
})

# =============================
# 2. پردازش و آموزش مدل
# =============================
X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

clf = LogisticRegression()
clf.fit(X_train_tfidf, y_train)

y_pred = clf.predict(X_test_tfidf)
print(classification_report(y_test, y_pred))

# =============================
# 3. ذخیره مدل و وکتورایزر
# =============================
joblib.dump(clf, "spam_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

# =============================
# 4. API با FastAPI
# =============================
app = FastAPI()

clf = joblib.load("spam_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

@app.post("/predict/")
async def predict(email: str):
    X = vectorizer.transform([email])
    prediction = clf.predict(X)[0]
    return {"prediction": "spam" if prediction == 1 else "ham"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
