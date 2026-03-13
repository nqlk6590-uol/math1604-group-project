import pandas as pd

# load dataset
df = pd.read_csv("../data/dataset.csv")

# remove duplicate rows
df = df.drop_duplicates()

# remove rows with missing values
df = df.dropna()

# reset index
df = df.reset_index(drop=True)

# save cleaned data
df.to_csv("../output/cleaned_data_M1.csv", index=False)

print("Data cleaning completed.")
