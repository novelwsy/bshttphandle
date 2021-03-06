import formatter
import htmllib

nilfmter = formatter.NullFormatter()


class LinksExtractor(htmllib.HTMLParser):
    def __init__(self, fmter=nilfmter):
        htmllib.HTMLParser.__init__(self, fmter)
        self.links = []

    def start_a(self, attrs):
        if len(attrs) > 0:
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])

    def get_links(self):
        return self.links
