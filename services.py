import warnings, urllib, html5lib
from html5lib.treebuilders import dom

class GoogleForexRateClient():
    def url_for(self, currency1, currency2):
        """builds a get request for google's currency converter from the two currencie"""
        url = "http://www.google.com/finance/converter?a=1&from=" + currency1 + "&to=" + currency2
        return url


    def build_dom_from(self, html):
        """builds a dom from a html string"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            parser = html5lib.HTMLParser(tree=dom.TreeBuilder)
            tree = parser.parse(html)
            # Normalise the tree.  This basically cleans up the
            # text nodes inside which makes our life easier.
            tree.normalize()
            return tree

    def scrape_url_for_response(self,tree):
        # tags with the class of "row")
        rows = [div for div in tree.getElementsByTagName("div")\
            if div.getAttribute("id").strip() == "currency_converter_result"]

        from_currency1 =  rows[0].childNodes[0].data
        to_currency2 = rows[0].childNodes[1].childNodes[0].data
        #TODO build a currency object that is (CUR,amt)
        return (from_currency1,to_currency2)

    def pull_response_for(self, currency1, currency2):
        #TODO be able to toggle server for testing
        url = self.url_for(currency1, currency2)
        response = urllib.urlopen(url)
        return response.read()

    def get_rate(self, currency1, currency2):
        """converts one unit of currency1 to currency2"""
        data = self.pull_response_for(currency1, currency2)
        tree = self.build_dom_from(data)
        return self.scrape_url_for_response(tree)


