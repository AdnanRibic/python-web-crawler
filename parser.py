from html.parser import HTMLParser
from urllib import parse
# In this class we will give it html file and it will reutrn us all links
class link_parser(HTMLParser):
    def __init__(self, base, url):
        super().__init__()
        self.base_url = base
        self.page_url = url
        self.links = set()

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attributes):
        # letter a is for ancor(links in html)
        if tag == 'a':
            for (attribute, value) in attributes:
                if attribute == 'href':
                    # Because sometimes url does not have full link, we need to check it out and add missing url(base_url: http://www.teleconr.no)
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
    # Returns us results with links
    def page_links(self):
        return self.links

    def error(self, message):
        pass