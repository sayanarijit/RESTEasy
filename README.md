# RESTEasy

REST API calls made easier

[![PyPI version](https://img.shields.io/pypi/v/resteasy.svg)](https://pypi.python.org/pypi/resteasy)
[![Build Status](https://travis-ci.org/rapidstack/RESTEasy.svg?branch=master)](https://travis-ci.org/rapidstack/RESTEasy)
[![Join the chat at https://gitter.im/rapidstack/RESTEasy](https://badges.gitter.im/rapidstack/RESTEasy.svg)](https://gitter.im/rapidstack/RESTEasy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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

api = RESTEasy(base_url='https://api.example.com',
               auth=('user', '****'),
               verify=False, cert=None, timeout=None,
               encoder=json.dumps, decoder=json.loads, debug=False)
               
# optional timeout
api.timeout = 60
```

### Example 1: GitHub Jobs

```python
api =  RESTEasy(base_url='https://jobs.github.com')

positions = api.route('positions.json')

positions.get(description='python', full_time=1)
# or
positions.do('GET', {'description': 'python', 'full_time': 1})

# GET https://jobs.github.com/positions.json?description=python&full_time=1
```

### Example 2: All methods: GET, POST, PUT, PATCH, DELETE

```python
api = RESTEasy(base_url='https://jsonplaceholder.typicode.com')

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

api = RESTEasy(base_url='https://api.chucknorris.io')


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
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.found = False
        self.anime = None

    def handle_starttag(self, tag, attrs):
        '''Inherited method'''
        if tag == 'title' and not self.found:
            self.found = True
    
    def handle_data(self, data):
        '''Inherited method'''
        if self.found and self.anime is None:
            self.anime = data
    
    def parse(self, content):
        '''Parse content and return object'''
        self.feed(content)
        return self
    
    def __repr__(self):
        return 'Anime({})'.format(self.anime.strip() if self.found else '')

parser = MyHTMLParser()

api = RESTEasy(base_url='https://myanimelist.net', decoder=parser.parse)

### One way
api.route('anime/1').get()

### Another way
api.route('anime', 1).get()

### Yet another way
api.route('anime').route(1).get()

### This is the last way I swear
api.route('anime').route(1).do('GET')

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
 'kwargs': {'userId': 1},
 'method': 'GET',
 'session': <requests.sessions.Session at 0x7f1e8c8bfeb8>}
```

## Exceptions

* As this package uses requests module to perform HTTP calls, most exceptions will be raised by requests module itself.

* In case API server returns HTTP status code outside the range of 200-299, It will raise ***resteasy.HTTPError***

* In case the returned content by API server is not parsable, It will raise ***resteasy.InvalidResponseError***
