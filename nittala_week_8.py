"""
######################################################################
#Author: Srireshmi Nittala                                           #
#Date: 11-05-2017                                                    #
#Description: Generate a line chart for IBM Stock from a json file   #
######################################################################
"""

import json
import datetime
from matplotlib import pyplot
from matplotlib import dates


def read_file(file_path):
    """Read a json file.
      :param file_path: This is the input file path.
      :return: json data
     """
    with open(file_path) as f:
        data = json.load(f)
        return data


def add_data_to_graph(open_price, close_price, date):
    """Plot graph using price,date Parameters:
    :param open_price: Open price
    :param close_price: Close price
    :param date: Date
    :return: The graph with the data
    """
    # date = dates.date2num(date)
    pyplot.plot(date, open_price, linestyle='solid', marker='None', label="Open Price")
    pyplot.plot(date, close_price, linestyle='solid', marker='None', label="Close Price")
    return pyplot


def main():
    """
    Add Stock data of IBM to price and date lists.
    """
    file_path = "AllStocks.json"
    data = read_file(file_path)
    open_price = []
    close_price = []
    date_list = []
    for i in data:
        # filter by symbol
        if i["Symbol"] == "IBM":
            # filter out of all -
            if i['Open'] != '-':
                open_price.append(float(i["Open"]))
                close_price.append(float(i["Close"]))
                date = datetime.datetime.strptime(i['Date'], '%d-%b-%y').date()
                date_list.append(date)
                # generate 2 lines within one graph
    graph = add_data_to_graph(open_price, close_price, date_list)
    graph.legend()
    graph.title("Stock Info of Open or Close price v/s Date")
    graph.xlabel('Date')
    graph.ylabel('Price')
    graph.savefig('nittala_stock_graph_week8.png')
    graph.show()

if __name__ == "__main__":
    main()
