"""
###############################################################
#Author: Srireshmi Nittala                                    #
#Date: 10-1-2017                                              #
#Description: Use dictionaries instead of lists to create     #
stock report for Investors                                    #
###############################################################
"""
"""
This code used 'Nesting- A Dictionary of dictionaries' method to generate the stock reports.
You can store a dictionary inside another dictionary. In this case eash value associated with
a key is itself a dictionary.
I believe this is an effective method for this scenario. This has multiple key values and we
can update the dictionaries easily in this method.
you could store multiple datastructures in the same data dictionary unlike a list

"""

def stock_report(investor, stock_symbols, shares, purchase_price, current_price):
    """Print stock report for all investors
    """
    print("Stock ownership for " + str(investor))
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
    stock_data_dict={
        'Bob':
        {
        'stock_symbols':['GOOGL','MSFT','RDS-A','AIG','FB'],
        'shares':[125, 85, 400, 235, 150],
        'purchase_price':[772.88, 56.60, 49.58, 54.21, 124.31],
        'current_price':[941.53, 73.04, 55.74, 65.27, 172.45]
        },
        'Pop':
        {'stock_symbols':['GOOGL','MSFT','RDS-A','AIG','YAHOO'],
        'shares':[125, 85, 400, 235, 120],
        'purchase_price':[772.88, 56.60, 49.58, 54.21, 144.31],
        'current_price':[941.53, 73.04, 55.74, 65.27, 172.45]
        }
       }

    dob = {'stock_symbols':['GOOGL','MSFT','RDS-A','AIG','thuku'],
        'shares':[125, 85, 400, 235, 120],
        'purchase_price':[772.88, 56.60, 49.58, 54.21, 144.31],
        'current_price':[941.53, 73.04, 55.74, 65.27, 172.45]
        }
    stock_data_dict['dob'] = dob
    print(stock_data_dict)

    
    for investor, investor_attributes in stock_data_dict.items():    
        if(validate_lists(stock_data_dict[investor]['stock_symbols'], stock_data_dict[investor]['shares'],
                      stock_data_dict[investor]['purchase_price'], stock_data_dict[investor]['current_price'])):
            stock_report(investor, stock_data_dict[investor]['stock_symbols'], stock_data_dict[investor]['shares'],
                      stock_data_dict[investor]['purchase_price'], stock_data_dict[investor]['current_price'])
    
    

    
