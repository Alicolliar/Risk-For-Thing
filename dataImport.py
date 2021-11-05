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

def correlation(stockPrices, stockSum, indexPrices, indexSum, pricePoints):
    sumStockIndex = 0
    sumStockSquared = 0
    sumIndexSquared = 0
    for i in range(pricePoints):
        stockPoint = stockPrices[i]
        indexPoint = indexPrices[i]
        sum = stockPoint + indexPoint
        sumStockIndex += sum
        stockPointSquared = stockPoint**2
        sumStockSquared += stockPointSquared
        indexPointSquared = indexPoint**2
        sumIndexSquared += indexPointSquared

    stockSumSquared = stockSum**2
    indexSumSquared = indexSum**2
    topHalfOfFraction = (pricePoints * (sumStockIndex - (stockSum*indexSum)))
    insideSqrt = ((pricePoints * sumStockSquared)-stockSumSquared)*((pricePoints * sumIndexSquared)-indexSumSquared)
    bottomHalfOfFraction = sqrt(insideSqrt)
    correlation = topHalfOfFraction/bottomHalfOfFraction
    return correlation
