import random
import json
import os

class QuoteHandler():
    def __init__(self, filename: str = "quotes.json"):
        self.filename = filename

    def getQuotes(self):
        # Get the quotes from the json file and return them quotes into 1, 2
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                quotes = json.load(f)
                return quotes
        else:
            with open(self.filename, "w") as f:
                json.dump({}, f)
            with open(self.filename, "r") as f:
                quotes = json.load(f)
                return quotes


    def getMaxNumberOfQuotes(self):
        quotes = self.getQuotes()
        max_number_of_quotes = len(quotes["quotes"])
        return max_number_of_quotes
            

    def generateRandomIntForQuote(self):
        max_number_of_quotes = self.getMaxNumberOfQuotes()
        random_int = random.randint(1, max_number_of_quotes)
        return random_int


    def getRandomQuote(self):
        quotes = self.getQuotes()
        random_int = self.generateRandomIntForQuote()
        quote = quotes["quotes"][str(random_int)]
        return quote


    def createQuote(self, content, author):
        # Create a quote
        quotes = self.getQuotes()
        max_number_of_quotes = self.getMaxNumberOfQuotes()
        quotes["quotes"][str(max_number_of_quotes + 1)] = {
            "quote_content": content,
            "author": author,
        }
        with open(self.filename, "w") as f:
            json.dump(quotes, f, indent=4)