# Most neccessary mathematical calculation modules, including those specific to risk analysis, are stored in this file
# Also, the full class structure (booo! down with classism) for the code is stored in here

import csv
from math import sqrt
from numpy import corrcoef, ravel

class Stock():
    def __init__(self, ticker, folder):
        """This class exists solely to satisfy my ego into proving to myself that, yes, I can write "object-oriented",
        or whatever horror Python actually lets me produce, considering that this will be a class stored inside of a list
        that is operated on inside of modules itself meaning NOTHING IS REAL AND THE GOVERNMENT IS BEES. Also, it is
        genuinely easier for me to use a class here so, yeeeeaaaah."""
        self._ticker = ticker
        self._path = folder + "/" + ticker + ".csv"
        self._riskScore = 0 # NOTE: In my brain, this goes to a max of 40
        self._beta = 0
        self.importPreviousPrices()
        self.standardDeviation()
        self.standardDeviationOfReturns()

    def getPricedData(self):
        return self._prices, self._totalPricePoints

    def getPrices(self):
        return self._prices, self._mean, self._stdDev, self._stdDevPercent

    def getSelectData(self, index):
        return self._prices[index]

    def getDataForTest(self):
        return self._mean, self._stdDev, self._stdDevPercent, self._riskScore, self._beta

    def importPreviousPrices(self):
        """NOTE: This was moved to the class, it's just easier this way, I promise, also, it's 1 am and I can't fcuxking type"""
        file = open(self._path)
        priceReader = csv.reader(file)
        next(priceReader)
        prices = []
        totalPricePoints = 0
        for row in priceReader:
            if row[1] != "":
                prices.append(float(row[1]))
        prices.pop()
        self._totalPricePoints = len(prices)
        self._prices = prices
        self._currentPrice = prices[-1]

    def updateRiskScore(self, value):
        """This function updates the stocks risk score, I don't know what more to say"""
        if value < 0:
            value = 0 - value
            predictValue = self._riskScore - value
        elif value > 0:
            predictValue = self._riskScore + value
        if predictValue > 40:
            self._riskScore = 40
        elif predictValue < 0:
            self._riskScore = 0

    def selectTimedData(self, days=7):
        ticks = days * 24
        prices = self._prices
        pricePoints = self._totalPricePoints
        usablePrices = []
        for point in range(ticks):
            curPoint = pricePoints-point
            price = prices[curPoint-1]
            usablePrices.append(price)
        self._prices = usablePrices
        self._totalPricePoints = ticks

    def meanCalculations(self):
        """NOTE: These calculations can be absolute *bitches* to you and all your friends, may cause tears, be very, very wary"""
        total = 0
        stockPrices, stockPricePoints = self.getPricedData()
        for price in stockPrices:
            total += price
        mean = total/stockPricePoints
        self._total = total
        self._mean = mean

    def standardDeviation(self):
        """NOTE: Some very bog standard deviousness, nothing weird about it."""
        prices, pricePoints = self.getPricedData()
        self.meanCalculations()
        addingSubtractions = 0
        for price in prices:
            subtractMeanSqrd = (price-self._mean)**2
            addingSubtractions += subtractMeanSqrd
        divisions = addingSubtractions/(pricePoints-1)
        stdDevFinal = divisions ** (1/2)
        if stdDevFinal < 0:
            stdDevFinal = 0-stdDevFinal
        self._stdDev = stdDevFinal
        self._stdDevPercent = round(((stdDevFinal/self._mean)*100),0)

    def standardDeviationOfReturns(self):
        prices, pricePoints = self.getPricedData()
        totalReturns = 0
        stockReturns = []
        for i in range(1, len(prices)-1):
            stockReturn = (prices[i] - prices[i-1])/prices[i-1]
            stockReturns.append(stockReturn)
            totalReturns += stockReturn
            print(self._ticker, i, stockReturn)
        returnMean = totalReturns / len(stockReturns)
        returnMinusMeanSum = 0
        for i in stockReturns:
            returnMinusMean = (i - returnMean)**2
            returnMinusMeanSum += returnMinusMean
        stdDevOfReturns = (returnMinusMeanSum/(len(stockReturns)-1))**(1/2)
        self._stdDevReturnsPercent = stdDevOfReturns


    def correlationCalculation(self, stockIndex):
        """Holy shit, why did it take so long to get this work?"""
        indexData = stockIndex.getPrices()
        indexPrices = indexData[0]
        stockPrices = self._prices
        correlation = corrcoef(stockPrices, indexPrices)
        self._correlation = ravel(correlation[1])[0]

    def betaCalculation(self, index):
        """This function caused me more pain than I thought I could physically withstand. I'm proud of myself for this,
        even though I probably have fuck all right to be. Turns out all of said pain was needless, due to me being
        stupid/stubborn.    In this function, please not that "s" at the start of a
        variable indicates it is related to the stock, whereas "i"
        indicates it is related to the index"""
        iStdDevP = index.getPrices()[5]
        sStdDevP = self._stdDevReturnsPercent
        self.correlationCalculation(index)
        stockCorrelation = self._correlation
        stdDevDivision = (sStdDevP/100)/(iStdDevP/100)
        beta = stockCorrelation * stdDevDivision # THIS?!?! THIS IS FUCKING IT? THIS IS THE BIG FUCKING FINALE FOR THIS SECTION!!???!?!?!?!
        self._beta =  beta # Well, I guess this is the big finale, but that's so much worse

    def stdDevRiskUpdate(self):
        """This function updates the risk for stocks from std dev"""
        prices, mean, stdDev, stdDevPercent = self.getPrices()
        prelimRiskSet = round((stdDevPercent/0.67), 0)
        if prelimRiskSet >= 15:
            self.updateRiskScore(15)
        else:
            self.updateRiskScore(prelimRiskSet)

    def exportData(self):
        name = "producedData/"+self._ticker+"-trimmed.csv"
        with open(name, "w") as csvfile:
            writerJob = csv.writer(csvfile, lineterminator='\n')
            writerJob.writerow(["tick", "price"])
            prices = self._prices
            for i in range(0,(len(prices)-1)):
                writerJob.writerow([i, prices[i]])

    def betaRiskUpdate(self):
        beta = self._beta
        if beta > 1:
            riskUpdate = (beta-1)/100
        else:
            riskUpdate = 0
        if riskUpdate > 25:
            riskUpdate = 25
        self._riskScore += riskUpdate

    def exportStockAndMarketData(self, index):
        stockData = self._prices
        indexData = index.getPrices()[0]
        ticker = self._ticker
        name = "producedData/"+ticker+"-withMarket.csv"
        with open(name, "w") as csvfile:
            writerJob = csv.writer(csvfile, lineterminator='\n')
            writerJob.writerow(["tick", "stock price", "market price"])
            for i in range(0, len(stockData)-1):
                writerJob.writerow([i, stockData[i], indexData[i]])

