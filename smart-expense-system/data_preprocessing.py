import pandas as pd
df_temp=pd.read_csv("transactions.csv")
df=df_temp[["category","description"]].copy()
print(df["category"].unique())

extra_data = [
    # food
    ("swiggy order", "food"),
    ("zomato dinner", "food"),
    ("restaurant lunch", "food"),
    ("pizza order", "food"),
    ("food delivery", "food"),

    # transport
    ("uber ride", "transport"),
    ("ola cab", "transport"),
    ("bus ticket", "transport"),
    ("train ticket", "transport"),
    ("auto fare", "transport"),

    # shopping
    ("amazon shopping", "shopping"),
    ("flipkart purchase", "shopping"),
    ("online order", "shopping"),
    ("clothes shopping", "shopping"),
    ("mall purchase", "shopping"),

    # entertainment
    ("movie ticket", "entertainment"),
    ("netflix subscription", "entertainment"),
    ("spotify subscription", "entertainment"),
    ("concert ticket", "entertainment"),
    ("game purchase", "entertainment"),

    # technology
    ("laptop purchase", "technology"),
    ("mobile phone", "technology"),
    ("software subscription", "technology"),
    ("electronics purchase", "technology"),
    ("computer accessories", "technology"),
]

extra_df = pd.DataFrame(extra_data, columns=["description", "category"])

df = pd.concat([df, extra_df], ignore_index=True)
# top_categories = df["category"].value_counts().head(5).index
# print(top_categories)
# df=df[df["Category"].isin(top_categories)]
print(df["category"].value_counts())
# print(df.head(100))
# print(df.columns)

def import_data():
    return df
