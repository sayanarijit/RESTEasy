from pprint import pprint
from resteasy import RESTEasy

api = RESTEasy(base_url='https://jsonplaceholder.typicode.com')

posts = api.route('posts')

### GET (fetch resources)
pprint(posts.get())
pprint(posts.get(userId=1))
pprint(posts.route(1).get())
pprint(posts.route(1).do('GET'))
pprint(posts.route(1).do('GET', {'userId': 1}))

### POST (create a resource)
pprint(posts.post(title='foo', body='bar', userId=1))
pprint(posts.do('POST', {'title': 'foo', 'body': 'bar', 'userId': 1}))

### PUT & PATCH (update a resource)
pprint(posts.route(1).put(id=1, title='foo', body='bar', userId=1))
pprint(posts.route(1).do('PUT', {'id': 1, 'title': 'foo', 'body': 'bar', 'userId': 1}))

pprint(posts.route(1).patch(title='foo'))
pprint(posts.route(1).do('PATCH', {'title': 'foo'}))

### DELETE (delete a resource)
pprint(posts.route(1).delete())
pprint(posts.route(1).do('DELETE'))
