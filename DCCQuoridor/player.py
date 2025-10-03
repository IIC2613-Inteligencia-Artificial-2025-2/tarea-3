# NO TOCAR
class HumanPlayer:
    def __init__(self, name="Human"):
        self.name = name
        self.is_human = True

class MinimaxPlayer:
    def __init__(self, name, depth, eval_fun, use_alphabeta=True):
        self.name = name
        self.depth = depth
        self.is_human = False
        self.eval_fun = eval_fun
        self.use_alphabeta = use_alphabeta
