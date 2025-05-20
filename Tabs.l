%{
#include "Tabs.tab.h"
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

struct symtab *symlook(char *s);

%}

%option noyywrap nounput noinput

%%

"get"           { return GET; }
"play"          { return PLAY; }
"print"         { return PRINT; }
"if"            { return IF; }
"else"          { return ELSE; }
"while"         { return WHILE; }

"||"            { return OR; }
"&&"            { return AND; }

":decat:"       { return DECAT; }
":concat:"      { return CONCAT; }
":pow:"         { return POWER; }

"=="            { return EQ; }
">="            { return GE; }
"<="            { return LE; }

">"             { return '>'; }
"<"             { return '<'; }
"="             { return '='; }
"+"             { return '+'; }
"-"             { return '-'; }
"*"             { return '*'; }
"/"             { return '/'; }
"!"             { return '!'; }

"("             { return '('; }
")"             { return ')'; }
"{"             { return '{'; }
"}"             { return '}'; }
";"             { return ';'; }

[0-9]+("."[0-9]+)?  {
                        yylval.dval = atof(yytext);
                        return NUMBER;
                    }

[ \t\n]+        { }

\"[^\"\n]*\"    {
                        char clean_val[128];
                        int len = yyleng - 2;
                        if (len < 0) len = 0;

                        if (len < sizeof(clean_val)) {
                            strncpy(clean_val, yytext + 1, len);
                            clean_val[len] = '\0';
                            yylval.symp = symlook(clean_val);
                            return TAB;
                        } else {
                            fprintf(stderr, "Lexical Error: TAB string too long: %s\n", yytext);
                            return YYerror;
                        }
                    }

[A-Z_][A-Z0-9_]* { yylval.symp = symlook(yytext); return SONG_IDENTIFIER; }

[a-z_][a-z0-9_]* { yylval.symp = symlook(yytext); return WORD; }

[a-zA-Z_][a-zA-Z0-9_]* { yylval.symp = symlook(yytext); return IDENTIFIER; }


.                   {
                        fprintf(stderr, "Lexical Error: Unrecognized character '%c'\n", yytext[0]);
                        return YYerror;
                    }

%%