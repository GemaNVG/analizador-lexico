import re

class AnalizadorLexico:
    # Token renglon
    lin_num = 1

    def tokenizar(self, codigo):
        # Verificar si el código contiene letras minúsculas
        if any(char.islower() for char in codigo):
            print("El código contiene letras minúsculas. Solo se permiten letras mayúsculas.")
        reglas = [
            # Palabras reservadas
            (r'BEGIN', 'BEGIN'),            # Inicio de un bloque de código
            (r'END', 'END'),                # Fin de un bloque de código
            (r'PROCEDURE', 'PROCEDURE'),    # Declaración de una función
            (r'DO', 'DO'),                  # Hacer algo
            (r'PRINT', 'PRINT'),            # Impresión de un mensaje
            (r'AND', 'AND'),                # Operador lógico AND
            (r'OR', 'OR'),                  # Operador lógico OR
            (r'NOT', 'NOT'),                # Operador lógico NOT
            (r'IF', 'IF'),                  # Inicio de una condición
            (r'ELSE', 'ELSE'),              # Opción alternativa en una condición
            (r'ENDIF', 'ENDIF'),            # Fin de una condición
            (r'REPEAT', 'REPEAT'),          # Inicio de un ciclo
            (r'UNTIL', 'UNTIL'),            # Fin de un ciclo
            # Operadores
            (r'\+', 'PLUS'),                # Operador de suma
            (r'-', 'MINUS'),                # Operador de resta
            (r'\*', 'MULT'),                # Operador de multiplicación
            (r'/', 'DIV'),                  # Operador de división
            (r'=', 'EQUAL'),                # Operador de igualdad
            # Especiales
            (r'"', 'QUOTE'),                # Comillas
            (r',', 'COMMA'),                # Coma
            (r';', 'SEMICOLON'),            # Punto y coma
            (r'\(', 'LPAREN'),              # Paréntesis izquierdo
            (r'\)', 'RPAREN'),              # Paréntesis derecho
            (r'#', 'HASH'),                 # Hashtag
            # Constantes numericas
            (r'\d+', 'NUMBER_INT'),         # Números enteros
            # Constantes de caracteres
            (r'".*?"', 'STRING'),           # Cadenas de texto
            # Identificadores
            (r'[A-Z]\w*', 'ID'),            # Identificadores
            # Otros
            (r'\n', 'NEWLINE'),             # Nueva línea
            (r'[ \t]+', 'SKIP'),            # Espacios en blanco
            (r'.', 'MISMATCH'),             # Caracteres no reconocidos
        ]
        
        tokens_join = '|'.join(f'(?P<{name}>{pattern})' for pattern, name in reglas)
        lin_start = 0

        
        # Listas de salida del programa
        token = []
        lexema = []
        renglon = []
        columna = []

        # Analiza el código para encontrar los lexemas y sus respectivos Tokens
        for m in re.finditer(tokens_join, codigo):
                    token_type = m.lastgroup
                    token_lexema = m.group(token_type)

                    if token_type == 'NEWLINE':
                        lin_start = m.end()
                        self.lin_num += 1
                    elif token_type == 'SKIP':
                        continue
                    elif token_type == 'MISMATCH':
                        # Columna donde ocurre el error
                        col = m.start() - lin_start
                        print('Error inesperado en linea %d, columna %d: "%s" no es un token valido.' % (self.lin_num, col, token_lexema))
                    else:
                            col = m.start() - lin_start
                            columna.append(col)
                            token.append(token_type)
                            lexema.append(token_lexema)
                            renglon.append(self.lin_num)
                            # Para imprimir información sobre un token
                            print('Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'.format(token_type, token_lexema, self.lin_num, col))

        return token, lexema, renglon, columna