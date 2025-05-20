import re

numbers = [str(n) for n in range(10)]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
ALPHAS = [alpha for alpha in (alphabet + alphabet.lower())];

VOCABULARY = [" ","\n","+","-","*","/","(",")", "{", "}","=","_",";","<",">","&","|", '"', ":"] + numbers + ALPHAS

SEQUENCE = {
    "number": ["operator", "eof"],
    "operator": ["number"],
    "": ["number"],
    "prio": ["number"],
}
