# Page Pulse Audit API

A production-ready URL Audit Service built using **FastAPI**. This API validates a URL, fetches the webpage, extracts important information such as the page title, response time, status code, and content length, and returns the results in JSON format. The project also includes caching, rate limiting, structured logging, unit testing, and GitHub Actions for continuous integration.

---

## Features

- URL validation using Pydantic
- FastAPI REST API
- Fetch webpage details
- Extract HTML page title
- Measure response time
- Return HTTP status code
- Return page content length
- 5-second request timeout
- 10-minute in-memory caching
- Rate limiting (10 requests per minute)
- Structured logging with Request IDs
- Unit testing using Pytest
- GitHub Actions CI workflow

---

## Technologies Used

- Python 3.14
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- Cachetools
- SlowAPI
- Pytest
- HTTPX
- Python-dotenv

---

## Project Structure

```
page-pulse-audit/
│
├── app/
│   ├── cache.py
│   ├── limiter.py
│   └── logger.py
│
├── tests/
│   └── test_api.py
│
├── logs/
│
├── .github/
│   └── workflows/
│       └── python.yml
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/eepu-divya/page-pulse-audit.git
```

Move to the project directory

```bash
cd page-pulse-audit
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI server

```bash
uvicorn main:app --reload
```

Application URL

```
http://127.0.0.1:8000
```

Swagger API Documentation

```
http://127.0.0.1:8000/docs
```

---

## API Endpoint

### POST `/audit`

Audits a webpage and returns useful metadata.

### Request

```json
{
  "url": "https://example.com"
}
```

### Response

```json
{
  "cached": false,
  "data": {
    "url": "https://example.com",
    "status_code": 200,
    "title": "Example Domain",
    "response_time_seconds": 0.215,
    "content_length": 559
  }
}
```

If the same URL is requested again within 10 minutes, the response is served from the cache.

---

## Running Tests

Run all unit tests

```bash
pytest
```

or

```bash
pytest -v
```

---

## Logging

Application logs are stored in:

```
logs/app.log
```

Each request records:

- Request ID
- URL
- Status Code
- Response Time
- Cache Status

---

## Rate Limiting

The API limits each client to:

```
10 requests per minute
```

If the limit is exceeded, the API returns:

```
429 Too Many Requests
```

---

## Caching

Successful audit results are cached for:

```
10 minutes
```

This reduces repeated network requests and improves performance.

---

## Continuous Integration

GitHub Actions automatically:

- Installs dependencies
- Runs unit tests
- Validates the project on every push and pull request

---

## Future Improvements

- Redis-based distributed caching
- Asynchronous HTTP requests using AsyncClient
- Docker support
- Authentication with API Keys
- Prometheus monitoring
- Health check endpoint
- Cloud deployment with Kubernetes

---

## AI Usage Statement

AI tools (ChatGPT) were used to assist with understanding FastAPI concepts, improving project structure, debugging issues, and reviewing documentation. The implementation, testing, modifications, and final verification of the project were completed manually.

---

## Author

**Eepu Divya**

B.Tech Graduate

Python | FastAPI | Machine Learning | Data Analytics
