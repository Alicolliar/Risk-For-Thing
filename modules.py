# All neccessary mathematical calculation modules, including those specific to risk analysis, are stored in this file
# Also, the full class structure (booo! down with classism) for the code is stored in here
import csv

class Stock():
    def __init__(self, ticker, folder):
        """This class exists solely to satisfy my ego into proving to myself that, yes, I can write "object-oriented",
        or whatever horror Python actually lets me produce, considering that this will be a class stored inside of a list
        that is operated on inside of modules itself meaning NOTHING IS REAL AND THE GOVERNMENT IS BEES. Also, it is
        genuinely easier for me to use a class here so, yeeeeaaaah."""
        self._ticker = ticker
        self._path = folder + "/" + ticker + ".csv"
        self._riskScore = 0 # NOTE: In my brain, this goes to a max of 40
        self.importPreviousPrices()
        self.standardDeviation()

    def getPricedData(self):
        return self._prices, self._totalPricePoints

    def getPrices(self):
        return self._prices, self._stdDev, self._stdDevPercent

    def getSelectData(self, index):
        return self._prices[index]

    def getDataForTest(self):
        return self._mean, self._stdDev, self._stdDevPercent, self._riskScore

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
            self._riskScore -= value
        elif value > 0:
            self._riskScore += value
        else:
            return

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
        self._mean = mean

    def standardDeviation(self):
        """NOTE: Some very bog standard deviousness, nothing weird about it. Also, these can only take a Stock *or Index* type"""
        prices, pricePoints = self.getPricedData()
        self.meanCalculations()
        addingSubtractions = 0
        for price in prices:
            subtractMeanSqrd = (self._mean-price)**2
            addingSubtractions += subtractMeanSqrd
        divisions = addingSubtractions/(pricePoints-1)
        stdDevFinal = divisions ** (1/2)
        if stdDevFinal < 0:
            stdDevFinal = 0-stdDevFinal
        self._stdDev = stdDevFinal
        self._stdDevPercent = round(((stdDevFinal/self._mean)*100),0)

    def betaCalculation(self, index):
        """In this function, please not that "s" at the start of a
        variable indicates it is related to the stock, whereas "i"
        indicates it is related to the index"""
        sPrices, sStdDev, sStdDevP = self.getPrices()
        iPrices, iStdDev, iStdDevP = index.getMeans()

        return

    def stdDevRiskUpdate(self):
        """This function updates the risk for stocks from std dev"""
        mean, stdDev, stdDevPercent = self.getMeans()
        prelimRiskSet = round((stdDevPercent/0.67), 0)
        if prelimRiskSet >= 15:
            self.updateRiskScore(15)
        else:
            self.updateRiskScore(prelimRiskSet)

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

    def getMeans(self):
        return self._mean, self._stdDev, self._stdDevPercent

    def indexCalcs(self):
        """IMPORTANT!!!: THIS DOES NOT RETURN A SINGLE NUMBER, BUT INSTEAD A LIST as it produces the index prices"""
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

    def exportData(self):
        name = self._ticker+".csv"
        with open(name, "w") as csvfile:
            writerJob = csv.writer(csvfile, lineterminator='\n')
            writerJob.writerow(["tick", "price"])
            prices = self._prices
            for i in range(0,(len(prices)-1)):
                writerJob.writerow([i, prices[i]])
