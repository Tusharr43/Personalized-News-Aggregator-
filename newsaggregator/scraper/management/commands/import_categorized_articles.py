from django.core.management.base import BaseCommand
import pandas as pd
from scraper.models import Article
from datetime import datetime

class Command(BaseCommand):
    help = 'Import categorized articles from a CSV file into the database'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\Tushar upadhyay\OneDrive\Desktop\my projects\django\si-news\categorized_news_articles.csv'
        
        # Load the CSV file
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        # Print the columns to verify
        self.stdout.write(self.style.SUCCESS(f'Columns in CSV: {list(df.columns)}'))

        # Ensure all required columns are present
        required_columns = ['Title', 'Summary', 'Publication Date', 'Source', 'URL', 'Category']
        if not all(col in df.columns for col in required_columns):
            self.stderr.write(self.style.ERROR(f'Missing required columns in the CSV file'))
            return

        # Function to convert date format
        def convert_date(date_str):
            try:
                # Adjust the format as needed
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            except ValueError:
                # Handle the case where the date is in an unexpected format
                self.stderr.write(self.style.ERROR(f'Invalid date format: {date_str}'))
                return None

        # Import or update articles
        for _, row in df.iterrows():
            article_date = convert_date(row['Publication Date'])
            if article_date:  # Only update if the date is valid
                Article.objects.update_or_create(
                    title=row['Title'],
                    defaults={
                        'summary': row['Summary'],
                        'date': article_date,
                        'origin': row['Source'],
                        'url': row['URL'],
                        'category': row['Category']
                    }
                )
            
        self.stdout.write(self.style.SUCCESS('Categorized articles imported successfully.'))
