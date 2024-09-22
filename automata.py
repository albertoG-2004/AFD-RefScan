class Automata:
    def __init__(self):
        self.referencias = []
        self.current_reference = ""
        self.state = 'start'

    def transition(self, char):
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
            if char.islower():
                self.state = 'minus'
                self.current_reference += char
            else:
                self.reset()
        
        elif self.state == 'minus':
            if char.islower():
                self.current_reference += char
            elif char == ' ':
                self.state = 'spacekey'
                self.current_reference += char
            else:
                self.reset()

        elif self.state == 'spacekey':
            if char.isdigit():
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
                self.store_reference()
            else:
                self.reset()
    
    def reset(self):
        self.state = 'start'
        self.current_reference = ""

    def store_reference(self):
        if self.current_reference:
            self.referencias.append(self.current_reference)
        self.reset()
    
    def find_references(self, text):
        print(f"Texto recibido: {text}")
        self.referencias = []
        self.current_reference = ""
        self.state = 'start'
        for char in text:
            self.transition(char)

        self.store_reference()
        return self.referencias