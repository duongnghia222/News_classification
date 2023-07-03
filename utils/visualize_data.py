import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
df = pd.read_csv('../data/raw_data/raw_data_vietnambiz.csv', encoding='utf-8-sig')

# Count the number of words in each article's content
df['Word Count'] = df['Content'].apply(lambda x: len(str(x).split()))

# Calculate statistics for word count
word_count_statistics = df['Word Count'].describe()

print(word_count_statistics)

# Plot histogram for word count
plt.hist(df['Word Count'], bins=20, color='skyblue', edgecolor='black')
plt.title('Histogram of Word Count')
plt.xlabel('Word Count')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Load data from CSV file
df = pd.read_csv('../data/raw_data/raw_data_vietnambiz.csv', encoding='utf-8-sig')

# Count the occurrence of each unique label
label_counts = df['Label'].value_counts()
print(label_counts.describe())

# Loop over each unique label and print its count
for label, count in label_counts.items():
    print(f"Label: {label}, Count: {count}")

