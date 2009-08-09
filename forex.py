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

    if(options.show_currencies): show_currencies()
    if (len(arguments) != 2): print_and_quit(USAGE_MSG)
    
    base_currency = arguments[0].upper() 
    quote_currency = arguments[1].upper()
    
    for currency in (base_currency,quote_currency):
        if (not(currency in CURRENCIES)):
            print_and_quit(currency + ' is not a valid currency')

    client = GoogleForexRateClient()
    amount = client.get_rate(base_currency, quote_currency)
    print '1 '+base_currency +' = '+ amount +' '+ quote_currency

if __name__ == "__main__":
    main()    