class Index(Stock):
    def __init__(self, ticker, indexConstits):
        self._ticker = ticker
        self._constituents = indexConstits
        self.importPreviousPrices(indexConstits)
        self.indexDataTrim()
        self.indexCalcs()
        self.standardDeviation()

    def importPreviousPrices(self, indexConstits):
        index = []
        for stock in indexConstits:
            newItem = Stock(stock, "marketData")
            index.append(newItem)
        self._index = index

    def getTotalPricePoints(self):
        return self._totalPricePoints

    def getDataForTest(self):
        return self._mean, self._stdDev, self._stdDevPercent

    def indexDataTrim(self):
        index = self._index
        counts = []
        for i in index:
            prices, pricePoints = i.getPricedData()
            counts.append(pricePoints)
        minimumCount = min(counts)
        minimumCountForTimed = int(round(minimumCount/24, 0))
        for i in index:
            i.selectTimedData(minimumCountForTimed)
        self._totalPricePoints = minimumCount

    def getPrices(self):
        return self._prices, self._mean, self._stdDev, self._stdDevPercent, self._total, self._stdDevReturnsPercent

    def getMeans(self):
        return self._mean, self._stdDev, self._stdDevPercent, self._total

    def indexCalcs(self):
        """IMPORTANT!!!: THIS DOES NOT RETURN A SINGLE NUMBER, BUT INSTEAD A LIST as it produces the full gamut of index prices"""
        averages = []
        for i in range((self._totalPricePoints-1),0, -1):
            constits = self._index
            indexSize = len(constits)
            workingAvg = 0
            for stock in constits:
                workingAvg += stock.getSelectData(i)
            workingAvg = workingAvg/indexSize
            averages.append(workingAvg)
        self._prices = averages

    def selectTimedData(self, days=7):
        ticks = days * 24
        prices = self._prices
        pricePoints = self._totalPricePoints-1
        usablePrices = []
        for point in range(ticks):
            curPoint = pricePoints-point
            price = prices[curPoint-1]
            usablePrices.append(price)
        self._prices = usablePrices
        self._totalPricePoints = ticks
        self.standardDeviationOfReturns()

    def exportData(self):
        name = self._ticker+".csv"
        with open(name, "w") as csvfile:
            writerJob = csv.writer(csvfile, lineterminator='\n')
            writerJob.writerow(["tick", "price"])
            prices = self._prices
            for i in range(0,(len(prices)-1)):
                writerJob.writerow([i, prices[i]])
