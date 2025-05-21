from Tokenizer import Tokenizer
from constants import SEQUENCE
from Node import *
from utils import print_tree
from SymbolTable import *


class Parser:
    tokenizer: Tokenizer
    node: Node

    def parseTab(self):
        token = self.tokenizer.next


        if token.type != "TAB":
            raise Exception("Expected a tab")
        self.tokenizer.selectNext()

        children = []

        while True:

            if self.tokenizer.next.type not in ["NUMBER", "UNPLAYED"]:
                raise Exception("Expected a number")
            if self.tokenizer.next.type == "NUMBER":
                if int(self.tokenizer.next.value) > 29:
                    raise Exception("Tab number too high") 
    
            children.append(self.tokenizer.next.value)
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == "TAB":
                self.tokenizer.selectNext()
                break

            if self.tokenizer.next.value != "-":
                raise Exception("")
            self.tokenizer.selectNext()

        if len(children) != 6:
            raise Exception("")
                

        return Tab(children, None)
    
    def parseFactor(self):
        token = self.tokenizer.next
        node = None
        
        if token.value in "+-!":
            self.tokenizer.selectNext()
            node = UnOp([self.parseFactor()], token.value)

        elif token.value == "(":
            self.tokenizer.selectNext()
            node = self.parseBoolExp()
            if self.tokenizer.next.value != ")":
                raise Exception("Unclosed parenthesis")
            else:
                self.tokenizer.selectNext()

        elif token.value == "GET":
            self.tokenizer.selectNext()
            if self.tokenizer.next.value == "(":
                node = Input([], None)
                self.tokenizer.selectNext()
            else:
                raise Exception("unexpected use of input")

            if self.tokenizer.next.value == ")":
                self.tokenizer.selectNext()
            else:
                raise Exception("Unclosed parenthesis")
            
        elif token.type == "IDENTIFIER":
            self.tokenizer.selectNext()
            node = Identifier([False], token.value)

        elif token.type == "NUMBER":
            self.tokenizer.selectNext()
            node = IntVal([], token.value)

        else:
            raise Exception("Unexpected Token")
        
        return node

    def parseTerm(self):
        node = self.parseFactor()

        while self.tokenizer.next.type == "operator" and self.tokenizer.next.value in ["*", "/"]:
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            right = self.parseFactor()

            if op.value == "*":
                node = BinOp([node, right], op.value)
            elif op.value == "/":
                node = BinOp([node, right], op.value)
        return node

    def parseExpression(self):
        node = self.parseTerm()

        while self.tokenizer.next.value in ["+", "-", "++"]:
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            right = self.parseTerm()

            if op.value == "+":
                node = BinOp([node, right], op.value)
            elif op.value == "-":
                node = BinOp([node, right], op.value)
            elif op.value =="++":
                node = BinOp([node, right], op.value)

        return node
    

    def ParseSongFactor(self):
        token = self.tokenizer.next
        node = None
    
        if token.type == "SONG_IDENTIFIER":
            self.tokenizer.selectNext()
            node = Identifier([True], token.value)
        
        elif token.value == "QUOTE":
            self.tokenizer.selectNext()
            
            children = []

            while True:
                if self.tokenizer.next.type == "SONG_IDENTIFIER":
                    children.append(Identifier([True], self.tokenizer.next.value))
                else:
                    tab = self.parseTab()
                    children.append(tab)

                if self.tokenizer.next.type == "QUOTE":
                    break
                self.tokenizer.selectNext()

            if self.tokenizer.next.type != "QUOTE":
                raise Exception("Unclosed quote")
            self.tokenizer.selectNext()

            node = Song(children, None)

        elif token.value == "GET":
            self.tokenizer.selectNext()
            if self.tokenizer.next.value == "(":
                node = Input([], None)
                self.tokenizer.selectNext()
            else:
                raise Exception("unexpected use of input")

            if self.tokenizer.next.value == ")":
                self.tokenizer.selectNext()
            else:
                raise Exception("Unclosed parenthesis")
            
        elif token.value == "(":
            self.tokenizer.selectNext()
            node = self.parseSongExpression()
            if self.tokenizer.next.value != ")":
                raise Exception("Unclosed parenthesis")
            
            self.tokenizer.selectNext()

        else:
            raise Exception("Unexpected Token")
        
        return node     

    def parseSongTerm(self):
        if self.tokenizer.next.type in ["NUMBER","SONG_IDENTIFIER"]:
            node = self.parseFactor()
            factor = True
        else:
            node = self.ParseSongFactor()
            factor = False

        while self.tokenizer.next.type == "OPERATOR" and self.tokenizer.next.value in ["**"]:
            op = self.tokenizer.next
            self.tokenizer.selectNext()

            if self.tokenizer.next.type in ["NUMBER","SONG_IDENTIFIER"]:
                right = self.ParseFactor()
                if factor:
                    raise Exception("operation between two numericals")
            else:
                right = self.ParseSongFactor()
                if not factor:
                    raise Exception("operation between two songs")
                
            if op.value == "**":
                node = BinOp([node, right], op.value)

        return node
    
    def parseSongExpression(self):
        node = self.parseSongTerm()

        while self.tokenizer.next.type == "OPERATOR" and self.tokenizer.next.value in ["++", "--"]:
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            right = self.parseSong()

            if op.value == "++":
                node = BinOp([node, right], op.value)
            elif op.value == "--":
                node = BinOp([node, right], op.value)

        return node


    def parseRelExp(self):
        if self.tokenizer.next.type in ["IDENTIFIER", "NUMBER"]:
            node = self.parseExpression()
        else:
            node = self.parseSongExpression()

        while self.tokenizer.next.type in ["EQ", "GT", "LT", "GTE", "LTE"]:
            op = self.tokenizer.next
            self.tokenizer.selectNext()

            if self.tokenizer.next.type in ["IDENTIFIER", "NUMBER"]:
                right = self.parseExpression()
            elif self.tokenizer.next.type == "SONG_IDENTIFIER":
                right = self.parseSongExpression()

            

            node = BinOp([node, right], op.value)

        return node

    def parseBoolTerm(self):
        node = self.parseRelExp()
    
        while self.tokenizer.next.type == "and":
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            right = self.parseRelExp()

            node = BinOp([node, right], op.value)

        return node
    
    def parseBoolExp(self):
        node = self.parseBoolTerm()

        while self.tokenizer.next.type == "or":
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            right = self.parseBoolTerm()

            node = BinOp([node, right], op.value)

        return node

    def parseStatement(self):

        token = self.tokenizer.next
        node = Node([], None)
        statementEnd = False

        if token.type == "IDENTIFIER":
            self.tokenizer.selectNext()
            id = Identifier([False], token.value)

            if self.tokenizer.next.type == "EQUAL":
                self.tokenizer.selectNext()
                node = Assignment([id, self.parseBoolExp()], None)
            else:
                raise SyntaxError("Set identifier like IDENTIFIER = VALUE")
       
        elif token.type == "SONG_IDENTIFIER":
            self.tokenizer.selectNext()
            id = Identifier([True], token.value)

            if self.tokenizer.next.type == "EQUAL":
                self.tokenizer.selectNext()
                node = Assignment([id, self.parseSongExpression()], None)
            else:
                raise SyntaxError("Set identifier like IDENTIFIER = VALUE")
            
        elif token.type == "VAR":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type not in ["IDENTIFIER", "SONG_IDENTIFIER"]:
                raise SyntaxError("Unproper declairing of variable")
            
            if self.tokenizer.next.type == "IDENTIFIER":
                id = Identifier([False], self.tokenizer.next.value)
            else:
                id = Identifier([True], self.tokenizer.next.value)

            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "EQUAL":
                self.tokenizer.selectNext()

                if id.children[0]:
                    node = VarDec([id, self.parseSongExpression()], "Song")
                else:
                    node = VarDec([id, self.parseBoolExp()], "int")

            else:
                if id.children[0]:
                    node = VarDec([id], "Song")
                else:
                    node = VarDec([id], "int")
                  
        elif token.type in ["PRINT", "PRINT_SONG"]:
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "OPEN_PAR":
                raise SyntaxError("Unproper use of print, proper: print(<expression>)")
            self.tokenizer.selectNext()
        
            if token.type == "PRINT":
                node = Print([self.parseBoolExp()], None)
            else:
                node = Print([self.parseSongExpression()], None)

            if self.tokenizer.next.type != "CLOSE_PAR":
                raise SyntaxError("Unproper use of print, proper: print(<expression>)")

            self.tokenizer.selectNext()

        elif token.type == "IF":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "OPEN_PAR":
                raise SyntaxError("Unproper use of if, proper: if(<condition>){<block>}[else{<block>}]")
            self.tokenizer.selectNext()

            condition = self.parseBoolExp()

            if self.tokenizer.next.type != "CLOSE_PAR":
                raise SyntaxError("Unproper use of if, proper: if(<condition>){<block>}[else{<block>}]")
            self.tokenizer.selectNext()
            
            onConditionTrue = self.parseBlock()

            conditionFalse = False
            if self.tokenizer.next.type == "ELSE":
                conditionFalse = True
                self.tokenizer.selectNext()
                onConditionFalse = self.parseBlock()
            
            if conditionFalse:
                node = Conditional([condition, onConditionTrue, onConditionFalse], None)
            else:
                node = Conditional([condition, onConditionTrue], None)

            statementEnd = True

        elif token.type == "WHILE":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "OPEN_PAR":
                raise SyntaxError("Unproper use of while, proper: while(<condition>){<block>}")
            self.tokenizer.selectNext()

            condition = self.parseBoolExp()

            if self.tokenizer.next.type != "CLOSE_PAR":
                raise SyntaxError("Unproper use of while, proper: while(<condition>){<block>}")
            self.tokenizer.selectNext()

            content = self.parseBlock()

            node = WhileLoop([condition, content], None)

            statementEnd = True

        elif token.type == "END_STATEMENT":
            pass
        
        else:
            raise Exception("Invalid Token")
        
        if not statementEnd:
            if self.tokenizer.next.type != "END_STATEMENT":
                raise SyntaxError("Unclosed statement")
            else:
                self.tokenizer.selectNext()


        return node

    def parseBlock(self):
        statements = []

        token = self.tokenizer.next
        if token.type != "OPEN_BRACKETS":
            raise SyntaxError('Start block with "{"')
        self.tokenizer.selectNext()        

        while self.tokenizer.next.type != "CLOSE_BRACKETS":
            statements.append(self.parseStatement())   

        self.tokenizer.selectNext()

        return Block(statements, None)

    def run(self, code):
        self.tokenizer = Tokenizer(code)
        self.tokenizer.selectNext()

        mainBlock = self.parseBlock()
        

        if self.tokenizer.next.type != "eof":
            raise Exception("Unexpected end of input")

        return mainBlock
