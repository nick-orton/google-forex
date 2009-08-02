#!/usr/bin/python
import warnings
import urllib
import html5lib
from html5lib.treebuilders import dom
import sys

class GoolgeCurrencyConverter():
    def url_for(self, currency1, currency2):
        """builds a get request for google's currency converter from the two currencie"""
        url = "http://www.google.com/finance/converter?a=1&from=" + currency1 + "&to=" + currency2
        return url


    def get_tree_from(self, html):
        """builds a dom from a html string"""
        # Create an HTML parser which creates DOMs.
        parser = html5lib.HTMLParser(tree=dom.TreeBuilder)
        # Parse the source.
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
        return (from_currency1,to_currency2)

    def convert(self, currency1, currency2):
            """converts one unit of currency1 to currency2"""
            url = self.url_for(currency1, currency2)
            response = urllib.urlopen(url)
            data = response.read()

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tree = self.get_tree_from(data)
                return self.scrape_url_for_response(tree)
 
if __name__ == "__main__":
    if (len(sys.argv) != 3): 
        print "Usage: forex.py USD CNY"
        quit()

    currency1 = sys.argv[1] 
    currency2 = sys.argv[2]

    c = GoolgeCurrencyConverter()
    result_string = c.convert(currency1, currency2)
    print result_string[0]+result_string[1]


