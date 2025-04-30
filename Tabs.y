%token <symp> TAB
%token <symp> SONG_IDENTIFIER
%token <symp> IDENTIFIER
%token <symp> WORD
%token <dval> NUMBER

%left 'and'
%left 'or'
%left '<' '<=' '==' '>=' '>'
%left '+' '-'
%left '*' '/'
%left '+' '-' '!'
%left '++' '--'
%left '**'

%type <dval> Expression

block: '{' multiple_statements '}'

multiple_statements: 
    | multiple_statements statement

statement: 
      assignment ";"
    | ";"
    | print ";"
    | play ";"
    | while
    | condition
    | ";"


assignment: IDENTIFIER "=" bool_expression

song_assignment: SONG_IDENTIFIER "=" song_expression


print:  
      "print" "(" bool_expression ")"
    | "print" "(" song_expression ")"

play: "play" "(" song_expression ")"


while: "while" "(" bool_expression ")" block

condition: 
     "if" "(" bool_expression ")" block
    | "if" "(" bool_expression ")" block "else" block


bool_expression: 
      bool_term
    | bool_expression "or" bool_term

bool_term: 
      rel_expression
    | bool_term "and" rel_expression

factor:
      NUMBER
    | IDENTIFIER
    | "+" factor
    | "-" factor
    | "!" factor
    | "(" bool_expression ")"
    | "get"


song_expression:
      song_term
    | song_expression "++" song_term
    | song_expression "--" song_term

song_term:
      song_factor "**" factor
    | factor "**" song_factor

song_factor:
      song
    | SONG_IDENTIFIER
    | "(" song_expression ")"


song: '"' multiple_tabs '"'

multiple_tabs:
    | multiple_tabs TAB ","





