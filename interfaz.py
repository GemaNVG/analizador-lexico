import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QTextEdit, QVBoxLayout, QSizePolicy, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from lexico import AnalizadorLexico


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador léxico")
        self.setGeometry(400, 100, 600, 500)

        # Crear la barra de menú
        self.crear_menu()

        # Widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal vertical
        layout_principal = QVBoxLayout()

        # Cuadro de texto para "Analizar"
        self.text_input = self.crear_txt_edit("Texto para analizar")
        self.text_input.setEnabled(False)
        self.text_input.textChanged.connect(self.actualizar_botones)

        # Cuadro de texto para "Tokens generados"
        self.tokens_output = self.crear_txt_edit("Tokens generados", editable=False)

        # Cuadro de texto para "Errores encontrados"
        self.errors_output = self.crear_txt_edit("Errores encontrados", editable=False)

        # Botón "Limpiar"
        self.limpiar_btn = QPushButton("Limpiar (Ctrl+L)")
        self.limpiar_btn.setShortcut(QKeySequence("Ctrl+L"))
        self.limpiar_btn.setEnabled(False)
        self.limpiar_btn.clicked.connect(self.limpiar_campos)

        # Añadir widgets al layout principal
        layout_principal.addWidget(self.text_input)
        layout_principal.addWidget(self.tokens_output)
        layout_principal.addWidget(self.errors_output)
        layout_principal.addWidget(self.limpiar_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Asignar el layout al widget central
        central_widget.setLayout(layout_principal)

    def crear_menu(self):
        """Crear la barra de menú con secciones."""
        menu_bar = self.menuBar()

        # Secciones de la barra de opciones
        self.seccion_texto = QAction("Texto (Ctrl+T)", self)
        self.seccion_texto.setShortcut(QKeySequence("Ctrl+T"))
        self.seccion_archivo = QAction("Archivo (Ctrl+A)", self)
        self.seccion_archivo.setShortcut(QKeySequence("Ctrl+A"))
        self.seccion_analizar = QAction("Analizar (Ctrl+E)", self)
        self.seccion_analizar.setShortcut(QKeySequence("Ctrl+E"))
        self.seccion_analizar.setEnabled(False)

        # Añadir acciones a la barra de menú
        menu_bar.addAction(self.seccion_texto)
        menu_bar.addAction(self.seccion_archivo)
        menu_bar.addAction(self.seccion_analizar)

        # Conectar acciones a métodos
        self.seccion_texto.triggered.connect(self.accion_texto)
        self.seccion_archivo.triggered.connect(self.accion_archivo)
        self.seccion_analizar.triggered.connect(self.accion_analizar)

    def accion_texto(self):
        """Acción al presionar el botón 'TEXTO'."""
        self.text_input.setEnabled(True)
        self.text_input.setFocus()
        self.seccion_archivo.setText("Guardar (Ctrl+G)")
        self.seccion_archivo.setShortcut(QKeySequence("Ctrl+G"))

    def accion_archivo(self):
        """Acción al presionar el botón 'ARCHIVO'."""
        if self.text_input.isEnabled():
            self.guardar_archivo()
        else:
            self.abrir_archivo()

    def abrir_archivo(self):
        """Abrir un archivo de texto."""
        self.file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo de texto", "", "Archivos de texto (*.txt)"
        )

        if self.file_path:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.contenido = file.read()
                    self.text_input.clear()  # Limpiar el contenido anterior
                    self.text_input.setPlainText(self.contenido)
                    self.text_input.setEnabled(True)  # Habilitar el cuadro de texto
                    self.text_input.setReadOnly(True)  # Establecer en modo solo lectura
                    self.text_input.verticalScrollBar().setValue(0)  # Ajustar al inicio del documento
                    self.actualizar_botones()
            except Exception as e:
                print(f"Error al leer el archivo: {e}")

    def cargar_buffer(self):
        extraer_texto = self.text_input.toPlainText()
        file = extraer_texto.splitlines()  # Esto es una lista de líneas
        buffer = []
        cont = 0
        
        while file:
            # Añade línea por línea en lugar de toda la lista
            for linea in file:
                buffer.append(linea)
                cont += 1
                
                # Si el buffer alcanza 10 líneas o no hay más líneas, devuelve el contenido
                if cont == 10:
                    buf = "\n".join(buffer)  # Une las líneas con saltos de línea
                    cont = 0
                    yield buf
                    buffer = []  # Limpia el buffer después de generarlo
            
            # Vuelve a cargar `file` como lista vacía para terminar el bucle
            file = []

        # Si quedan líneas en el buffer al finalizar, se devuelven
        if buffer:
            buf = "\n".join(buffer)
            yield buf

    def guardar_archivo(self):
        """Guardar el contenido del cuadro de texto en un archivo."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo de texto", "", "Archivos de texto (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    contenido = self.text_input.toPlainText()
                    file.write(contenido)
                    print("Archivo guardado exitosamente.")
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")

    def accion_analizar(self):
        """Acción al presionar el botón 'ANALIZAR'."""
        self.buffer = self.cargar_buffer()
        self.Analyzer = AnalizadorLexico()

        # Inicialización de listas para almacenar resultados
        token = []
        lexema = []
        renglon = []
        columna = []
        errors = []  # Lista para recolectar mensajes de error

        # Tokenizar y cargar el buffer
        for i in self.buffer:
            try:
                # Intentar tokenizar el código
                t, lex, lin, col, errs = self.Analyzer.tokenizar(i)
                # Agregar tokens reconocidos a las listas
                token += t
                lexema += lex
                renglon += lin
                columna += col
                errors += errs
            except RuntimeError as e:
                # Agregar el error a la lista sin interrumpir la iteración
                errors.append(str(e))

        # Crear la salida de tokens reconocidos
        tokens_recognized = "\n".join(
            f"Linea {lin} = Token tipo {tok} donde Lexema es '{lex}' en la Columna: {col}"
            for lin, tok, lex, col in zip(renglon, token, lexema, columna)
        )
        # Formatear errores para la salida
        errors_output = "\n".join(errors) if errors else "No se encontraron errores."

        print("Analizando texto...")

        # Mostrar tokens y errores en la interfaz
        self.tokens_output.setText(tokens_recognized)
        self.errors_output.setText(errors_output)


    def crear_txt_edit(self, placeholder_text, editable=True):
        """Crear un QTextEdit con barras de desplazamiento y un texto de marcador."""
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder_text)
        text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        text_edit.setAcceptRichText(False)
        text_edit.setReadOnly(not editable)
        text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        return text_edit

    def limpiar_campos(self):
        """Limpiar los cuadros de texto."""
        self.text_input.clear()
        self.tokens_output.clear()
        self.errors_output.clear()
        self.text_input.setReadOnly(False)
        self.text_input.setEnabled(False)
        self.actualizar_botones()
        self.seccion_archivo.setText("Archivo (Ctrl+A)")
        self.seccion_archivo.setShortcut(QKeySequence("Ctrl+A"))

    def actualizar_botones(self):
        """Actualizar el estado de los botones según el contenido del cuadro de texto."""
        hay_texto = bool(self.text_input.toPlainText())
        self.limpiar_btn.setEnabled(hay_texto)
        self.seccion_analizar.setEnabled(hay_texto)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


