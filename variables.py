class Var:
    def __init__(self, pos, number, color):
        self.number = number
        self.pos = pos
        self.color = color
        self.path = None
        self.domain = None
        self.head = False
        self.legal_paths = []

    def remove_value(self):
        self.legal_paths = self.domain.copy()
        if not self.head:
            self.color = 0

    def set_value(self, color):
        self.color = color


