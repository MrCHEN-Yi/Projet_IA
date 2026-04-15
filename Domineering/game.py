class Domineering:
    def __init__(self, size=8):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.last_move = None  # On mémorise le dernier coup pour le colorer !

    def display(self):
        # Codes couleurs 
        BLEU = '\033[94m'
        JAUNE = '\033[93m'
        ROUGE = '\033[91m'  
        RESET = '\033[0m'   

        print("\n  " + " ".join(str(i) for i in range(self.size)))
        for r in range(self.size):
            row_display = []
            for c in range(self.size):
                cell = self.board[r][c]
                
                
                if self.last_move and (r, c) in self.last_move:
                    row_display.append(f"{ROUGE}{cell}{RESET}")
                elif cell == "V":
                    row_display.append(f"{BLEU}V{RESET}")
                elif cell == "H":
                    row_display.append(f"{JAUNE}H{RESET}")
                else:
                    row_display.append(cell)
                    
            print(f"{r} {' '.join(row_display)}")
        print()

    def get_legal_moves(self, player):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if player == "V":
                    if r + 1 < self.size and self.board[r][c] == "." and self.board[r+1][c] == ".":
                        moves.append(((r, c), (r+1, c)))
                elif player == "H":
                    if c + 1 < self.size and self.board[r][c] == "." and self.board[r][c+1] == ".":
                        moves.append(((r, c), (r, c+1)))
        return moves

    def play_move(self, move, player):
        (r1, c1), (r2, c2) = move
        self.board[r1][c1] = player
        self.board[r2][c2] = player
        self.last_move = move

    def undo_move(self, move):
        """Annule un coup. Très utile pour que l'IA simule des coups sans casser le vrai plateau."""
        (r1, c1), (r2, c2) = move
        self.board[r1][c1] = "."
        self.board[r2][c2] = "."
        