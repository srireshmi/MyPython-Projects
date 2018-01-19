"""
###############################################################
#Author: Srireshmi Nittala                                    #
#Date: 10-8-2017                                              #
#Description: Create and use functions in the Stock Problem   #
###############################################################
"""

import StockCalculator as sc
from datetime import datetime


def stock_report(investor, stock_symbols, shares, purchase_price, current_price, current_date, purchase_date):
    """Print stock report for all investors
    """
    justification = max(len(stock) for stock in stock_symbols)
    print("Stock ownership for " + str(investor))
    print("----------------------------------------------------------------------------\n")
    print("STOCK".ljust(justification), "\t""\t", "#SHARES", "\t", "EARNINGS/LOSS", "\t""\t", "YEARLY EARNING/LOSS")
    print("----------------------------------------------------------------------------")

    for i in range(0, len(stock_symbols)):
        print(str(stock_symbols[i]).ljust(justification), "\t\t",
              shares[i], "\t\t",
              sc.calculate_loss_gain(i, purchase_price, current_price, shares), "\t\t\t",
              sc.calculate_percent_yield_loss(i, purchase_price, current_price, current_date, purchase_date))


def validate_lists(investor_attributes):
    """ Validates that the lists have values and are all aligned.
    """
    try:
        stock_symbols = investor_attributes['stock_symbols']
        shares = investor_attributes['shares']
        purchase_price = investor_attributes['purchase_price']
        current_price = investor_attributes['current_price']
        current_date = investor_attributes['current_date']
        purchase_date = investor_attributes['purchase_date']
        if (len(stock_symbols) > 0 and
                    len(stock_symbols) == len(shares) and
                    len(stock_symbols) == len(purchase_price) and
                    len(stock_symbols) == len(current_price) and
                    len(stock_symbols) == len(current_date) and
                    len(stock_symbols) == len(purchase_date)):
            return 1
        else:
            print("Please check lists for errors!!!")
            return 0
    except Exception as e:
        print("Exception occurred while validating lists!!!", e)


def validate_keys(investor_attributes):
    """Validates that all the expected keys exist in the stock data dictionary for each of the investors
    """
    try:
        if (('stock_symbols') in investor_attributes.keys() and
                    ('shares') in investor_attributes.keys() and
                    ('purchase_price') in investor_attributes.keys() and
                    ('current_price') in investor_attributes.keys() and
                    ('current_date') in investor_attributes.keys() and
                    ('purchase_date') in investor_attributes.keys()):
            return True
        else:
            print("Missing Keys. Please check input.")
            return False
    except Exception as e:
        print("Exception occurred while validating keys!!! ", e)


def validate_types(investor_attributes):
    """Validates that all the values in the dictionary are of the expected data types
    """
    try:
        stock_symbols = investor_attributes['stock_symbols']
        shares = investor_attributes['shares']
        purchase_price = investor_attributes['purchase_price']
        current_price = investor_attributes['current_price']
        current_date = investor_attributes['current_date']
        purchase_date = investor_attributes['purchase_date']

        if (all(isinstance(stock, str) for stock in stock_symbols) and
                all(isinstance(share, int) for share in shares) and
                all(isinstance(pp, float) for pp in purchase_price) and
                all(isinstance(cp, float) for cp in current_price) and
                all(isinstance(datetime.strptime(cd, "%m/%d/%Y"), datetime) for cd in current_date) and
                all(isinstance(datetime.strptime(pd, "%m/%d/%Y"), datetime) for pd in purchase_date)):
            return True
        else:
            print("The types are invalid")
    except Exception as e:
        print("Exception occurred while validating types!!! ", e)


if __name__ == "__main__":
    # Dictionary of stock symbols, shares, purchase price, current price, current_date, and purchase date.
    stock_data_dict = {
        'Bob':
            {
                'stock_symbols': ['GOOGL', 'MSFT', 'RDS-A', 'AIG', 'FB', 'M', 'F', 'IBM'],
                'shares': [125, 85, 400, 235, 150, 425, 85, 80],
                'purchase_price': [772.88, 56.60, 49.58, 54.21, 124.31, 30.30, 12.58, 150.37],
                'current_price': [941.53, 73.04, 55.74, 65.27, 172.45, 23.98, 10.95, 145.30],
                'purchase_date': ['8/1/2015', '8/1/2015', '8/1/2015', '8/1/2015', '8/1/2015', '1/10/2017', '2/17/2017',
                                  '5/12/2017'],
                'current_date': ['10/8/2017', '10/8/2017', '10/8/2017', '10/8/2017', '10/8/2017', '10/8/2017',
                                 '10/8/2017', '10/8/2017']
            }}

    for investor, investor_attributes in stock_data_dict.items():
        if (validate_keys(investor_attributes) and validate_types(investor_attributes) and validate_lists(
                investor_attributes)):
            stock_report(investor, investor_attributes['stock_symbols'], investor_attributes['shares'],
                         investor_attributes['purchase_price'], investor_attributes['current_price'],
                         investor_attributes['current_date'], investor_attributes['purchase_date'])
