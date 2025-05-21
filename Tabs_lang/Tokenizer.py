from Token import Token
from constants import VOCABULARY
from PrePro import PrePro

class Tokenizer():
    source: str
    position: int
    next: Token

    def __init__(self, source):
        prePro = PrePro()
        self.source = prePro.filter(source)
        self.position = 0
        self.next = Token()

    def selectNext(self):

        newToken = Token()

        if self.position >= len(self.source):
            newToken.type = "eof"
            newToken.value = "eof"
            self.next = newToken
            return

        c_char = self.source[self.position]

        if c_char not in VOCABULARY:
            newToken.type = "Unexpected Token"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return

        while c_char.isnumeric():
            newToken.type = "NUMBER"
            newToken.value += c_char
            self.position += 1
            if self.position >= len(self.source):
                self.next = newToken
                return
            c_char = self.source[self.position]
            if not c_char.isnumeric():
                self.next = newToken
                return
            
        if c_char in ["+", "-", "*"]:
            newToken.type = "OPERATOR"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            if self.source[self.position] == c_char:
                newToken.type = "OPERATOR"
                newToken.value += c_char
                self.next = newToken
                self.position += 1
                return
            return  

        if c_char in ["/"]:
            newToken.type = "OPERATOR"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "!":
            newToken.type = "NOT"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
 
        if c_char == "(":
            newToken.type = "OPEN_PAR"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == ")":
            newToken.type = "CLOSE_PAR"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "{":
            newToken.type = "OPEN_BRACKETS"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "}":
            newToken.type = "CLOSE_BRACKETS"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == '"':
            newToken.type = "QUOTE"
            newToken.value = "QUOTE"
            self.next = newToken
            self.position += 1
            return

        if c_char.isalpha() or c_char == "_":
            newToken.type = "IDENTIFIER"
            newToken.value = ""
            while c_char.isalnum() or c_char == "_":
                newToken.value += c_char
                self.position += 1

                if self.position >= len(self.source):
                    self.next = newToken
                    return
                
                c_char = self.source[self.position]
                if not (c_char.isalnum() or c_char == '_'):
                    if newToken.value == "print":
                        newToken.type = "PRINT"

                    if newToken.value == "prints":
                        newToken.type = "PRINT_SONG"
                        
                    if newToken.value == "if":
                        newToken.type = "IF"
                    if newToken.value == "else":
                        newToken.type = "ELSE"
                    if newToken.value == "while":
                        newToken.type = "WHILE"
                    if newToken.value == "get":
                        newToken.type = "GET"

                    if newToken.value == "X":
                        newToken.type = "UNPLAYED"

                    if newToken.value == "var":
                        newToken.type = "VAR"

                    if newToken.value == "play":
                        newToken.type = "PLAY"

                    if newToken.value == "and":
                        newToken.type = "AND"
                    if newToken.value == "or":
                        newToken.type = "OR"
                    
                    if newToken.value.isupper() and newToken.value != "X":
                        newToken.type = "SONG_IDENTIFIER"
                    self.next = newToken
                    return
            
        if c_char == "=":
            newToken.type = "EQUAL"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            if self.source[self.position] == "=":
                newToken.type = "EQ"
                newToken.value += c_char
                self.next = newToken
                self.position += 1
                return
            return
        
        if c_char == ";":
            newToken.type = "END_STATEMENT"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "<":
            newToken.type = "LT"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            if self.source[self.position] == "=":
                newToken.type = "LTE"
                newToken.value += "="
                self.next = newToken
                self.position += 1
                return
            return
        
        if c_char == ">":
            newToken.type = "GT"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            if self.source[self.position] == "=":
                newToken.type = "GTE"
                newToken.value += "="
                self.next = newToken
                self.position += 1
                return
            return
        
        if c_char == ",":
            newToken.type = "COMMA"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "|":
            newToken.type = "TAB"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        self.position += 1        
        self.selectNext()


# tkn = Tokenizer('"TESTE = |12|23|12|13|4 () Teste , " false true')
# while tkn.next.type != "eof":
#     print(tkn.next.type, " - ", tkn.next.value)
#     tkn.selectNext()
