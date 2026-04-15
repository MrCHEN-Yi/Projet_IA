import tkinter as tk
from tkinter import messagebox
from game import Domineering
from ai import ia_level_1, ia_level_2, ia_level_3

class DomineeringGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Domineering - Intelligence Artificielle")
        
        self.game = Domineering(size=8)
        self.current_player = "V"
        self.cell_size = 60  # Taille d'une case en pixels
        
        # Variables pour les options
        self.mode_var = tk.StringVar(value="1")
        self.human_role_var = tk.StringVar(value="V")
        
        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        """Crée les boutons et le menu en haut de la fenêtre."""
        menu_frame = tk.Frame(self.root, padx=10, pady=10)
        menu_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Colonne 1 : Choix du mode
        tk.Label(menu_frame, text="Mode de jeu :", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        tk.Radiobutton(menu_frame, text="1. Humain vs Humain", variable=self.mode_var, value="1").grid(row=1, column=0, sticky="w")
        tk.Radiobutton(menu_frame, text="2. Humain vs IA (Aléatoire)", variable=self.mode_var, value="2").grid(row=2, column=0, sticky="w")
        tk.Radiobutton(menu_frame, text="3. Humain vs IA (Gloutonne)", variable=self.mode_var, value="3").grid(row=3, column=0, sticky="w")
        tk.Radiobutton(menu_frame, text="4. Humain vs IA (Alpha-Beta)", variable=self.mode_var, value="4").grid(row=4, column=0, sticky="w")
        
        # Colonne 2 : Choix du camp (Qui commence ?)
        tk.Label(menu_frame, text="L'humain joue :", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky="w", padx=30)
        tk.Radiobutton(menu_frame, text="Vertical (Bleu - Commence)", variable=self.human_role_var, value="V").grid(row=1, column=1, sticky="w", padx=30)
        tk.Radiobutton(menu_frame, text="Horizontal (Jaune - Second)", variable=self.human_role_var, value="H").grid(row=2, column=1, sticky="w", padx=30)
        
        # Colonne 3 : Bouton Nouvelle Partie
        tk.Button(menu_frame, text="Nouvelle Partie", bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), command=self.reset_game).grid(row=1, column=2, rowspan=2, padx=20)
        
        # Label d'information (À qui le tour ?)
        self.status_label = tk.Label(self.root, text="Tour de : Vertical (Bleu)", font=("Arial", 14, "bold"), fg="#2980b9")
        self.status_label.pack(pady=5)
        
        # Zone de dessin (Canvas) pour la grille
        canvas_size = self.game.size * self.cell_size
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size, bg="white", highlightthickness=2, highlightbackground="black")
        self.canvas.pack(padx=20, pady=20)
        
        # Détection du clic de souris
        self.canvas.bind("<Button-1>", self.on_click)
        
    def reset_game(self):
        """Relance une partie à zéro."""
        self.game = Domineering(size=8)
        self.current_player = "V"
        self.update_status()
        self.draw_board()
        
        # Si c'est un mode IA et que l'humain a choisi de jouer en second (Horizontal)
        if self.mode_var.get() != "1" and self.human_role_var.get() == "H":
            self.root.after(500, self.ai_turn) # L'IA joue après 0.5 sec
            
    def draw_board(self):
        """Dessine la grille et les dominos."""
        self.canvas.delete("all")
        for r in range(self.game.size):
            for c in range(self.game.size):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell_val = self.game.board[r][c]
                color = "white"
                if cell_val == "V": color = "#3498db" # Bleu
                elif cell_val == "H": color = "#f1c40f" # Jaune
                
                # Mise en évidence du dernier coup en rouge
                outline_color = "black"
                outline_width = 1
                if self.game.last_move and (r, c) in self.game.last_move:
                    outline_color = "#e74c3c" # Rouge
                    outline_width = 3
                    
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline_color, width=outline_width)
                
    def on_click(self, event):
        """Géré quand le joueur clique sur la grille."""
        # On ignore si le jeu est fini ou si c'est le tour de l'IA
        if not self.game.get_legal_moves(self.current_player): return
        if self.mode_var.get() != "1" and self.current_player != self.human_role_var.get(): return
            
        # Calcul de la case cliquée
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        
        # Construction du coup selon le joueur
        move = ((r, c), (r+1, c)) if self.current_player == "V" else ((r, c), (r, c+1))
        
        # Vérification et application du coup
        if move in self.game.get_legal_moves(self.current_player):
            self.game.play_move(move, self.current_player)
            self.next_turn()
            
    def next_turn(self):
        """Passe au tour suivant et vérifie les conditions de victoire."""
        self.draw_board()
        self.current_player = "H" if self.current_player == "V" else "V"
        self.update_status()
        
        # Vérification de fin de partie
        if not self.game.get_legal_moves(self.current_player):
            winner = "Horizontal (Jaune)" if self.current_player == "V" else "Vertical (Bleu)"
            messagebox.showinfo("Fin de partie", f"Le joueur {self.current_player} est bloqué.\n\n🏆 Victoire de {winner} !")
            return
            
        # Déclenchement du tour de l'IA si nécessaire
        if self.mode_var.get() != "1" and self.current_player != self.human_role_var.get():
            self.root.after(100, self.ai_turn) # Laisse 100ms à l'interface pour se rafraîchir
            
    def update_status(self):
        """Met à jour le texte qui dit à qui c'est le tour."""
        if self.current_player == "V":
            self.status_label.config(text="Tour de : Vertical (Bleu)", fg="#2980b9")
        else:
            self.status_label.config(text="Tour de : Horizontal (Jaune)", fg="#f39c12")
            
    def ai_turn(self):
        """Fait jouer l'IA selon le niveau sélectionné."""
        legal_moves = self.game.get_legal_moves(self.current_player)
        if not legal_moves: return
        
        mode = self.mode_var.get()
        niveau_ia = int(mode) - 1
        self.status_label.config(text=f" L'IA (Niveau {niveau_ia}) réfléchit...", fg="#e67e22")
        self.root.update() # Force l'interface à afficher le texte de réflexion
        
        # Appel de tes fonctions d'IA
        if mode == "2":
            move = ia_level_1(legal_moves)
        elif mode == "3":
            move = ia_level_2(self.game, self.current_player, legal_moves)
        elif mode == "4":
            move = ia_level_3(self.game, self.current_player, legal_moves, depth=4)
            
        self.game.play_move(move, self.current_player)
        self.next_turn()

if __name__ == "__main__":
    root = tk.Tk()
    app = DomineeringGUI(root)
    root.mainloop()