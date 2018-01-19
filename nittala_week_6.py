"""
################################################################
#Author: Srireshmi Nittala                                     #
#Date: 10-22-2017                                              #
#Description: Read data from files, load data into             #
#             Stocks, Bonds, Investor classes, and then print  #
#            results to an output txt file.                    #
################################################################
"""

from datetime import datetime
import os


class Investor(object):
    def __init__(self, investor_id, first_name, address, phone_number):
        """Initialize the investor.
        """
        self._investor_id = investor_id
        self._first_name = first_name
        self._address = address
        self._phone_number = phone_number
        self._list_of_stocks = []
        self._list_of_bonds = []

    def add_stock(self, stock):
        """
        :param stock: This is the current Stock Object
        """
        self._list_of_stocks.append(stock)

    def add_bond(self, bond):
        """
        :param bond: This is the current Bond Object
        """
        self._list_of_bonds.append(bond)

    def print_investments(self, report):
        """Print each of the investor's investments into a report file"""

        report.write("##################################################")
        report.write("\n#### Investment Report for {0}".format(self._first_name))
        report.write("\n#### Address:- {0}".format(self._address))
        report.write("\n#### Phone:- {0}".format(self._phone_number))
        report.write("\n##################################################")

        # Stock headers
        report.write('\n-------------------------------------------------------------------------------------')
        report.write('\n{:<16}{:<16}{:<16}{:<16}'.format('STOCK', '#SHARES', 'EARNINGS/LOSS', 'YEARLY RATE'))
        report.write('\n-------------------------------------------------------------------------------------')
        for stock in self._list_of_stocks:
            stock.stock_report(report)

        # Bond headers
        report.write('\n\n-------------------------------------------------------------------------------------')
        report.write(
            '\n{:<16}{:<16}{:<16}{:<16}{:<16}{:<16}'.format('BOND', '#QTY', 'EARNINGS/LOSS', 'YEARLY RATE',
                                                            'COUPON', 'YIELD'))
        report.write('\n-------------------------------------------------------------------------------------')
        for bond in self._list_of_bonds:
            bond.bond_report(report)
        report.write('\n\n\n\n')


class Stock(object):
    def __init__(self, purchase_id, stock_symbol, purchase_price, current_price, shares, current_date, purchase_date):
        """Assign values to stock attributes"""
        self._purchase_id = purchase_id
        self._stock_symbol = stock_symbol

        try:
            self._purchase_price = float(purchase_price)
        except Exception as e:
            print(str(e))
            raise

        try:
            self._current_price = float(current_price)
        except Exception as e:
            print(str(e))
            raise

        try:
            self._shares = int(shares)
        except Exception as e:
            print(str(e))
            raise

        try:
            self._current_date = datetime.strptime(current_date, "%m/%d/%Y").date()
        except Exception as e:
            print(str(e))
            raise

        try:
            self._purchase_date = datetime.strptime(purchase_date, "%m/%d/%Y").date()
        except Exception as e:
            print(str(e))
            raise

        if self._current_date < self._purchase_date:
            raise ValueError("Purchase Date should be prior to today")

        self._loss_gain = self.calculate_loss_gain(self._purchase_price, self._current_price, self._shares)
        self._annual_percent_yield_loss = self.calculate_annual_percent_yield_loss(self._purchase_price,
                                                                                   self._current_price,
                                                                                   self._current_date,
                                                                                   self._purchase_date)

    def calculate_loss_gain(self, purchase_price, current_price, shares):
        """Calculates the loss or gain
        """
        return str(round((current_price - purchase_price) * shares, 2))

    def calculate_annual_percent_yield_loss(self, purchase_price, current_price, current_date, purchase_date):
        """Calculates the annual percent yield or loss
        """
        return str(round(
            (((current_price - purchase_price) / purchase_price) / (
                (current_date - purchase_date).days)) * 100 * 365, 2)) + "%"

    def stock_report(self, report_file):
        """Print stock report for a given investor
        """

        report_file.write(
            "\n{:<16}{:<16}{:<16}{:<16}".format(str(self._stock_symbol), str(self._shares), str(self._loss_gain),
                                                str(self._annual_percent_yield_loss)))


