import re

class AnalizadorLexico:
    # Token renglon
    lin_num = 1

    def tokenizar(self, codigo):
        reglas = [
            # Palabras reservadas
            (r'BEGIN', 'palabra_reservada_BEGIN'),            # Inicio de un bloque de código
            (r'END', 'palabra_reservada_END'),                # Fin de un bloque de código
            (r'PROCEDURE', 'palabra_reservada_PROCEDURE'),    # Declaración de una función
            (r'DO', 'palabra_reservada_DO'),                  # Hacer algo
            (r'PRINT', 'palabra_reservada_PRINT'),            # Impresión de un mensaje
            (r'AND', 'palabra_reservada_AND'),                # Operador lógico AND
            (r'OR', 'palabra_reservada_OR'),                  # Operador lógico OR
            (r'NOT', 'palabra_reservada_NOT'),                # Operador lógico NOT
            (r'IF', 'palabra_reservada_IF'),                  # Inicio de una condición
            (r'ELSE', 'palabra_reservada_ELSE'),              # Opción alternativa en una condición
            (r'ENDIF', 'palabra_reservada_ENDIF'),            # Fin de una condición
            (r'REPEAT', 'palabra_reservada_REPEAT'),          # Inicio de un ciclo
            (r'UNTIL', 'palabra_reservada_UNTIL'),            # Fin de un ciclo
            # Operadores
            (r'\+', 'operador_mas'),                          # Operador de suma
            (r'-', 'operador_menos'),                         # Operador de resta
            (r'\*', 'operador_multiplicacion'),               # Operador de multiplicación
            (r'/', 'operador_division'),                      # Operador de división
            (r'=', 'operador_igual'),                         # Operador de igualdad
            # Especiales
            (r'"', 'especial_comillas'),                      # Comillas
            (r',', 'especial_coma'),                          # Coma
            (r';', 'especial_punto_coma'),                    # Punto y coma
            (r'\(', 'especial_parentesis_izquierdo'),         # Paréntesis izquierdo
            (r'\)', 'especial_parentesis_derecho'),           # Paréntesis derecho
            (r'#', 'especial_hashtag'),                       # Hashtag
            # Constantes numericas
            (r'\d+', 'cons_num_entero'),                      # Números enteros
            # Constantes de caracteres
            (r'"[A-Z]+"', 'cons_caracteres'),                 # Cadenas de texto
            # Identificadores
            (r'[A-Z]+', 'identificadores'),                   # Identificadores
            # Otros
            (r'\n', 'NEWLINE'),                               # Nueva línea
            (r'[ \t]+', 'SKIP'),                              # Espacios en blanco
            (r'.', 'MISMATCH'),                               # Caracteres no reconocidos
            (r'"[A-Z]+"', 'COMMENT'),                         # Comentarios
        ]
        
        tokens_join = '|'.join(f'(?P<{name}>{pattern})' for pattern, name in reglas)
        lin_start = 0

        
        # Listas de salida del programa
        token = []
        lexema = []
        renglon = []
        columna = []
        errores = []

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
                col = m.start() - lin_start
                errores.append(f'Error inesperado en línea {self.lin_num}, columna {col}: "{token_lexema}" no es un token válido.')
            elif token_type == 'ID':
                if not token_lexema.isupper():
                    col = m.start() - lin_start
                    errores.append(f'Error de identificador en línea {self.lin_num}, columna {col}: "{token_lexema}" debe estar en mayúsculas.')
            else:
                col = m.start() - lin_start
                columna.append(col)
                token.append(token_type)
                lexema.append(token_lexema)
                renglon.append(self.lin_num)
    
        return token, lexema, renglon, columna, errores