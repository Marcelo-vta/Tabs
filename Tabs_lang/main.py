import sys
from Parser import Parser
from utils import print_tree
from SymbolTable import SymbolTable

if __name__ == "__main__":
    # input = sys.argv[1]
    
    # input = """
    #     {
    #         var x_1:i32;
    #         x_1 = reader();
            
    #         printf(x_1);
            
    #         if ((x_1 > 1 && !!!(x_1 < 1)) || x_1 == 3) {
    #             x_1 = 2;
    #         }
            
    #         var x:i32 = 3+6/3   *  2 -+-  +  2*4/2 + 0/1 -((6+ ((4)))/(2)); // Teste // Teste 2
    #         var y_1:i32 = 3;
    #         y_1 = y_1 + x_1;
    #         var z__:i32;
    #         z__ = x + y_1;
            
    #         if (x_1 == 2) {
    #             x_1 = 2;
    #         }
            
    #         if (x_1 == 3) {
    #             x_1 = 2;
    #         } else {
    #             x_1 = 3;
    #         }
            
    #         x_1 = 0;
    #         while (x_1 < 1 || x == 2) {
    #             printf(x_1);
    #             x_1 = x_1 + 1;
    #         }
            
            
    #         ;;;
    #         // Saida final
    #         printf(x_1);
    #         printf(x);
    #         printf(z__+1);
            
    #         // All int operations
    #         var y:i32 = 2;
    #         var z:i32;
    #         z = (y - 1);
    #         printf(y+z);
    #         printf(y-z);
    #         printf(y*z);
    #         printf(y/z);
    #         printf(y == z);
    #         printf(y < z);
    #         printf(y > z);
            
    #         // All str operations 
    #         var a:str;
    #         var b:str;
            
    #         x_1 = 1;
    #         y = 1; 
    #         z = 2;
    #         a = "abc";
    #         b = "def";
    #         printf(a++b);
    #         printf(a++x_1);
    #         printf(x_1++a);
    #         printf(y++z);
    #         printf(a++(x_1==1));
    #         printf(a == a);
    #         printf(a < b);
    #         printf(a > b);
    #         }
    # """

    filename = sys.argv[1]

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


