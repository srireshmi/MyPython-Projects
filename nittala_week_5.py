"""
################################################################
#Author: Srireshmi Nittala                                     #
#Date: 10-15-2017                                              #
#Description: Create classes and objects for Stocks, Bonds of  #
#             an investor and use inheritance to use common    #
#             attributes across the Parent and the Child Class #
################################################################
"""

import StockCalculator as sc
from datetime import datetime


class Investor():
    def __init__(self, investor_id, first_name, address, phone_number, list_of_stocks):
        """Initialize the investor."""
        self.investor_id = investor_id
        self.first_name = first_name
        self.address = address
        self.phone_number = phone_number
        self.list_of_stocks = list_of_stocks


class Stocks():
    def __init__(self, purchase_id, stock_symbol, purchase_price, current_price, shares, current_date, purchase_date):
        """Assign values to stock attributes"""
        self.purchase_id = purchase_id
        self.stock_symbol = stock_symbol
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.shares = shares
        self.current_date = current_date
        self.purchase_date = purchase_date

    def stock_report(self):
        """Print stock report for all investors
        """
        print(self.stock_symbol.ljust(justification), "\t\t",
              self.shares, "\t\t",
              sc.calculate_loss_gain(self.purchase_price, self.current_price, self.shares), "\t\t\t",
              sc.calculate_percent_yield_loss(self.purchase_price, self.current_price, self.current_date,
                                              self.purchase_date))


class Bonds(Stocks):
    def __init__(self, purchase_id, symbol, purchase_price, current_price, shares, current_date, purchase_date, coupon,
                 yld):
        """Assign values to Bond attributes."""
        super().__init__(purchase_id, symbol, purchase_price, current_price, shares, current_date, purchase_date)
        self.coupon = coupon
        self.yld = yld

    def bond_report(self):
        """Print bond report for all investors
        """
        print(self.stock_symbol.ljust(justification), "\t\t",
              self.shares, "\t\t",
              sc.calculate_loss_gain(self.purchase_price, self.current_price, self.shares), "\t\t\t",
              sc.calculate_percent_yield_loss(self.purchase_price, self.current_price, self.current_date,
                                              self.purchase_date), "\t\t\t\t\t\t",
              self.coupon, "\t\t\t",
              self.yld)


if __name__ == "__main__":
    today = str(datetime.now().strftime("%m/%d/%Y"))


    def validate_lists(investor_attributes):
        """ Validates that the lists have values and are all aligned.
        """
        try:
            stock_symbols = investor_attributes['stock_symbols']
            purchase_id = investor_attributes['purchase_id']
            shares = investor_attributes['shares']
            purchase_price = investor_attributes['purchase_price']
            current_price = investor_attributes['current_price']
            current_date = investor_attributes['current_date']
            purchase_date = investor_attributes['purchase_date']
            if (len(stock_symbols) > 0 and
                        len(stock_symbols) == len(shares) and
                        len(stock_symbols) == len(purchase_id) and
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
                        ('purchase_id') in investor_attributes.keys() and
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
            purchase_id = investor_attributes['purchase_id']
            shares = investor_attributes['shares']
            purchase_price = investor_attributes['purchase_price']
            current_price = investor_attributes['current_price']
            current_date = investor_attributes['current_date']
            purchase_date = investor_attributes['purchase_date']

            if (all(isinstance(stock, str) for stock in stock_symbols) and
                    all(isinstance(pid, int) for pid in purchase_id) and
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


    # Dictionary of stock symbols, shares, purchase price, current price, current_date, and purchase date.
    data_dict = {"1":
                     {'investor_name': 'Bob',
                      'investor_address': 'University Of Denver',
                      'investor_phone': '303-239-9099',
                      'investor_data':
                          {'Stocks':
                               {'stock_symbols': ['GOOGL', 'MSFT', 'RDS-A', 'AIG', 'FB', 'M', 'F', 'IBM'],
                                'purchase_id': [1, 2, 3, 4, 5, 6, 7, 8],
                                'shares': [125, 85, 400, 235, 150, 425, 85, 80],
                                'purchase_price': [772.88, 56.60, 49.58, 54.21, 124.31, 30.30, 12.58, 150.37],
                                'current_price': [941.53, 73.04, 55.74, 65.27, 172.45, 23.98, 10.95, 145.30],
                                'purchase_date': ['8/1/2015', '8/1/2015', '8/1/2015', '8/1/2015', '8/1/2015',
                                                  '1/10/2017',
                                                  '2/17/2017', '5/12/2017'],
                                'current_date': [today, today, today, today, today, today, today, today]
                                },
                           'Bonds':
                               {'stock_symbols': ['GT2:GOV'],
                                'purchase_id': [1],
                                'shares': [200],
                                'purchase_price': [100.02],
                                'current_price': [100.05],
                                'purchase_date': ['8/1/2017'],
                                'current_date': [today],
                                'coupon': [1.38],
                                'yield': [1.35]
                                }
                           }
                      }
                 }

    for investor_id, investor_data_dict in data_dict.items():
        investor_id = investor_id
        investor_name = investor_data_dict['investor_name']
        investor_address = investor_data_dict['investor_address']
        investor_phone = investor_data_dict['investor_phone']
        investor_stock_data = investor_data_dict['investor_data']['Stocks']
        investor_bond_data = investor_data_dict['investor_data']['Bonds']

        investor = Investor(investor_id, investor_name, investor_address, investor_phone,
                            investor_stock_data['stock_symbols'])

        if (validate_keys(investor_stock_data) and validate_types(investor_stock_data) and validate_lists(
                investor_stock_data)):
            justification = max(len(stock) for stock in investor_stock_data['stock_symbols'])
            # Process Stock Data
            print("Stock ownership for " + str(investor_name))
            print("----------------------------------------------------------------------------\n")
            print("STOCK".ljust(justification), "\t""\t", "#SHARES", "\t", "EARNINGS/LOSS", "\t""\t",
                  "YEARLY EARNING/LOSS")
            print("----------------------------------------------------------------------------")
            for i in range(0, len(investor_stock_data['stock_symbols'])):
                stocks = Stocks(investor_stock_data['purchase_id'][i], investor_stock_data['stock_symbols'][i],
                                investor_stock_data['purchase_price'][i],
                                investor_stock_data['current_price'][i], investor_stock_data['shares'][i],
                                investor_stock_data['current_date'][i], investor_stock_data['purchase_date'][i])
                stocks.stock_report()

            # Process Bond Data
            print("\n\nBond ownership for " + str(investor_name))
            print("----------------------------------------------------------------------------\n")
            print("BOND".ljust(justification), "\t""\t", "#SHARES", "\t", "EARNINGS/LOSS", "\t""\t",
                  "YEARLY EARNING/LOSS", "\t\t", "COUPON", "\t\t", "YIELD")
            print("----------------------------------------------------------------------------")
            for i in range(0, len(investor_bond_data['stock_symbols'])):
                bonds = Bonds(investor_bond_data['purchase_id'][i], investor_bond_data['stock_symbols'][i],
                              investor_bond_data['purchase_price'][i],
                              investor_bond_data['current_price'][i], investor_bond_data['shares'][i],
                              investor_bond_data['current_date'][i], investor_bond_data['purchase_date'][i],
                              investor_bond_data['coupon'][i], investor_bond_data['yield'][i])
                bonds.bond_report()
