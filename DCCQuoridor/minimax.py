# minimax.py
NEG_INF = float("-inf")
POS_INF = float("inf")

def _eval_terminal_or_heur(game, fixed_player_id, eval_function):
    # NO TOCAR
    # Si alguien ganó, se aplican los puntajes máximos
    if game.winner is not None:
        return POS_INF if game.winner.index == fixed_player_id else NEG_INF
    # Si no, se usa la función de evaluación heurística
    return eval_function(game, fixed_player_id)

def _apply_move_clone(game, mv):
    # NO TOCAR
    g2 = game.clone()
    kind, (r, c) = mv
    if kind == 'move':
        ok = g2.move_pawn(r, c)
    elif kind == 'hwall':
        ok = g2.place_horiz(r, c)
    else:
        ok = g2.place_vert(r, c)
    return g2, ok

def minimax(game, player_id, fixed_player_id, depth, max_player, use_alphabeta, eval_function, alpha=NEG_INF, beta=POS_INF):
    # Caso base donde se corta por profundidad o estado terminal
    if depth == 0 or game.winner is not None:
        return _eval_terminal_or_heur(game, fixed_player_id, eval_function), None

    # Generar movimientos
    moves = game.get_all_moves()
    if not moves:
        # Si no hay jugadas no formzamos derrota, sino que la heurística decide
        return _eval_terminal_or_heur(game, fixed_player_id, eval_function), None

    # Determinar si este nodo es MAX (mueve fixed_player_id) o MIN (mueve el rival)
    is_max = (game.turn % 2) == fixed_player_id
    base_my  = game.shortest_distance_for(fixed_player_id)
    base_opp = game.shortest_distance_for(1 - fixed_player_id)

    best_score = NEG_INF if is_max else POS_INF
    best_move = None
    best_prog = None

    for mv in moves:
        g2, ok = _apply_move_clone(game, mv)
        if not ok:
            continue  # Movimiento ilegal, saltar

        # Si la jugada gana inmediatamente, devolvemos el extremo correspondiente
        if g2.winner is not None:
            if g2.winner.index == fixed_player_id:
                return POS_INF, mv
            score = NEG_INF
        else:
            score, _ = minimax(g2, 1 - player_id, fixed_player_id, depth - 1, not is_max, use_alphabeta, eval_function, alpha, beta)
        
        # Casos de empates, en MAX preferimos que las distancias disminuyan o que la del rival aumente, en MIN lo contrario.
        my_after  = g2.shortest_distance_for(fixed_player_id)
        opp_after = g2.shortest_distance_for(1 - fixed_player_id)
        if is_max:
            prog = (base_my - my_after, opp_after - base_opp)
            better = (score > best_score) or (score == best_score and (best_prog is None or prog > best_prog))
        else:
            prog = (my_after - base_my, base_opp - opp_after)  # "peor" para MAX = "mejor" para MIN
            better = (score < best_score) or (score == best_score and (best_prog is None or prog > best_prog))

        if better:
            best_score = score
            best_move  = mv
            best_prog  = prog

            
        # Poda alfa-beta
        if use_alphabeta:
            # COMPLETAR
            pass

    return best_score, best_move