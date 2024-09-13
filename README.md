# Personalized-News-Aggregator-
# SI-News Aggregator

## Project Overview

This project is a news aggregator that scrapes news articles, categorizes them using machine learning, and provides a REST API to access the categorized news articles.

## Setup Instructions

1. **Clone the Repository**

    ```bash
    git clone <repository_url>
    cd si-news
    ```

2. **Create and Activate Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**

    ```bash
    python manage.py migrate
    ```

5. **Import Categorized Articles**

    ```bash
    python manage.py import_categorized_articles
    ```

6. **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

## API Endpoints

- **Home Page**: `/`
- **List and Create Articles**: `/api/articles/`
- **Retrieve Article**: `/api/articles/<id>/`
- **Search Articles**: `/api/articles/search/`
- **Categorize News**: `/api/categorize-news/`

## Testing

Use Postman or a similar tool to test the API endpoints.

## Screenshots / Video

Please refer to the `screenshots/` directory for screenshots and `video/` directory for the video of the APIs in action.

## License

This project is licensed under the MIT License.
