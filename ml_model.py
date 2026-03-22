from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from data_preprocessing import import_data
import pandas as pd

df=import_data()

labels=df["category"]
texts=df["description"]

vectorizer = TfidfVectorizer(ngram_range=(1,2),min_df=1)
X=vectorizer.fit_transform(texts)

model=MultinomialNB(alpha=0.5)
model.fit(X,labels)

def predict_category(description):
    X_input = vectorizer.transform([description])

    probs=model.predict_proba(X_input)
    confidence=probs.max()
    if confidence<0.3:
        return "other"
    return model.predict(X_input)[0]

def test_manual_inputs():
    print("\n🧪 Manual Testing:\n")

    test_cases = [
        # food
        "swiggy order",
        "zomato dinner",
        "pizza delivery",

        # transport
        "uber ride",
        "ola cab",
        "bus ticket",

        # shopping
        "amazon shopping",
        "flipkart purchase",
        "buy clothes",

        # entertainment
        "movie ticket",
        "netflix subscription",
        "concert ticket",

        # technology
        "laptop purchase",
        "mobile phone",
        "software subscription",

        # edge cases
        "atm withdrawal",
        "random payment",
        "unknown transaction"
    ]

    for text in test_cases:
        prediction = predict_category(text)
        print(f"{text:<25} → {prediction}")


if __name__ == "__main__":

    test_manual_inputs()

