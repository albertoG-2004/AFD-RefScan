class Automata:
    def __init__(self):
        self.referencias = []
        self.current_reference = ""
        self.state = 'A'

    def transition(self, char, line_number, char_position):
        if self.state == 'A':
            if char == '(':
                self.state = 'q1'
                self.current_reference += char
            else:
                self.reset()
        
        elif self.state == 'q1':
            if char.isupper() and char not in 'ÁÉÍÓÚ':
                self.state = 'q2'
                self.current_reference += char
            elif char in 'ÁÉÍÓÚ':
                self.state = 'q3'
                self.current_reference += char
            else:
                self.reset()

        elif self.state == 'q2':
            if char.islower() and char not in 'áéíóú':
                self.state = 'q8'
                self.current_reference += char
            elif char in 'áéíóú':
                self.state = 'q3'
                self.current_reference += char
            else:
                self.reset()

        elif self.state == 'q3':
            if char.islower() and char not in 'áéíóú':
                self.state = 'q5'
                self.current_reference += char
            else:
                self.reset()

        elif self.state == 'q5':
            if char.islower() and char not in 'áéíóú':
                self.current_reference += char
            elif char == ' ':
                self.state = 'q6'
                self.current_reference += char
            elif char == ")":
                self.state = 'q4'
                self.current_reference += char
                self.store_reference(line_number, char_position)
            else:
                self.reset()
            
        elif self.state == 'q6':
            if char == ' ':
                pass
            elif char.isdigit():
                self.state = 'q7'
                self.current_reference += char
            else:
                self.reset()

        elif self.state == 'q7':
            if char.isdigit():
                self.current_reference += char
            elif char == ')':
                self.state = 'q4'
                self.current_reference += char
                self.store_reference(line_number, char_position)
            else:
                self.reset()

        elif self.state == 'q8':
            if char.islower() and char not in 'áéíóú':
                self.current_reference += char
                print("q8")
            elif char in 'áéíóú':
                self.state = 'q9'
                self.current_reference += char
            elif char == ' ':
                self.state = 'q6'
                self.current_reference += char
            elif char == ")":
                self.state = 'q4'
                self.current_reference += char
                self.store_reference(line_number, char_position)
            else:
                self.reset()
        
        elif self.state == 'q9':
            if char.islower() and char not in 'áéíóú':
                self.current_reference += char
            elif char == ' ':
                self.state = 'q6'
                self.current_reference += char
            elif char == ")":
                self.state = 'q4'
                self.current_reference += char
                self.store_reference(line_number, char_position)
            else:
                self.reset()

    def reset(self):
        self.state = 'A'
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
        self.state = 'A'
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            for char_position, char in enumerate(line, start=1):
                self.transition(char, line_number, char_position)

        self.store_reference(line_number, char_position)
        return self.referencias