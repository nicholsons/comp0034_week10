# Using a REST API in a Flask app

## Introduction

In this activity we will use a third party API to provide content for our Flask app.

We will add recycling news items to the home page.

There are many published API’s, most require registration, many are free

- [Programmable web API directory](https://www.programmableweb.com/apis/directory)
- [Any API](https://any-api.com/)
- [API list](https://apilist.fun/)

For this activity we are going to use recycling related stories from
[Google News API](https://newsapi.org/docs/get-started).

To use this you need to register to get an API key.

To understand the API parameters and results refer to
the [documentation for the 'everything' endpoint](https://newsapi.org/docs/endpoints/everything)

Due to the number of stories returned the code in the following example is limited to the last hour.

## Modify the homepage route

Modify the index route to query the API. Pass the results, which are in JSON format, to the index template.

```python
from datetime import datetime, timedelta
import requests
from flask import Blueprint, render_template
from flask_login import current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/', defaults={'name': 'Anonymous'})
@main_bp.route('/<name>')
def index(name):
    if not current_user.is_anonymous:
        name = current_user.firstname

    api_key = ''  # place your API key here
    search = 'recycling'
    # 'to' date and optional time for the newest article allowed.
    newest = datetime.today().strftime('%Y-%m-%d')
    # 'from' date and optional time for the oldest article allowed in ISO 8601 format e.g. 2021-02-20
    oldest = (datetime.today() - timedelta(hours=1)).strftime('%Y-%m-%d')
    sort_by = 'publishedAt'
    url = f'https://newsapi.org/v2/everything?q={search}&from={oldest}&to={newest}&sortBy={sort_by}'

    response = requests.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(api_key)
    })
    news = response.json()
    return render_template('index.html', title='Home page', name=name, news=news)
```

## Modify the home page template

Modify the homepage template, `index.html` to iterate through the list of news stories and display the title as a
hyperlink to the story.

```html
{% extends 'layout.html' %}
{% block content %}
    <h1>{{ title }}</h1>
    <p>Welcome {{ name }}</p>
    <br>
    <h2>Latest recycling news</h2>
    {% for article in news['articles'] %}
        <p><a href="{{ article.url|e }}">{{ article.title|e }}</a></p>
    {% endfor %}
{% endblock %}
```