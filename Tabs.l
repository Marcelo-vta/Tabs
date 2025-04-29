get {
    return INPUT;
}

play {
    return PLAY;
}

print {
    return PRINT;
}

if {
    return IF;
}

else {
    return ELSE;
}

or {
    return OR;
}

and {
    return AND;
}


( \|[0-2][0-9](-[0-2][0-9]){5}\| ) {
    char clean_val[32];
    strncpy(clean_val, yytext + 2, strlen(yytext) - 4);
    clean_val[strlen(yytext) - 4] = '\0';

    struct symtab *sp = symlook(clean_val);
    yyval.symp = sp;
    return TAB;
}

[A-Z][A-Z0-9]* {
    struct symtab *sp = symlook(yytext);
    yylval.symp = sp;
    return SONG_IDENTIFIER;
}

[a-zA-Z][a-zA-Z0-9]* {
    struct symtab *sp = symlook(yytext);
    yylval.symp = sp;
    return IDENTIFIER;
}

[A-Z]+ {
    struct symtab *sp = symlook(yytext);
    yylval.symp = sp;
    return WORD;
}

[0-9]+ {
    yyval.dval = atof(yytext);
    return NUMBER;
}


\+\+ {
    return SONG_OPERATOR_CONCAT;
}

-- {
    return SONG_OPERATOR_REMOVE;
}

\*\* {
    return SONG_OPERATOR_MULT;
}


\+ {
    return OPERATOR_SUM;
}

- {
    return OPERATOR_MINUS;
}

\* {
    return OPERATOR_MULT;
}

/ {
    return OPERATOR_DIV;
}

! {
    return OPERATOR_NEG;
}


\( {
    return OPEN_PAR;
}

\) {
    return CLOSE_PAR;
}

\{ {
    return OPEN_CB;
}

\} {
    return CLOSE_CB;
}


" {
    return SONG_DELIMITER;
}


== {
    return BOOL_OPERATOR_EQUALS;
}

> {
    return BOOL_OPERATOR_GREATER;
}

< {
    return BOOL_OPERATOR_LESS;
}

>= {
    return BOOL_OPERATOR_GREATEROREQUAL;
}

<= {
    return BOOL_OPERATOR_LESSOREQUAL;
}


= {
    return ASSIGN;
}


. { return yytext[0]; }