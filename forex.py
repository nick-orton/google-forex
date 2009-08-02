import urllib
import html5lib
from html5lib.treebuilders import dom

currency1 = "AED"
currency2 = "ARS"
url = "http://www.google.com/finance/converter?a=1&from=" + currency1 + "&to=" + currency2
print url
response = urllib.urlopen(url)
headers = response.info()
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
