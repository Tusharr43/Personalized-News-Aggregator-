from django.core.management.base import BaseCommand
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class Command(BaseCommand):
    help = 'Categorize news articles and save to a new CSV file'

    def handle(self, *args, **kwargs):
        input_file = r'C:\Users\Tushar upadhyay\OneDrive\Desktop\my projects\django\si-news\news_articles.csv'
        df = pd.read_csv(input_file)

        categories = ['World', 'Politics', 'Business', 'Technology', 'Entertainment', 'Sports']

        training_data = pd.DataFrame({
            'Title': ['Russian sanctions', 'New tech trends', 'Oscars highlights', 'Stock market crash'],
            'Category': ['World', 'Technology', 'Entertainment', 'Business']
        })

        X_train = training_data['Title']
        y_train = training_data['Category']

        model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        model.fit(X_train, y_train)

        df['Category'] = model.predict(df['Title'])

        output_file = r'C:\Users\Tushar upadhyay\OneDrive\Desktop\my projects\django\si-news\categorized_news_articles.csv'
        df.to_csv(output_file, index=False)

        self.stdout.write(self.style.SUCCESS(f'Categorized news articles saved to {output_file}'))
