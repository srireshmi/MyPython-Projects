"""
################################################
# Author: Srireshmi Nittala                    #
# Date: 09/17/2017                             #
# Description: This program calculates,        #
# how much money was earned or lost in shares. #
################################################
"""

def run():
    """Inputs to the program: Name, symbol, #shares, purchase price, current price
    """
    name = input("Your Name:")
    symbol = input("Your Stock symbol:")
    number_of_shares= int(input("Number of shares you own:"))
    purchase_price = float(input("Purchase price per share:"))
    current_price = float(input("Current price per share:"))
    earnings_loss_to_date = (float(current_price)-float(purchase_price)) * int(number_of_shares)

    """ Calculate earnings or loss to date and print all the required outputs
    """
    print("-------------OUTPUT ---------------")
    print(symbol.upper()+": "+ str(number_of_shares))
    print("Purchase Price per share: " + str(purchase_price))
    print("Current Price per share: " + str(current_price))
    print("Earnings/Loss to-date: " + "$" +str(earnings_loss_to_date))

if __name__ == "__main__":
    run()





    

