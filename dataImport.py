# This file includes all the neccessary data import functions
import csv

def importPreviousPrices(stockTicker):
    stockFileName = "testData/" + stockTicker + ".csv"
    file = open(stockFile)
    priceReader = csv.reader(file)
    next(priceReader)
    prices = []
    for row in priceReader:
        prices.append(row[2])
    return prices
