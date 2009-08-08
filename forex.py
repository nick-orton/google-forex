#!/usr/bin/python
import warnings,urllib,html5lib,sys
from html5lib.treebuilders import dom
import optparse
from currencies import CURRENCIES


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

USAGE_MSG = "Usage: forex.py USD CNY"
 
def print_and_quit(msg):
    """prints an output message and ends """
    print msg
    quit()

def show_currencies():
    print 'need help?'
    print USAGE_MSG
    print 'Available Currencies:'
    print_and_quit(CURRENCIES._keys)

def main():
    parser = optparse.OptionParser()
    parser.add_option('--currencies', '-c', action="store_true", default=False, 
                      dest="show_currencies", help="List Valid Currencies")

    options, arguments = parser.parse_args()

    if(options.show_currencies):
       show_currencies()
    if (len(arguments) != 2): 
        print_and_quit(USAGE_MSG)
    currency1 = arguments[0].upper() 
    
    currency2 = arguments[1].upper()
    
    for currency in (currency1,currency2):
        if (not(currency in CURRENCIES)):
            print currency + ' is not a valid currency'
            quit()

    client = GoogleForexRateClient()
    rate = client.get_rate(currency1, currency2)
    print rate[0]+rate[1]

if __name__ == "__main__":
    main()    
