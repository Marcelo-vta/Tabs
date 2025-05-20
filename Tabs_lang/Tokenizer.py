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
            newToken.type = "number"
            newToken.value += c_char
            self.position += 1
            if self.position >= len(self.source):
                self.next = newToken
                return
            c_char = self.source[self.position]
            if not c_char.isnumeric():
                self.next = newToken
                return
            
        if c_char == "+":
            newToken.type = "operator"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            if self.source[self.position] == "+":
                newToken.type = "concat"
                newToken.value += c_char
                self.next = newToken
                self.position += 1
                return
            return  

        if c_char in ["-", "*", "/"]:
            newToken.type = "operator"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "!":
            newToken.type = "not"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
 
        if c_char == "(":
            newToken.type = "openPrio"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == ")":
            newToken.type = "closePrio"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "{":
            newToken.type = "openBlock"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "}":
            newToken.type = "closeBlock"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == '"':
            newToken.type = "string"
            newToken.value = ""
            self.position += 1
            c_char = self.source[self.position]
            while c_char != '"':
                newToken.value += c_char

                self.position += 1
                c_char = self.source[self.position]

                if self.position >= len(self.source):
                    raise Exception("Unclosed string")
                
            self.next = newToken
            self.position += 1

            return

        if c_char.isalpha() or c_char == "_":
            newToken.type = "identifier"
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
                        newToken.type = "print"
                    if newToken.value == "printf":
                        newToken.type = "print"
                        
                    if newToken.value == "if":
                        newToken.type = "if"
                    if newToken.value == "else":
                        newToken.type = "else"
                    if newToken.value == "while":
                        newToken.type = "while"
                    if newToken.value == "var":
                        newToken.type = "setVar"
                    if newToken.value == "reader":
                        newToken.type = "read"

                    if newToken.value == "i32":
                        newToken.type = "type"
                    if newToken.value == "str":
                        newToken.type = "type"
                    if newToken.value == "bool":
                        newToken.type = "type"

                    if newToken.value == "true":
                        newToken.type = "bool"
                    if newToken.value == "false":
                        newToken.type = "bool"
                    
                    self.next = newToken
                    return
                
        if c_char == ":":
            newToken.type = "atributte"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
            
        if c_char == "=":
            newToken.type = "equals"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            if self.source[self.position] == "=":
                newToken.type = "equalsTo"
                newToken.value += c_char
                self.next = newToken
                self.position += 1
                return
            return
        
        if c_char == ";":
            newToken.type = "endStatement"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            return
        
        if c_char == "<":
            newToken.type = "lessThan"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            if self.source[self.position] == "=":
                newToken.type = "lessOrEqualsTo"
                newToken.value += "="
                self.next = newToken
                self.position += 1
                return
            return
        
        if c_char == ">":
            newToken.type = "greaterThan"
            newToken.value = c_char
            self.next = newToken
            self.position += 1
            if self.source[self.position] == "=":
                newToken.type = "greaterOrEqualsTo"
                newToken.value += "="
                self.next = newToken
                self.position += 1
                return
            return
        
        if c_char == "&":
            if self.source[self.position+1] == "&":
                newToken.type = "and"
                newToken.value = "&&"
                self.next = newToken
                self.position += 2
                return
        
        if c_char == "|":
            if self.source[self.position+1] == "|":
                newToken.type = "or"
                newToken.value = "||"
                self.next = newToken
                self.position += 2
                return
        

        
        self.position += 1        
        self.selectNext()


# tkn = Tokenizer('"teste tesudo" false true')
# while tkn.next.type != "eof":
#     print(tkn.next.type, " - ", tkn.next.value)
#     tkn.selectNext()
