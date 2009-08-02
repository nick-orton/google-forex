import urllib
import html5lib
from html5lib.treebuilders import dom
import sys

if (len(sys.argv) != 3): 
    print "usage: python forex.py USD CNY"
    quit()

currency1 = sys.argv[1] 
currency2 = sys.argv[2]

url = "http://www.google.com/finance/converter?a=1&from=" + currency1 + "&to=" + currency2

response = urllib.urlopen(url)
data = response.read()

# Create an HTML parser which creates DOMs.
parser = html5lib.HTMLParser(tree=dom.TreeBuilder)
# Parse the source.
tree = parser.parse(data)
# Normalise the tree.  This basically cleans up the
# text nodes inside which makes our life easier.
tree.normalize()

# Create a list of all the rows (that is, all <div>
# tags with the class of "row")
rows = [div for div in tree.getElementsByTagName("div")\
        if div.getAttribute("id").strip() == "currency_converter_result"]
#<div id=currency_converter_result>1 AED = <span class=bld>1.0423 ARS</span>

from_currency1 =  rows[0].childNodes[0].data
to_currency2 = rows[0].childNodes[1].childNodes[0].data
print from_currency1+to_currency2
