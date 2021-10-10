from modules import *
import dataImport

def UserInput():
    """This is, possibly, a placeholder, so it'll look shite
    for now without any of that customer service bollockery"""
    numberofStocks = int(input("Please input the number of stocks the customer owns.\n> "))
    days = int(input("Please input the number of days you would like the data to go back. (If you wish to use all data, please enter \"0\".)\n> "))
    stocks = []
    for i in numberofStocks:
        ticker = input("Please input the ticker for the current stock.\n> "))
        stocks[i-1] = Stock(ticker)
    return stocks

def firstMetric(stocks):
    """NOTE: This function performs the std dev calcs and assigns the risk scores to a max of 15"""
    for stock in stocks:
        return

def secondMetric(stocks):
    """NOTE: This function performs the beta calcs and assigns the risk scores to a max of 25"""
    for stock in stocks:
        return
