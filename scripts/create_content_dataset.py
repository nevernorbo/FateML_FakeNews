import pandas as pd

# Data with scraped article content
dataset = pd.read_csv('../data/FakeNewsNetWithArticleContent.csv')

# Remove duplicated titles
dataset.drop_duplicates(subset='title', inplace=True)
# Remove empty news_url rows
dataset.dropna(subset='news_url', inplace=True)
# Remove rows with invalid article content
dataset = dataset.dropna(subset='article_content', inplace=False)
dataset = dataset[dataset['article_content'] != '[ERROR]']

# Select 160 random rows where real == 1
real_sample = dataset[dataset['real'] == 1].sample(n=min(160, dataset[dataset['real'] == 1].shape[0]), random_state=42)

# Select all rows where real == 0
fake_all = dataset[dataset['real'] == 0]

# Concatenate the two DataFrames
combined = pd.concat([real_sample, fake_all], ignore_index=True)

print(combined)

# Save to a new CSV file
combined.to_csv('../data/FakeNewsNetContent.csv', index=False)

print('Saved new dataset')