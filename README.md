# RESTEasy

REST API calls made easier

[![PyPI version](https://img.shields.io/pypi/v/resteasy.svg)](https://pypi.org/project/resteasy)
[![Python versions](https://img.shields.io/pypi/pyversions/resteasy.svg)](https://pypi.org/project/resteasy)
[![Build status](https://travis-ci.org/sayanarijit/resteasy.svg?branch=master)](https://travis-ci.org/sayanarijit/resteasy)
[![Code coverage](https://codecov.io/gh/sayanarijit/resteasy/branch/master/graph/badge.svg)](https://codecov.io/gh/sayanarijit/resteasy)

- [RESTEasy](#resteasy)
    - [Installation](#installation)
    - [Usage and examples](#usage-and-examples)
        - [Import](#import)
        - [Example 1: GitHub Jobs](#example-1-github-jobs)
        - [Example 2: All methods: GET, POST, PUT, PATCH, DELETE](#example-2-all-methods-get-post-put-patch-delete)
        - [Example 3: Chuck Norris jokes](#example-3-chuck-norris-jokes)
        - [Example 4: Using custom decoder: Parsing MyAnimeList HTML content](#example-4-using-custom-decoder-parsing-myanimelist-html-content)
    - [Debugging](#debugging)
    - [Exceptions](#exceptions)

## Installation

```bash
pip install resteasy
```

## Usage and examples

### Import

```python
from resteasy import RESTEasy, json

api = RESTEasy(endpoint='https://api.example.com',
               auth=('user', '****'),
               verify=False, cert=None, timeout=None,
               allow_redirects=True,
               encoder=json.dumps, decoder=json.loads, debug=False)
               
# optional timeout
api.timeout = 60
```

### Example 1: GitHub Jobs

```python
api =  RESTEasy(endpoint='https://jobs.github.com')

positions = api.route('positions.json')

positions.get(description='python', full_time=1)
# or
positions.do('GET', {'description': 'python', 'full_time': 1})

# GET https://jobs.github.com/positions.json?description=python&full_time=1
```

### Example 2: All methods: GET, POST, PUT, PATCH, DELETE

```python
from resteasy import RESTEasy

api = RESTEasy(endpoint='https://jsonplaceholder.typicode.com')

posts = api.route('posts')

### GET (fetch resources)
posts.get()
posts.get(userId=1)
posts.route(1).get()

### POST (create a resource)
posts.post(title='foo', body='bar', userId=1)

### PUT & PATCH (update a resource)
posts.route(1).put(id=1, title='foo', body='bar', userId=1)
posts.route(1).patch(title='foo')

### DELETE (delete a resource)
posts.route(1).delete()
```

### Example 3: Chuck Norris jokes

```python
from __future__ import print_function
from resteasy import RESTEasy

api = RESTEasy(endpoint='https://api.chucknorris.io')


### Print a random joke
jokes = api.route('jokes')
random = jokes.route('random')
print(random.get())

# GET https://api.chucknorris.io/jokes/random


### Get all categories
categories = jokes.route('categories').get()
print(categories)

# GET https://api.chucknorris.io/jokes/categories


### Print a random joke from each category
for category in categories:
    random_joke = random.get(category=category)
    print(category, ':', random_joke['value'])

    # GET https://api.chucknorris.io/jokes/random?category=<category>
```

### Example 4: Using custom decoder: Parsing MyAnimeList HTML content

```python
from resteasy import RESTEasy
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    '''Custom HTML parser'''
    
    def handle_starttag(self, tag, attrs):
        '''Overriding abstract method'''
        if tag == 'title' and not self.found:
            self.found = True

    def handle_data(self, data):
        '''Overriding abstract method'''
        if self.found and self.anime is None:
            self.anime = data
    
    def parse(self, content):
        '''Parse content and return object'''
        self.found = False
        self.anime = None
        self.feed(content)
        title = self.anime.strip().replace(' - MyAnimeList.net', '') if self.found else None
        return dict(title=title)

parser = MyHTMLParser()

api = RESTEasy(endpoint='https://myanimelist.net', decoder=parser.parse)

### One way
api.route('anime/1').get()

### Another way
api.route('anime', 1).get()

### Yet another way
api.route('anime').route(1).get()

### This is the last way I swear
api.route('anime').route(1).do('GET')

### Just kidding...
api.route('anime').route(1).request('GET').json()

# GET https://myanimelist.net/anime/1
```

## Debugging

To enable debugging just pass or set ***debug=True***

```python
api.debug = True
```

Once debugging is set to 'True', Every HTTP call will return debug information instead of doing the actual request

```python
>>> posts.debug = True
>>> posts.get(userId=1)
{'endpoint': 'https://jsonplaceholder.typicode.com/posts',
 'params': {'userId': 1},
 'method': 'GET',
 'timeout': None}
```

## Exceptions

* As this package uses requests module to perform HTTP calls, so all exceptions will be raised by requests module itself.
