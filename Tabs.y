%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct symtab {
    char *name;
    double value; // add a value if variables store numbers
};

struct symtab *symlook(char *s);
double get_value(struct symtab *sym);

int yylex(void);
void yyerror(const char *s) { fprintf(stderr, "Error: %s\n", s); }
%}

%union {
    double dval;
    struct symtab *symp;
}

// Tokens with values
%token <symp> TAB
%token <symp> SONG_IDENTIFIER
%token <symp> IDENTIFIER
%token <symp> WORD
%token <dval> NUMBER
%token GET PLAY PRINT IF ELSE WHILE
%token OR AND

%token DECAT CONCAT POWER
%token EQ GE LE

// Operator precedence
%left OR
%left AND
%left '<' LE EQ GE '>'
%left '+' '-'
%left '*' '/'
%left '!'          // unary
%left DECAT CONCAT
%left POWER

// Types
%type <dval> factor bool_expression bool_term rel_expression
%type <dval> song_expression song_term
%type <dval> song_factor

%%

// Top-level rule
block: '{' multiple_statements '}';

multiple_statements:
    | multiple_statements statement;

statement:
      assignment ';'
    | song_assignment ';'
    | print ';'
    | play ';'
    | while
    | condition
    | ';';

assignment: IDENTIFIER '=' bool_expression {
    $1->value = $3;
};

song_assignment: SONG_IDENTIFIER '=' song_expression {
    $1->value = $3;
};

print:
      PRINT '(' bool_expression ')'
    | PRINT '(' song_expression ')';

play: PLAY '(' song_expression ')';

while: WHILE '(' bool_expression ')' block;

condition:
      IF '(' bool_expression ')' block
    | IF '(' bool_expression ')' block ELSE block;

bool_expression:
      bool_term
    | bool_expression OR bool_term { $$ = $1 || $3; };

bool_term:
      rel_expression
    | bool_term AND rel_expression { $$ = $1 && $3; };

rel_expression:
      factor
    | factor '<' factor  { $$ = $1 < $3; }
    | factor LE factor   { $$ = $1 <= $3; }
    | factor EQ factor   { $$ = $1 == $3; }
    | factor GE factor   { $$ = $1 >= $3; }
    | factor '>' factor  { $$ = $1 > $3; };

factor:
      NUMBER                  { $$ = $1; }
    | IDENTIFIER              { $$ = get_value($1); }
    | '+' factor              { $$ = +$2; }
    | '-' factor              { $$ = -$2; }
    | '!' factor              { $$ = !$2; }
    | '(' bool_expression ')' { $$ = $2; }
    | GET                     { $$ = 1; /* or real input logic */ };

song_expression:
      song_term
    | song_expression DECAT song_term { $$ = $1 + $3; }
    | song_expression CONCAT song_term { $$ = $1 - $3; };

song_term:
      song_factor POWER factor { $$ = $1 * $3; }
    | factor POWER song_factor { $$ = $1 * $3; };

song_factor:
      WORD               { $$ = 1; /* placeholder */ }
    | SONG_IDENTIFIER    { $$ = get_value($1); }
    | '(' song_expression ')' { $$ = $2; };

%%

double get_value(struct symtab *sym) {
    return sym ? sym->value : 0;
}
