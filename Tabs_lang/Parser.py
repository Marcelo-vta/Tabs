from Tokenizer import Tokenizer
from constants import SEQUENCE
from Node import *
from utils import print_tree
from SymbolTable import *


class Parser:
    tokenizer: Tokenizer
    node: Node

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

        elif token.value == "reader":
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
            
        elif token.type == "identifier":
            self.tokenizer.selectNext()
            node = Identifier([], token.value)

        elif token.type == "number":
            self.tokenizer.selectNext()
            node = IntVal([], token.value)

        elif token.type == "bool":
            self.tokenizer.selectNext()
            node = BoolVal([], token.value)

        elif token.type == "string":
            self.tokenizer.selectNext()
            node = StrVal([], token.value)

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
    
    def parseRelExp(self):
        node = self.parseExpression()

        while self.tokenizer.next.type in ["equalsTo", "greaterThan", "lessThan", "greaterOrEqualsTo", "lessOrEqualsTo"]:
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            right = self.parseExpression()

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

        if token.type == "identifier":
            self.tokenizer.selectNext()
            id = Identifier([], token.value)

            if self.tokenizer.next.type == "equals":
                self.tokenizer.selectNext()
                node = Assignment([id, self.parseBoolExp()], None)
            else:
                raise SyntaxError("Set identifier like IDENTIFIER = VALUE")
            
        elif token.type == "setVar":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "identifier":
                raise SyntaxError("Unproper declairing of variable")
            id = Identifier([], self.tokenizer.next.value)
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "atributte":
                raise SyntaxError("Unproper declairing of variable")
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "type":
                raise SyntaxError("Unknown type of variable")
            type = self.tokenizer.next.value
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == "equals":
                self.tokenizer.selectNext()

                node = VarDec([id, self.parseBoolExp()], type)
            else:
                node = VarDec([id], type)
                  
        elif token.type == "print":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "openPrio":
                raise SyntaxError("Unproper use of print, proper: print(<expression>)")
            self.tokenizer.selectNext()

            node = Print([self.parseBoolExp()], None)

            if self.tokenizer.next.type != "closePrio":
                raise SyntaxError("Unproper use of print, proper: print(<expression>)")

            self.tokenizer.selectNext()

        elif token.type == "if":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "openPrio":
                raise SyntaxError("Unproper use of if, proper: if(<condition>){<block>}[else{<block>}]")
            self.tokenizer.selectNext()

            condition = self.parseBoolExp()

            if self.tokenizer.next.type != "closePrio":
                raise SyntaxError("Unproper use of if, proper: if(<condition>){<block>}[else{<block>}]")
            self.tokenizer.selectNext()
            
            onConditionTrue = self.parseBlock()

            conditionFalse = False
            if self.tokenizer.next.type == "else":
                conditionFalse = True
                self.tokenizer.selectNext()
                onConditionFalse = self.parseBlock()
            
            if conditionFalse:
                node = Conditional([condition, onConditionTrue, onConditionFalse], None)
            else:
                node = Conditional([condition, onConditionTrue], None)

            statementEnd = True

        elif token.type == "while":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "openPrio":
                raise SyntaxError("Unproper use of while, proper: while(<condition>){<block>}")
            self.tokenizer.selectNext()

            condition = self.parseBoolExp()

            if self.tokenizer.next.type != "closePrio":
                raise SyntaxError("Unproper use of while, proper: while(<condition>){<block>}")
            self.tokenizer.selectNext()

            content = self.parseBlock()

            node = WhileLoop([condition, content], None)

            statementEnd = True

        elif token.type == "endStatement":
            pass
        
        else:
            print(self.tokenizer.next.type)
            print(self.tokenizer.position)
            raise Exception("Invalid Token")
        
        if not statementEnd:
            if self.tokenizer.next.type != "endStatement":
                raise SyntaxError("Unclosed statement")
            else:
                self.tokenizer.selectNext()


        return node

    def parseBlock(self):
        statements = []

        token = self.tokenizer.next
        if token.type != "openBlock":
            raise SyntaxError('Start block with "{"')
        
        self.tokenizer.selectNext()

        while self.tokenizer.next.type != "closeBlock":
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
