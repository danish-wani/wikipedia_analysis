# Wikipedia Analysis API

This project is a Django-based API designed to interact with Wikipedia to perform specific text analysis tasks. It allows users to fetch the frequency of words in Wikipedia articles based on user queries and stores the search history.

## Table of Contents

- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Utility Functions](#utility-functions)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Setup

### Prerequisites

- Python 3.x
- Django 3.x
- Django REST Framework (if using DRF for API development)

### Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations to set up the database:
   ```bash
    python manage.py makemigrations
   ```
   ```bash
   python manage.py migrate
   ```
5. Run the server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### 1. Word Frequency Analysis Endpoint

- **URL**: `/word_frequency/`
- **Method**: `GET`
- **Parameters**:
 - `topic` (required): A string representing the subject of a Wikipedia article.
 - `n` (optional): An integer specifying the number of top frequent words to return. Default is 10.
- **Response**:
 - On success:
    ```json
    {
        "topic": "database sharding",
        "word_frequency": [
            {
                "word": "frequency"
            }
        ]
    }
    ```
 - On failure:
    ```json
    {
        "error": "error message"
    }
    ```

### 2. Search History Endpoint

- **URL**: `/search_history/`
- **Method**: `GET`
- **Parameters**:
 - `page` (optional): An integer specifying the page number for pagination. Default is 1.
 - `page_size` (optional): An integer specifying the number of results per page. Default is 10.
- **Response**:
 - On success:
    ```json
    {
        "data": [
            {
                "topic": "database sharding",
                "word_frequency": [
                    {
                        "word": "frequency"
                    }
                ],
                "created_at": "2023-04-01 12:00:00"
            }
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 2,
            "total_results": 20,
            "next_page": 2,
            "previous_page": null
        }
    }
    ```

## Utility Functions

### WikiAnalysisUtil

This utility class handles the business logic of the Wikipedia Analysis API. It includes methods for fetching Wikipedia articles, analyzing word frequencies, and saving search results.

- **Methods**:
 - `clean_input_topic(topic: str) -> str`: Cleans the input topic by converting it to lowercase and removing leading/trailing spaces.
 - `word_frequency_analysis(text: str) -> list`: Analyzes the given text to find the most common words and returns the top `n` words.
 - `fetch_wikipedia_article() -> dict`: Fetches the text of a Wikipedia article based on the provided topic.
 - `process() -> dict`: Runs the analysis and saves the result.

## Testing

To run tests, execute the following command in the project directory:

```bash
python manage.py test
```

## Contributing

Contributions are welcome. Please submit a pull request with your changes.

## License

To be added.