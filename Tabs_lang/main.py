import sys
from Parser import Parser
from utils import print_tree
from SymbolTable import SymbolTable

if __name__ == "__main__":
    
    filename = sys.argv[1]

    # filename = "test.Tabs"
    # filename = "smoke_on_the_water.Tabs"

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            input = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {e}")

    parser = Parser()
    mainBlock = parser.run(input)

    symbolTable = SymbolTable()
    mainBlock.Evaluate(symbolTable)


