"""
################################################################
#Author: Srireshmi Nittala                                     #
#Date: 10-29-2017                                              #
#Description: Generate Stock report by Inserting and Reading   #
#             from SQLite database                             #
################################################################
"""

import sqlite3
from datetime import datetime, date
import os
import uuid


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

    def insert_investor(self, conn):
        cur = conn.cursor()
        investor_data = [self._investor_id, self._first_name, self._address, self._phone_number]
        cur.execute("""INSERT INTO investor(investor_id, first_name, address, phone_number) VALUES(?, ?, ?, ?);""",
                    investor_data)

        for stock in self._list_of_stocks:
            stock.insert_stock(cur, self._investor_id)
        print("Inserted stock data for {0} successfully".format(self._first_name))

        for bond in self._list_of_bonds:
            bond.insert_bond(cur, self._investor_id)
        print("Inserted bond data for {0} successfully".format(self._first_name))

    def print_investments(self, cur, report):
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
    def __init__(self, purchase_id, stock_symbol, purchase_price, current_price, shares, purchase_date):
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
            self._purchase_date = datetime.strptime(purchase_date, "%m/%d/%Y").date()
        except Exception as e:
            print(str(e))
            raise

        if (date.today() - self._purchase_date).days <= 0:
            raise ValueError("Purchase Date should be prior to today")

        self._loss_gain = self.calculate_loss_gain()
        self._annual_percent_yield_loss = self.calculate_annual_percent_yield_loss()

    def calculate_loss_gain(self):
        """Calculates the loss or gain
        """
        return str(round((self._current_price - self._purchase_price) * self._shares, 2))

    def calculate_annual_percent_yield_loss(self):
        """Calculates the annual percent yield or loss
        """

        days = (date.today() - self._purchase_date).days
        return str(round(
            (((self._current_price - self._purchase_price) / self._purchase_price) / days) * 100 * 365, 2)) + "%"

    def insert_stock(self, cur, investor_id):
        """Insert Stock Record into database"""
        stock_data = [self._purchase_id, investor_id, self._stock_symbol, self._purchase_price, self._current_price,
                      self._shares, self._purchase_date.strftime("%m/%d/%Y")]
        cur.execute("""INSERT INTO stock(purchase_id, investor_id, stock_symbol, purchase_price, current_price, number_of_shares, purchase_date) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""", stock_data)

    def stock_report(self, report_file):
        """Print stock report for a given investor
        """

        report_file.write(
            "\n{:<16}{:<16}{:<16}{:<16}".format(str(self._stock_symbol), str(self._shares), str(self._loss_gain),
                                                str(self._annual_percent_yield_loss)))


