import random

class QuoteHandler():
    def __init__(self, filename):
        self.filename = filename

    def getQuotes(self):
        quotes = {}
        with open(self.filename, 'r') as f:
            for line in f:
                line = line.replace('"', '')
                line = line.replace(',', '')
                line = line.split(':')
                quotes[int(line[0])] = line[1].strip()
        return quotes

    def getMaxNumberOfQuotes(self):
        quotes = self.getQuotes()
        return len(quotes)

    def generateRandomIntForQuote(self):
        max_number_of_quotes = self.getMaxNumberOfQuotes()
        random_int = random.randint(1, max_number_of_quotes)
        return random_int

    def getRandomQuote(self):
        quotes = self.getQuotes()
        random_int = self.generateRandomIntForQuote()
        return quotes[random_int]