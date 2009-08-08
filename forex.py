#!/usr/bin/python
import optparse
from currencies import CURRENCIES
from services import GoogleForexRateClient

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
            print_and_quit(currency + ' is not a valid currency')

    client = GoogleForexRateClient()
    rate = client.get_rate(currency1, currency2)
    print rate[0]+rate[1]

if __name__ == "__main__":
    main()    
