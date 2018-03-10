# RESTEasy

[![PyPI version](https://img.shields.io/pypi/v/resteasy.svg)](https://pypi.python.org/pypi/resteasy)
[![Build Status](https://travis-ci.org/rapidstack/RESTEasy.svg?branch=master)](https://travis-ci.org/rapidstack/RESTEasy)
[![Join the chat at https://gitter.im/rapidstack/RESTEasy](https://badges.gitter.im/rapidstack/RESTEasy.svg)](https://gitter.im/rapidstack/RESTEasy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


REST API calls made easier


### Installation

```bash
pip install resteasy
```

### Usage and examples

* Import

```python
from resteasy import RESTEasy, json

api = RESTEasy(base_url='https://api.example.com',
               auth=('user', '****'),
               verify=False, cert=None, timeout=None,
               encoder=json.dumps, decoder=json.loads)
```

* Example 1: GitHub Jobs

```python
api =  RESTEasy(base_url='https://jobs.github.com')

positions = api.route('positions.json')
positions.get(description='python', full_time=True)

# GET https://jobs.github.com/positions.json?description=python&full_time=1
```

* Example 2: Jikan animes

```python
api = RESTEasy(base_url='https://api.jikan.me')

### One way
api.route('anime/1').get()

### Another way
api.route('anime', 1).get()

### Yet another way
api.route('anime').route(1).get()

### This is the last way I swear
api.route('anime').route(1).do('GET')

# GET https://api.jikan.me/anime/1
```

* Example 3: Chuck Norris jokes

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

* Example 4: All methods: GET, POST, PUT, PATCH, DELETE

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

