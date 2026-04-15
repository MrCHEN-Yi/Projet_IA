from game import Domineering
from ai import ia_level_1, ia_level_2, ia_level_3

def get_human_move(player, legal_moves):
    while True:
        try:
            if player == "V":
                print("Joueur V (BLEU), entrez LIGNE et COLONNE du HAUT (ex: 0 0) :")
            else:
                print("Joueur H (JAUNE), entrez LIGNE et COLONNE de GAUCHE (ex: 0 0) :")
            
            entree = input("> ")
            r, c = map(int, entree.split())
            
            move = ((r, c), (r+1, c)) if player == "V" else ((r, c), (r, c+1))
                
            if move in legal_moves:
                return move
            else:
                print(" Coup invalide ou case occupée.")
        except ValueError:
            print(" Format incorrect. Entrez deux chiffres séparés par un espace.")

def main():
    print("="*35)
    print(" BIENVENUE DANS DOMINEERING ")
    print("="*35)
    print("1. Humain vs Humain")
    print("2. Humain vs IA (Niveau 1 - Aléatoire)")
    print("3. Humain vs IA (Niveau 2 - Gloutonne)")
    print("4. Humain vs IA (Niveau 3 - Alpha-Beta)") 
    
    choix = input("\nVotre choix (1-4) : ") 
    if choix not in ["1", "2", "3", "4"]:   
        print("Choix invalide, lancement du mode 1 par défaut.")
        choix = "1"

    jeu = Domineering(size=8)
    current_player = "V" 


    while True:
        jeu.display()
        legal_moves = jeu.get_legal_moves(current_player)

        if not legal_moves:
            adversaire = "H" if current_player == "V" else "V"
            print(f"\n FIN DE PARTIE ! {current_player} est bloqué.")
            print(f" LE JOUEUR {adversaire} GAGNE LA PARTIE ! ")
            break

        print(f"--- Tour de {current_player} ---")
        
        if choix == "1":
            move = get_human_move(current_player, legal_moves)
        elif choix == "2":
            if current_player == "V":
                move = get_human_move(current_player, legal_moves)
            else:
                move = ia_level_1(legal_moves)
        elif choix == "3":
            if current_player == "V":
                move = get_human_move(current_player, legal_moves)
            else:
            
                move = ia_level_2(jeu, current_player, legal_moves)
        elif choix == "4":
            if current_player == "V":
                move = get_human_move(current_player, legal_moves)
            else:
                move = ia_level_3(jeu, current_player, legal_moves, depth=4)
        # On joue le coup validé
        jeu.play_move(move, current_player)
        
        # On passe à l'autre joueur
        current_player = "H" if current_player == "V" else "V"

if __name__ == "__main__":
    main()