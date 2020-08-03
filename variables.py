class Var:
    def __init__(self, pos, number, color):
        self.number = number
        self.pos = pos
        self.color = color
        self.path = None
        self.domain = []
        self.head = False
        self.legal_paths = []
        self.colored = False

    def remove_value(self, is_backtrack):
        if self.head:
            if is_backtrack:
                self.colored = False
                return
            self.legal_paths = self.domain.copy()
        if not self.head:
            self.color = 0
            self.colored = False

    def set_value(self, color):
        self.color = color
        self.colored = True
