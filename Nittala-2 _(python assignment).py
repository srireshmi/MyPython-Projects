"""
###############################################################
#Author: Srireshmi Nittala                                     #
#Date: 09-22-2017                                              #
#Description: Generate and display stock report for Bob Smith  #
###############################################################
"""


def stock_report(stock_symbols, shares, purchase_price, current_price):
    """Print stock report for Bob Smith
    """
    print("Stock ownership for Bob Smith")
    print("--------------------------------------------\n")
    print("STOCK", "\t", "SHARE#", "\t", "EARNINGS/LOSS")
    print("--------------------------------------------")
    for i in range(0, len(stock_symbols)):
            print(stock_symbols[i], "\t", shares[i], "\t\t", round((current_price[i]-purchase_price[i])*shares[i],2))    

def validate_lists(stock_symbols, shares, purchase_price, current_price):
    """ Validates that the lists have values and are all aligned.
    """
    if(len(stock_symbols) > 0 and
       len(stock_symbols) == len(shares) and
       len(stock_symbols) == len(purchase_price) and
       len(stock_symbols) == len(current_price)):
        return 1
    else:
        print("Please check lists for errors!!!")
        return 0

if __name__ == "__main__":
    #Lists of stock symbols, shares, purchase price, and current price
    stock_symbols=['GOOGL','MSFT','RDS-A','AIG','FB']
    shares=[125, 85, 400, 235, 150]
    purchase_price=[772.88, 56.60, 49.58, 54.21, 124.31]
    current_price=[941.53, 73.04, 55.74, 65.27, 172.45]

    if(validate_lists(stock_symbols, shares, purchase_price, current_price)):
        stock_report(stock_symbols, shares, purchase_price, current_price)
    
    
