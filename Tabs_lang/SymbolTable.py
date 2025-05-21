from var import Var

class SymbolTable():
    symbols = {
        "BLANK": Var("song", [["X","X","X","X","X","X"]]),
    }

    def setSymbol(self, key, value):
        self.symbols[key] = value
        return
    
    def setSymbolValue(self, key, value):
        self.symbols[key].value = value
    
    def containsSymbol(self, key):
        return key in self.symbols.keys()

    def printTable(self):
        print(self.symbols)

    def getSymbol(self, key):
        return self.symbols[key]