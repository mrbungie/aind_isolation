"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    loc = game.get_player_location(player)

    # Utility functions for handling winning or losing terminal states]
    if game.is_loser(player):
        return float("-inf")
 
    if game.is_winner(player):
        return float("inf")

    # Porcentage of remaining moves
    remaining_moves = float(len(game.get_blank_spaces()))/float(game.height*game.width)

    # Centrality Weight
    centrality_w = 1.0 - abs(float((loc[0] - game.height / 2. + loc[1] - game.width / 2.)))/float(game.width / 2. + game.height / 2.)

    # Centrality weigthed difference of my moves vs my opponent moves (weighted by porcentage of remaining moves)
    # As the game progresses the score moves from closed based to open based.
    return centrality_w*float(len(game.get_legal_moves(player)) - remaining_moves*len(game.get_legal_moves(game.get_opponent(player))))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    loc = game.get_player_location(player)

    # Utility functions for handling winning or losing terminal states
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Centrality Weight
    centrality_w  = 1.0 - abs(float((loc[0] - game.height / 2. + loc[1] - game.width / 2.)))/float(game.width / 2. + game.height / 2.)

    # Centrality weigthed difference of my moves vs my opponent moves
    return centrality_w*float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.get_opponent(player))))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    loc = game.get_player_location(player)

    # Utility functions for handling winning or losing terminal states
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Initiliazing centrality weight
    w = 1.0

    # Infinite score for the center
    if loc == (int(game.height / 2.),int(game.width / 2.)):
        return float("inf")
    
    # Punishing when scoring border boxes
    if loc[0] in [0,game.height-1] or loc[1] in [0,game.width-1]:
        w = 0.5

    # Centrality weigthed difference of my moves vs my opponent moves
    return w*float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.get_opponent(player))))



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        _, movement = self.eval_minimax(game, depth)
        return movement 


    def eval_minimax(self, game, depth, maximize=True):
        """ Implementation of minimax algorithm 
            Source: Based on https://en.wikipedia.org/wiki/Minimax#Pseudocode and
            https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md (but without separating in three functions)"""
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # checking for terminal state and if so, return utility and (-1, -1) move.
        if game.is_winner(game.active_player) or game.is_loser(game.active_player):
            return game.utility(self), (-1, -1)

        # returning score and position for leaves
        if depth == 0:
            return self.score(game, self), (-1, -1)

        # get possible moves
        possible_moves = game.get_legal_moves()

        # depending on the level (min or max), we set our initial best_score.
        if maximize:
            best_score = float('-inf')
        else:
            best_score = float('inf')

        # initializing best_movement
        best_movement = (-1, -1)

        # for each possible move, we check the next level in the tree.
        for legal_move in possible_moves:
            new_board = game.forecast_move(legal_move)
            score, movement = self.eval_minimax(new_board, depth - 1, not maximize)

            # depending on the level (min or max), we evaluate if the movement is better than the best we've seen
            if maximize:
                evaluation = (score >= best_score)
            else:
                evaluation = (score <= best_score)

            # shall it be better, we mark it as the best yet
            if evaluation:
                best_score = score
                best_movement = legal_move

        # we return the best movement and it's score
        return best_score, best_movement



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            # while the timer doesn't expire, we continue increasing depth iteratively
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            return best_move  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        _, movement, _, _ = self.eval_alphabeta(game, depth, alpha, beta)
        return movement

    def eval_alphabeta(self, game, depth, alpha, beta, maximize=True):
        """ Structurally based on my minimax implementation plus
            differences displayed between https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
            and https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # checking for terminal state and if so, return utility and (-1, -1) move.
        if game.is_winner(game.active_player) or game.is_loser(game.active_player):
            return game.utility(self), (-1, -1), alpha, beta

        # returning score and position for leaves
        if depth == 0:
            return self.score(game, self), (-1, -1), alpha, beta

        possible_moves = game.get_legal_moves()

        # depending on the level (min or max), we set our initial best_score.
        if maximize:
            best_score = float('-inf')
        else:
            best_score = float('inf')

        # initializing best_movement           
        best_movement = (-1, -1)

        # for each possible move, we check the next level in the tree.
        for legal_move in possible_moves:
            new_board = game.forecast_move(legal_move)
            score, movement, alpha_tmp, beta_tmp = self.eval_alphabeta(new_board, depth - 1, alpha, beta, not maximize)

            # depending on the level (min or max), we evaluate if the movement is better than the best we've seen
            # initially we would reach the deepest level, and set the first (non infinity based) alpha or beta depending on the level (max or min)
            # from then on, we prune when:
            #   - We're maximizing and we find a score bigger than our current beta.
            #   - We're minimizing and we find a score smaller than our current alpha. 
            # if we don't prune, we check if it's bigger (max level) or smaller (min level) and set it as the new alpha or beta accordingly.
            if maximize:
                evaluation = (score >= best_score)
                if score >= beta:
                    return score, legal_move, alpha, beta
                alpha = max(score, alpha_tmp)
            else:
                evaluation = (score <= best_score)
                if score <= alpha:
                    return score, legal_move, alpha, beta
                beta = min(score, beta_tmp)

            if evaluation:
                best_score = score
                best_movement = legal_move

        return best_score, best_movement, alpha, beta