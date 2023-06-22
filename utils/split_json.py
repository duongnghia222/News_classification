import json

# Load the data from the large file
with open('../news_links_vietnambiz.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find the midpoint of the data
midpoint = len(data) // 2

# Split the data into two halves
data1 = data[:midpoint]
data2 = data[midpoint:]

# Write the first half of the data to a new file
with open('../news_links_vietnambiz_1.json', 'w', encoding='utf-8') as f:
    json.dump(data1, f, ensure_ascii=False, indent=4)

# Write the second half of the data to another new file
with open('../news_links_vietnambiz_2.json', 'w', encoding='utf-8') as f:
    json.dump(data2, f, ensure_ascii=False, indent=4)
