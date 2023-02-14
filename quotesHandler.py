import random

# To get the quotes from the quotes.txt file at the root of the project
def getQuote(filename):
    quotes = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.replace('"', '')
            line = line.replace(',', '')
            line = line.split(':')
            quotes[int(line[0])] = line[1]
    return quotes

# To get the max number of quotes in the quotes.txt file
# 1: "quote1"
# 2: "quote2"
def getMaxNumberOfQuotes(filename):
    quotes = getQuote(filename)
    return len(quotes)

# To generate a random int for the selection of a quote in the dictionnary
def generateRandomIntForQuote():
    randomInt = random.randint(1, getMaxNumberOfQuotes('quotes.txt'))
    return randomInt