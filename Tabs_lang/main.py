import sys
from Parser import Parser
from utils import print_tree
from SymbolTable import SymbolTable

if __name__ == "__main__":
    
    # input = '''
    #     {

    #     rep = get();
        
    #     A = "|0-2-2-X-X-X|";
    #     B = "|1-3-3-X-X-X|";
    #     C = "|2-4-4-X-X-X|";

    #     SONG = "";

    #     i = 0;
    #     while (i < rep){
    #         SONG = SONG ++ A ++ B ++ C;
    #         if (i == (rep - 1) ){
    #             SONG = SONG ++ "|X-X-X-X-X-X|";
    #         }
    #         i = i + 1;
    #     }

    #     prints(SONG);

    #     SONG = SONG -- "|X-X-X-X-X-X|";

    #     prints(SONG);

    #     // pode ser tambem

    #     SONG2 = (A ++ B ++ C)**rep;

    #     // ou

    #     SONG3 = "|0-2-2-X-X-X|, |1-3-3-X-X-X|, |2-4-4-X-X-X|" ** rep;

    #     print(SONG == SONG2);
    #     print(SONG2 == SONG3);

    #     }

    # '''

    filename = "test.Tabs"
    # filename = sys.argv[1]

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


