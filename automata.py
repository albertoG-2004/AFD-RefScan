class Automata:
    def __init__(self):
        self.referencias = []
        self.current_reference = ""
        self.state = 'start'

    def transition(self, char, line_number, char_position):
        if self.state == 'start':
            if char == '(':
                self.state = 'initialParenthesis'
                self.current_reference += char
            else:
                self.reset()
        
        elif self.state == 'initialParenthesis':
            if char.isupper():
                self.state = "mayus"
                self.current_reference += char
            else:
                self.reset()

        elif self.state == 'mayus':
            if char.islower() or char in 'áéíóú':
                self.state = 'minus'
                self.current_reference += char
            else:
                self.reset()
        
        elif self.state == 'minus':
            if char.islower() or char in 'áéíóú':
                self.current_reference += char
            elif char == ' ':
                self.state = 'spacekey'
                self.current_reference += char
            elif char == ")":
                self.state = 'finalParenthesis'
                self.current_reference += char
                self.store_reference(line_number, char_position)
            else:
                self.reset()

        elif self.state == 'spacekey':
            if char == ' ':
                pass
            elif char.isdigit():
                self.state = 'int'
                self.current_reference += char
            else:
                self.reset()

        elif self.state == 'int':
            if char.isdigit():
                self.current_reference += char
            elif char == ')':
                self.state = 'finalParenthesis'
                self.current_reference += char
                self.store_reference(line_number, char_position)
            else:
                self.reset()

    def reset(self):
        self.state = 'start'
        self.current_reference = ""

    def store_reference(self, line_number, char_position):
        if self.current_reference and ')' in self.current_reference:
            self.referencias.append({
                "Referencia": self.current_reference,
                "Linea": line_number,
                "Columna": char_position - len(self.current_reference) + 1
            })
        self.reset()

    def find_references(self, text):
        self.referencias = []
        self.current_reference = ""
        self.state = 'start'
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            for char_position, char in enumerate(line, start=1):
                self.transition(char, line_number, char_position)

        self.store_reference(line_number, char_position)
        return self.referencias