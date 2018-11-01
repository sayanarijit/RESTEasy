from pprint import pprint
from resteasy import RESTEasy
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


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
        title = self.anime.strip().replace(
            ' - MyAnimeList.net', '') if self.found else None
        return dict(title=title)


parser = MyHTMLParser()

api = RESTEasy(base_url='https://myanimelist.net', decoder=parser.parse)

pprint(api.route('anime', 1).get())
