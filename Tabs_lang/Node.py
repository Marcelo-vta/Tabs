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

        if left.type == "number" and right.type == "number":
            if self.value == "-":
                return Var("number", left.value - right.value)
            if self.value == "+":
                return Var("number", left.value + right.value)
            if self.value == "*":
                return Var("number", left.value * right.value)
            if self.value == "/":
                return Var("number", left.value // right.value)        
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

        if left.type == "song" and right.type == "song":
            if self.value == "++":
                return Var("song", left.value + right.value)
            if self.value == "--":
                return Var("song", [x for x in left.value if x not in right.value])
            if self.value == "==":
                return Var("bool", left.value == right.value)
            if self.value == ">=":
                return Var("bool", len(left.value) >= len(right.value))
            if self.value == "<=":
                return Var("bool", len(left.value) <= len(right.value))
            if self.value == "<":
                return Var("bool", len(left.value) < len(right.value))
            if self.value == ">":
                return Var("bool", len(left.value) > len(right.value))

        if left.type != right.type:
            if left.type == "song":
                song = left
                number = right
            else:
                song = right
                number = left
        
            if self.value == "==":
                return Var("bool", number.value == len(song.value))
            if self.value == ">=":
                return Var("bool", len(number.value) >= len(song.value))
            if self.value == "<=":
                return Var("bool", len(number.value) <= len(song.value))
            if self.value == "<":
                return Var("bool", len(number.value) < len(song.value))
            if self.value == ">":
                return Var("bool", len(number.value) > len(song.value))
        
        raise Exception(f"unsupported type {left.type} or {right.type} for operand {self.value}")
        
        


class UnOp(Node):
    
    def Evaluate(self, symbolTable):
        child = self.children[0].Evaluate(symbolTable)

        if child.type == "number":
            if self.value == "-":
                return Var("number", -child.value)
            if self.value == "+":
                return Var("number", +child.value)
            
        raise ValueError(f"unsupported type {child.type} for operand {self.value}")
    
            
class IntVal(Node):
    
    def Evaluate(self, symbolTable):
        return Var('number' , int(self.value))
        
class BoolVal(Node):
    
    def Evaluate(self, symbolTable):
        return Var('bool', self.value == "true")
    
class StrVal(Node):
    
    def Evaluate(self, symbolTable):
        return Var('str' ,self.value)
    
class Tab(Node):

    def Evaluate(self, symbolTable):
        return self.children

class Song(Node):

    def Evaluate(self, symbolTable):
        tabs = []
        for child in self.children:
            tabs.append(child.Evaluate(symbolTable))
        return Var('song', tabs)
        
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
            if type == "number":
                value = Var("number", 0)
            if type == "song":
                value = Var("song", [])

        if type != value.type:
            raise Exception("Unexpected type")
        
        if symbolTable.containsSymbol(id):
            raise Exception("Variable Already Declared")
        
        symbolTable.setSymbol(id, Var(type, value.value)) 

class Assignment(Node):
    
    def Evaluate(self, symbolTable):
        id = self.children[0].value
        type = "song" if self.children[0].children[0] else "number"

        try:
            symbolTable.getSymbol(id)
        except:
            VarDec([Var(None, id), self.children[1]], type).Evaluate(symbolTable)
        else:
            value = self.children[1].Evaluate(symbolTable)
            symbolTable.setSymbolValue(id, value)


      
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

            

