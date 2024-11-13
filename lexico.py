import re

class AnalizadorLexico:
    reglas = [
        # Palabras reservadas
        (r'begin', 'BEGIN'),
        (r'end', 'END'),
        (r'procedure', 'PROCEDURE'),
        (r'do', 'DO'),
        (r'print', 'PRINT'),
        (r'and', 'AND'),
        (r'or', 'OR'),
        (r'not', 'NOT'),
        (r'if', 'IF'),
        (r'else', 'ELSE'),
        (r'endif', 'ENDIF'),
        (r'repeat', 'REPEAT'),
        (r'until', 'UNTIL'),
        # Operadores
        (r'\+', 'PLUS'),
        (r'-', 'MINUS'),
        (r'\*', 'MULT'),
        (r'/', 'DIV'),
        (r'=', 'EQUAL'),
        # Especiales
        (r'"', 'QUOTE'),
        (r',', 'COMMA'),
        (r';', 'SEMICOLON'),
        (r'\(', 'LPAREN'),
        (r'\)', 'RPAREN'),
        (r'#', 'HASH'),
        # Constantes numericas
        (r'\d(\d)*', 'NUMBER_INT'),
        # Constantes de caracteres
        (r'".*"', 'STRING'),
        # Identificadores
        (r'[A-Z]\w*', 'ID')
    ]