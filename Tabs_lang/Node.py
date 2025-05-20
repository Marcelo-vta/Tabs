from var import Var

class Node():
    def __init__(self, children, value):
        self.children = children
        self.value = value
        return
    
    def Evaluate(self, symbolTable):
        pass

        
class Block(Node):
    def Evaluate(self, symbolTable):
        for child in self.children:
            child.Evaluate(symbolTable)
    
class BinOp(Node):
        
    def Evaluate(self, symbolTable):

        left = self.children[0].Evaluate(symbolTable)
        right = self.children[1].Evaluate(symbolTable)

        if left.type == "i32" and right.type == "i32":
            if self.value == "-":
                return Var("i32", left.value - right.value)
            if self.value == "+":
                return Var("i32", left.value + right.value)
            if self.value == "*":
                return Var("i32", left.value * right.value)
            if self.value == "/":
                return Var("i32", left.value // right.value)        
            
        if left.type == "bool" and right.type == "bool":
            if self.value == "||":
                return Var("bool", left.value or right.value)
            if self.value == "&&":
                return Var("bool", left.value and right.value)
        
        if left.type == right.type:
            if self.value == "==":
                return Var("bool", left.value == right.value)
            if self.value == ">=":
                return Var("bool", left.value >= right.value)
            if self.value == "<=":
                return Var("bool", left.value <= right.value)
            if self.value == "<":
                return Var("bool", left.value < right.value)
            if self.value == ">":
                return Var("bool", left.value > right.value)
        
        if self.value == "++":
            if left.type == "bool":
                left.value = str(left.value).lower()
            if right.type == "bool":
                right.value = str(right.value).lower()
            
            return Var("str", str(left.value) + str(right.value))
        
        raise Exception(f"unsupported type {left.type} or {right.type} for operand {self.value}")
        
        


class UnOp(Node):
    
    def Evaluate(self, symbolTable):
        child = self.children[0].Evaluate(symbolTable)

        if child.type == "i32":
            if self.value == "-":
                return Var("i32", -child.value)
            if self.value == "+":
                return Var("i32", +child.value)
        
        if child.type == "bool":        
            if self.value == "!":
                return Var("bool", not child.value)
        
        raise ValueError(f"unsupported type {child.type} for operand {self.value}")
    
            
class IntVal(Node):
    
    def Evaluate(self, symbolTable):
        return Var('i32' , int(self.value))
        
class BoolVal(Node):
    
    def Evaluate(self, symbolTable):
        return Var('bool', self.value == "true")
    
class StrVal(Node):
    
    def Evaluate(self, symbolTable):
        return Var('str' ,self.value)
    
        
class Identifier(Node):

    def Evaluate(self, symbolTable):
        return symbolTable.getSymbol(self.value)
    
class VarDec(Node):

    def Evaluate(self, symbolTable):

        id = self.children[0].value
        type = self.value

        if len(self.children) > 1:
            value = self.children[1].Evaluate(symbolTable)
        else:
            if type == "i32":
                value = Var("i32", 0)
            if type == "str":
                value = Var("str", "")
            if type == "bool":
                value = Var("bool", False)

        if type != value.type:
            raise Exception("Unexpected type")
        
        if symbolTable.containsSymbol(id):
            raise Exception("Variable Already Declared")
        
        symbolTable.setSymbol(id, Var(type, value.value)) 

class Assignment(Node):
    
    def Evaluate(self, symbolTable):
        id = self.children[0].value
        value = self.children[1].Evaluate(symbolTable)

        try:
            symbolTable.getSymbol(id)
        except:
            raise Exception(f"Variable {id} not declaired")

        symbolTable.setSymbolValue(id, value.value)

      
class NoOp(Node):
    pass

class Print(Node):

    def Evaluate(self, symbolTable):
        child = self.children[0].Evaluate(symbolTable)

        if child.type == "bool":
            child.value = str(child.value).lower()

        print(child.value)
    
    
class Conditional(Node):
    def Evaluate(self, symbolTable):
        conditional = self.children[0].Evaluate(symbolTable)
        if conditional.type != "bool":
            raise Exception("Incompatible types")

        if conditional.value:
            self.children[1].Evaluate(symbolTable)
        elif len(self.children) == 3:
            self.children[2].Evaluate(symbolTable)

class WhileLoop(Node):

    def Evaluate(self, symbolTable):
        conditional = self.children[0].Evaluate(symbolTable)
        if conditional.type != "bool":
            raise Exception("Incompatible types")

        while conditional.value:
            self.children[1].Evaluate(symbolTable)
            conditional = self.children[0].Evaluate(symbolTable)
    
class Input(Node):
    
    def Evaluate(self, symbolTable):
        return Var("i32", int(input()))


    


    




    
            
# number1 = IntVal(1)
# number2 = IntVal(2)
# number3 = IntVal(5)
# unop = UnOp([number1], "-")
# operator2 = BinOp([number2, number3], "*")
# operator = BinOp([operator2, unop], "+")
# mainNode = Node([operator], None)

            

