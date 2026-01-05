import pandas as pd

# Load dataset
df = pd.read_csv("../dataset/student_success_dataset.csv")

# Show first 5 rows
print(df.head())

# Show column names
print("\nColumns in dataset:")
print(df.columns)

# Show dataset shape
print("\nDataset shape (rows, columns):")
print(df.shape)
