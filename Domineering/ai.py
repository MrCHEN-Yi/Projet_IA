import random

# optique de almelioration : La Table de Transposition (Mémoïsation).

# ==========================================
# NIVEAU 1 : L'IA Aléatoire
# ==========================================
def ia_level_1(legal_moves):
    print(" L'IA (Niveau 1) joue au hasard...")
    return random.choice(legal_moves)

# ==========================================
# NIVEAU 2 : L'IA Gloutonne (1 coup d'avance)
# ==========================================
def ia_level_2(game, player, legal_moves):
    print(" L'IA (Niveau 2) évalue la meilleure position immédiate...")
    opponent = "H" if player == "V" else "V"
    
    best_score = -float('inf')
    best_moves = []

    for move in legal_moves:
        game.play_move(move, player)
        mes_coups = len(game.get_legal_moves(player))
        ses_coups = len(game.get_legal_moves(opponent))
        score = mes_coups - ses_coups
        game.undo_move(move)
        
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)

# ==========================================
# NIVEAU 3 : L'IA Stratège (Minimax + Alpha-Beta)
# ==========================================

def evaluate_board(game, player):
    """Calcule le score du plateau pour un joueur donné."""
    opponent = "H" if player == "V" else "V"
    mes_coups = len(game.get_legal_moves(player))
    ses_coups = len(game.get_legal_moves(opponent))
    return mes_coups - ses_coups


def minimax(game, depth, alpha, beta, is_maximizing, current_player, original_player):
    """Algorithme Minimax récursif avec élagage Alpha-Beta et détection de victoire."""
    legal_moves = game.get_legal_moves(current_player)
    
    
    random.shuffle(legal_moves)  # Move Ordering (a revoir )

    if not legal_moves:
        if current_player == original_player:
            return -10000 
        else:
            return 10000 
            
    if depth == 0:
        # OPTIMISATION : On compte juste l'adversaire car on connaît déjà nos coups
        opponent = "H" if current_player == "V" else "V"
        mes_coups = len(legal_moves) if current_player == original_player else len(game.get_legal_moves(original_player))
        ses_coups = len(legal_moves) if opponent == current_player else len(game.get_legal_moves(opponent))
        return mes_coups - ses_coups
        
    opponent = "H" if current_player == "V" else "V"
    
    if is_maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            game.play_move(move, current_player)
            eval_score = minimax(game, depth - 1, alpha, beta, False, opponent, original_player)
            game.undo_move(move)
            
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
        
    else:
        min_eval = float('inf')
        for move in legal_moves:
            game.play_move(move, current_player)
            eval_score = minimax(game, depth - 1, alpha, beta, True, opponent, original_player)
            game.undo_move(move)
            
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

def ia_level_3(game, player, legal_moves, depth=4):
    print(f" L'IA (Niveau 3) calcule le futur sur {depth} coups d'avance...")
    best_score = -float('inf')
    best_moves = []
    
    opponent = "H" if player == "V" else "V"
    
    for move in legal_moves:
        game.play_move(move, player)
        
        #  OPTIMISATION : Si ce coup bloque totalement l'adversaire direct, on gagne, pas besoin de réfléchir !
        if not game.get_legal_moves(opponent):
            game.undo_move(move)
            return move

        score = minimax(game, depth - 1, -float('inf'), float('inf'), False, opponent, player)
        game.undo_move(move)
        
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
            
    return random.choice(best_moves)


"""
L'IA est passée d'un simple compteur de cases aveugle à un stratège 
doté d'un véritable instinct de survie : en attribuant des scores absolus
(+10000 pour la victoire, -10000 pour la défaite), elle a arrêté de se 
suicider mathématiquement et cherche désormais activement à achever son
adversaire tout en préservant ses propres zones de sécurité.
"""

# def minimax(game, depth, alpha, beta, is_maximizing, current_player, original_player):
#     """Algorithme Minimax récursif avec élagage Alpha-Beta."""
#     legal_moves = game.get_legal_moves(current_player)
    
#     # Condition d'arrêt : on a atteint la limite de profondeur OU la partie est finie
#     if depth == 0 or not legal_moves:
#         return evaluate_board(game, original_player)
        
#     opponent = "H" if current_player == "V" else "V"
    
#     if is_maximizing:
#         max_eval = -float('inf')
#         for move in legal_moves:
#             game.play_move(move, current_player)
#             eval_score = minimax(game, depth - 1, alpha, beta, False, opponent, original_player)
#             game.undo_move(move)
            
#             max_eval = max(max_eval, eval_score)
#             alpha = max(alpha, eval_score)
#             if beta <= alpha:
#                 break # Élagage Beta (On arrête d'explorer cette branche inutile)
#         return max_eval
        
#     else:
#         min_eval = float('inf')
#         for move in legal_moves:
#             game.play_move(move, current_player)
#             eval_score = minimax(game, depth - 1, alpha, beta, True, opponent, original_player)
#             game.undo_move(move)
            
#             min_eval = min(min_eval, eval_score)
#             beta = min(beta, eval_score)
#             if beta <= alpha:
#                 break # Élagage Alpha
#         return min_eval


#  
# def ia_level_3(game, player, legal_moves, depth=4):
#     """
#     Lance la recherche Minimax. 
#     depth=4 signifie qu'elle anticipe 4 tours à l'avance (toi, elle, toi, elle).
#     """
#     print(f" L'IA (Niveau 3) calcule le futur sur {depth} coups d'avance...")
#     best_score = -float('inf')
#     best_moves = []
    
#     opponent = "H" if player == "V" else "V"
    
#     for move in legal_moves:
#         game.play_move(move, player)
#         # On simule la réponse de l'adversaire (is_maximizing = False)
#         score = minimax(game, depth - 1, -float('inf'), float('inf'), False, opponent, player)
#         game.undo_move(move)
        
#         if score > best_score:
#             best_score = score
#             best_moves = [move]
#         elif score == best_score:
#             best_moves.append(move)
            
#     return random.choice(best_moves)


"Pour optimiser l'élagage Alpha-Beta, j'ai implémenté un système"
" de 'Move Ordering' basique avec un shuffle. Au lieu de toujours"
" évaluer les cases de haut en bas (qui peuvent être des scénarios"
" catastrophiques et ralentir l'élagage), le mélange aléatoire"
" augmente statistiquement la probabilité de trouver un 'bon coup' "
"(cutoff) plus tôt dans la boucle, ce qui accélère drastiquement"
" la coupe des branches inutiles."


# get_legal_moves(player) -> 64 vérifications
# get_legal_moves(opponent) -> 64 vérifications
# Total = 128 vérifications par feuille de l'arbre.