class Bond(Stock):
    def __init__(self, purchase_id, symbol, purchase_price, current_price, shares, purchase_date, coupon,
                 yld):
        """Assign values to Bond attributes."""
        super().__init__(purchase_id, symbol, purchase_price, current_price, shares, purchase_date)
        self._coupon = coupon
        self._yld = yld

    def insert_bond(self, cur, investor_id):
        """Insert Bond Record into database"""
        bond_data = [self._purchase_id, investor_id, self._stock_symbol, self._purchase_price, self._current_price,
                     self._shares, self._purchase_date.strftime("%m/%d/%Y"), self._coupon, self._yld]
        cur.execute("""INSERT INTO bond(purchase_id, investor_id, stock_symbol, purchase_price, current_price, number_of_shares, purchase_date, coupon, yld) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", bond_data)

    def bond_report(self, report_file):
        """Print bond report for all investors
        """

        report_file.write("\n{:<16}{:<16}{:<16}{:<16}{:<16}{:<16}".format(str(self._stock_symbol), str(self._shares),
                                                                          str(self._loss_gain),
                                                                          str(self._annual_percent_yield_loss),
                                                                          str(self._coupon), str(self._yld)))


def load_stock_data(today, investor_obj):
    """Loads and adds stock data for a given investor object"""
    try:
        file_path = "Lesson6_Data_Stocks.csv"
        if os.path.exists(file_path):
            with open(file_path, "r") as stockFile:
                header = []
                for index, row in enumerate(stockFile):
                    uid = int(str(uuid.uuid4().time).replace("L", ""))
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
                            stock = Stock(uid, symbol, purchase_price, current_value, shares, purchase_date.strip())
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
                    uid = int(str(uuid.uuid4().time).replace("L", ""))
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
                            bond = Bond(uid, symbol, purchase_price, current_value, shares, purchase_date, coupon,
                                        yld.strip())
                            investor_obj.add_bond(bond)
                        else:
                            raise ValueError("Incorrect Columns in Bond file")
                bondFile.close()
        else:
            raise FileNotFoundError(
                "Bond File not found!! Please make sure input file exists in same directory as the Python program.")
    except Exception as e:
        raise e


def load_data_from_db(cur, investor_obj, investor_id):
    """Load Stock and Bond data from SQLite database"""
    _stock_data = cur.execute("SELECT * FROM stock WHERE investor_id = {0}".format(investor_id)).fetchall()
    _bond_data = cur.execute("SELECT * FROM bond WHERE investor_id = {0}".format(investor_id)).fetchall()
    for stock in _stock_data:
        stock_obj = Stock(stock[0], stock[2], stock[3], stock[4], stock[5], stock[6])
        investor_obj.add_stock(stock_obj)

    for bond in _bond_data:
        bond_obj = Bond(bond[0], bond[2], bond[3], bond[4], bond[5], bond[6], bond[7], bond[8])
        investor_obj.add_bond(bond_obj)


def create_tables(connection):
    """Create Table Schema for Stock, Bond, and Investor"""
    investor_table = """CREATE TABLE IF NOT EXISTS investor(
    investor_id integer PRIMARY KEY,
    first_name text NOT NULL,
    address text NOT NULL,
    phone_number integer NOT NULL);"""

    stock_table = """CREATE TABLE IF NOT EXISTS stock(
    purchase_id integer PRIMARY KEY,
    investor_id integer NOT NULL,
    stock_symbol text NOT NULL,
    purchase_price integer NOT NULL,
    current_price integer NOT NULL,
    number_of_shares integer NOT NULL,
    purchase_date text NOT NULL);"""

    bond_table = """CREATE TABLE IF NOT EXISTS bond(
    purchase_id integer PRIMARY KEY,
    investor_id integer NOT NULL,
    stock_symbol text NOT NULL,
    purchase_price integer NOT NULL,
    current_price integer NOT NULL,
    number_of_shares integer NOT NULL,
    purchase_date text NOT NULL,
    coupon integer NOT NULL,
    yld integer NOT NULL);"""

    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS investor")
    cursor.execute(investor_table)
    cursor.execute("DROP TABLE IF EXISTS stock")
    cursor.execute(stock_table)
    cursor.execute("DROP TABLE IF EXISTS bond")
    cursor.execute(bond_table)
    connection.commit()


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None"""

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
        return None


def delete_records(conn):
    """Delete records from each of the tables"""
    cur = conn.cursor()
    delete_investor = """delete from investor"""
    cur.execute(delete_investor)
    delete_stock = """delete from stock"""
    cur.execute(delete_stock)
    delete_bond = """delete from bond"""
    cur.execute(delete_bond)


def main():
    output_report_file = "investor_report.txt"
    db_file = "investments.db"
    today = str(datetime.now().strftime("%m/%d/%Y"))
    list_of_investors = []
    investor_obj1 = Investor(1, "Bob", "71 Pilgrim Avenue Chevy Chase, MD 20815", "303-303-3033")
    list_of_investors.append(investor_obj1)
    investor_obj2 = Investor(2, "Carl", "271 East Orchard Ave, CO 80112", "720-909-1234")
    list_of_investors.append(investor_obj2)

    # This piece of code is to:
    # 1) Read stock & bond data from CSV files
    # 2) Load data into classes
    # 3) Insert into SQLite investments database
    conn = create_connection(db_file)
    with conn:
        if not os._exists(db_file):
            create_tables(conn)
        delete_records(conn)
        for investor_obj in list_of_investors:
            load_stock_data(today, investor_obj)
            load_bond_data(today, investor_obj)
            investor_obj.insert_investor(conn)
    conn.close()

    # This piece of code performs the following steps:
    # 1) Read data from SQLite investments database,
    # 2) Load into class structures, and
    # 3) Generate an investment output report.
    with open(output_report_file, "w") as report:
        conn = create_connection(db_file)
        cur = conn.cursor()
        for record in cur.execute("SELECT * FROM investor"):
            print(record)
        for record in cur.execute("SELECT * FROM investor").fetchall():
            investor_obj = Investor(record[0], record[1], record[2], record[3])
            load_data_from_db(cur, investor_obj, record[0])
            investor_obj.print_investments(cur, report)
        conn.close()
    report.close()
    print("Report Generated successfully")


if __name__ == "__main__":
    main()