class Bond(Stock):
    def __init__(self, purchase_id, symbol, purchase_price, current_price, shares, current_date, purchase_date, coupon,
                 yld):
        """Assign values to Bond attributes."""
        super().__init__(purchase_id, symbol, purchase_price, current_price, shares, current_date, purchase_date)
        self.coupon = coupon
        self.yld = yld

    def bond_report(self, report_file):
        """Print bond report for all investors
        """

        report_file.write("\n{:<16}{:<16}{:<16}{:<16}{:<16}{:<16}".format(str(self._stock_symbol), str(self._shares),
                                                                          str(self._loss_gain),
                                                                          str(self._annual_percent_yield_loss),
                                                                          str(self.coupon), str(self.yld)))


def load_stock_data(today, investor_obj):
    """Loads and adds stock data for a given investor object"""
    try:
        file_path = "Lesson6_Data_Stocks.csv"
        if os.path.exists(file_path):
            with open(file_path, "r") as stockFile:
                header = []
                for index, row in enumerate(stockFile):
                    attributes = row.split(",")
                    if index == 0:
                        header = attributes
                    else:
                        if all(col in header for col in
                               ["SYMBOL", "NO_SHARES", "PURCHASE_PRICE", "CURRENT_VALUE", "PURCHASE_DATE\n"]):
                            symbol_index = header.index("SYMBOL")
                            symbol = attributes[symbol_index]
                            symbol_index = header.index("NO_SHARES")
                            shares = attributes[symbol_index]
                            symbol_index = header.index("PURCHASE_PRICE")
                            purchase_price = attributes[symbol_index]
                            symbol_index = header.index("CURRENT_VALUE")
                            current_value = attributes[symbol_index]
                            symbol_index = header.index("PURCHASE_DATE\n")
                            purchase_date = attributes[symbol_index]
                            stock = Stock(index, symbol, purchase_price, current_value, shares, today,
                                          purchase_date.strip())
                            investor_obj.add_stock(stock)
                        else:
                            raise ValueError("Incorrect Columns in Stock file")
                stockFile.close()
        else:
            raise FileNotFoundError(
                "Stock File not found!! Please make sure input file exists in same directory as the Python program.")
    except Exception as e:
        raise e


def load_bond_data(today, investor_obj):
    """Loads and adds Bond data for a given investor object"""
    try:
        file_path = "Lesson6_Data_Bonds.csv"
        if os.path.exists(file_path):
            with open(file_path, "r") as bondFile:
                header = []
                for index, row in enumerate(bondFile):
                    attributes = row.split(",")
                    if index == 0:
                        header = attributes
                    else:
                        if all(col in header for col in
                               ["SYMBOL", "NO_SHARES", "PURCHASE_PRICE", "CURRENT_VALUE", "PURCHASE_DATE", "Coupon",
                                "Yield\n"]):
                            symbol_index = header.index("SYMBOL")
                            symbol = attributes[symbol_index]
                            symbol_index = header.index("NO_SHARES")
                            shares = attributes[symbol_index]
                            symbol_index = header.index("PURCHASE_PRICE")
                            purchase_price = attributes[symbol_index]
                            symbol_index = header.index("CURRENT_VALUE")
                            current_value = attributes[symbol_index]
                            symbol_index = header.index("PURCHASE_DATE")
                            purchase_date = attributes[symbol_index]
                            symbol_index = header.index("Coupon")
                            coupon = attributes[symbol_index]
                            symbol_index = header.index("Yield\n")
                            yld = attributes[symbol_index]
                            bond = Bond(index, symbol, purchase_price, current_value, shares, today, purchase_date,
                                        coupon, yld.strip())
                            investor_obj.add_bond(bond)
                        else:
                            raise ValueError("Incorrect Columns in Bond file")
                bondFile.close()
        else:
            raise FileNotFoundError(
                "Bond File not found!! Please make sure input file exists in same directory as the Python program.")
    except Exception as e:
        raise e


def main():
    output_report_file = "investor_report.txt"
    today = str(datetime.now().strftime("%m/%d/%Y"))
    investor_id = 1
    list_of_investors = []
    investor_obj1 = Investor(investor_id, "Bob", "71 Pilgrim Avenue Chevy Chase, MD 20815", "303-303-3033")
    list_of_investors.append(investor_obj1)
    investor_obj2 = Investor(investor_id, "Carl", "271 East Orchard Ave, CO 80112", "720-909-1234")
    list_of_investors.append(investor_obj2)
    with open(output_report_file, "w") as report:
        for investor_obj in list_of_investors:
            load_stock_data(today, investor_obj)
            load_bond_data(today, investor_obj)
            investor_obj.print_investments(report)
    report.close()


if __name__ == "__main__":
    main()
