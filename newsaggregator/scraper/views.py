from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date
from django.db.models import Q

def home(request):
    return HttpResponse("<h1>Welcome to the News API</h1><p>Use /api/articles/ to view the articles.</p>")

# Management command view for categorizing news
def categorize_news(request):
    input_file = r'C:\Users\Tushar upadhyay\OneDrive\Desktop\my projects\django\si-news\news_articles.csv'
    df = pd.read_csv(input_file)

    categories = ['World', 'Politics', 'Business', 'Technology', 'Entertainment', 'Sports']

    # Sample training data for the model
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
    
    return HttpResponse(f'Categorized news articles saved to {output_file}')

# REST API for listing and creating articles
class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'date']
    search_fields = ['title', 'summary']
    ordering_fields = ['date']
    ordering = ['-date']

# REST API for retrieving an individual article
class ArticleDetail(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

def article_list(request):
    # Get query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    
    # Validate date inputs
    try:
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Query all articles with optional filters
    articles = Article.objects.all()
    if start_date:
        articles = articles.filter(date__gte=start_date)
    if end_date:
        articles = articles.filter(date__lte=end_date)
    if category:
        articles = articles.filter(category=category)  # Ensure 'category' is a field in your model

    # Debugging: Print SQL query and count of articles
    print("SQL Query:", str(articles.query))
    print("Number of articles:", articles.count())

    articles_list = list(articles.values('id', 'title', 'summary', 'date', 'origin', 'url', 'category'))
    return JsonResponse({'articles': articles_list})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    article_data = {
        'id': article.id,
        'title': article.title,
        'summary': article.summary,
        'date': article.date,
        'origin': article.origin,
        'url': article.url,
        'category': article.category
    }
    return JsonResponse({'article': article_data})

def article_search(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'No query parameter provided'}, status=400)

    articles = Article.objects.filter(
        Q(title__icontains=query) | Q(summary__icontains=query)
    ).values('id', 'title', 'summary', 'date', 'origin', 'url', 'category')

    articles_list = list(articles)
    return JsonResponse({'articles': articles_list})
