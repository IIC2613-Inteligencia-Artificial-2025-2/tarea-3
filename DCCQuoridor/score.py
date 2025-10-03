def evaluate(game, player_idx):
    if game.winner is not None:
        return 1e9 if game.winner.index == player_idx else -1e9
    
    opp_idx = 1 - player_idx
    dmy = game.shortest_distance_for(player_idx)
    dopp = game.shortest_distance_for(opp_idx)

    if dmy == 0: return 1e9
    if dopp == 0: return -1e9

    my_walls = game.board.pawns[player_idx].walls_left
    opp_walls = game.board.pawns[opp_idx].walls_left

    tempo = 0.01 if (game.turn % 2) == player_idx else -0.01
    score = (dopp - dmy) + 0.1*(my_walls - opp_walls) + tempo

    return score


def chat_gpt_eval(game, player_idx):
    if game.winner is not None:
        return 1e9 if game.winner.index == player_idx else -1e9

    opp_idx = 1 - player_idx
    my_dist = game.shortest_distance_for(player_idx)
    opp_dist = game.shortest_distance_for(opp_idx)

    if my_dist == 0:
        return 1e9
    if opp_dist == 0:
        return -1e9

    my_pawn = game.board.pawns[player_idx]
    opp_pawn = game.board.pawns[opp_idx]

    dist_score = (opp_dist - my_dist) * 2.0

    wall_diff = my_pawn.walls_left - opp_pawn.walls_left
    wall_weight = 0.35 if my_dist >= opp_dist else 0.2
    wall_score = wall_diff * wall_weight

    center_col = game.board.size // 2
    my_center_offset = abs(my_pawn.pos.c - center_col)
    opp_center_offset = abs(opp_pawn.pos.c - center_col)
    center_score = (opp_center_offset - my_center_offset) * 0.15

    my_progress = abs(my_pawn.pos.r - my_pawn.goal)
    opp_progress = abs(opp_pawn.pos.r - opp_pawn.goal)
    progress_score = (opp_progress - my_progress) * 0.4

    tempo = 0.15 if (game.turn % 2) == player_idx else -0.15

    return dist_score + wall_score + center_score + progress_score + tempo

# Acá defines tus funciones de evaluación
