import warnings, urllib, html5lib
from html5lib.treebuilders import dom

SERVER = "http://www.google.com/finance/converter?"
AMOUNT_PARAM = "a=1"
BASE_PARAM = "&from="
QUOTE_PARAM = "&to="

class GoogleForexRateClient():
    def _url_for(self, base, quote):
        """builds a get request for google's currency converter from the two currencie"""
        #TODO use a better string decorator
        return SERVER + AMOUNT_PARAM + BASE_PARAM + base + QUOTE_PARAM + quote

    def _build_dom_from(self, html):
        """builds a dom from a html string"""
        parser = html5lib.HTMLParser(tree=dom.TreeBuilder)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tree = parser.parse(html)
        tree.normalize()
        return tree

    def _scrape_url_for_response(self,tree):
        """ Pulls the desired data out of the dom """
        # TODO nicer scrape
        meaty_bits = [div for div in tree.getElementsByTagName("div")\
            if div.getAttribute("id").strip() == "currency_converter_result"][0]
        quote = meaty_bits.childNodes[1].childNodes[0].data
        amount = quote.split()[0]
        return amount

    def _pull_response_for(self, base, quote):
        """pulls the response from the server given two currencies"""
        #TODO be able to toggle server for testing
        url = self._url_for(base, quote)
        response = urllib.urlopen(url)
        return response.read()

    def get_rate(self, base, quote):
        """gives exchange rate for a currecny pair"""
        data = self._pull_response_for(base, quote)
        tree = self._build_dom_from(data)
        amount = self._scrape_url_for_response(tree)
        return amount



