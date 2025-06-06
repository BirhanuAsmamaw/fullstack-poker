from uuid import uuid4
from pokerkit import Automation, NoLimitTexasHoldem
from typing import List, Optional
from src.db.dataclass import PokerHand
from src.db.db_setup import get_connection
from src.repositories.poker_repository import PokerHandRepository
from src.models.models import PreflopResponse, GameStateResponse
from src.exceptions.game_exception import GameNotStartedException, InvalidActionException, InsufficientBetsOrRaiseException
from src.utils.utils import generate_unique_hole_cards, card_formatter

class GameStateManagerService:
    _instance = None

    def __init__(self):
        self.state: Optional[NoLimitTexasHoldem] = None
        self.hand_id: Optional[str] = uuid4()
        self.stack_size : Optional[int] = 0
        self.dealer_index : Optional[int]
        self.hand_pots : List[int] = [0]
        self.actions : List[str] = []
        self.player_hands: List[str] = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_game(self, stack_size: int, num_players: int = 6):
        """
        Initializes the game state with the given stack size and number of players.
        Args:
            stack_size (int): The initial stack size for each player.
            num_players (int): The number of players in the game.
            Returns:
            
            NoLimitTexasHoldem: The initialized game state.
        """
        # If there is an ongoing game, continue. Otherwise create a new game
        self.end_game()
        self.stack_size = stack_size
        self.state = NoLimitTexasHoldem.create_state(
            (
                Automation.BET_COLLECTION,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
            ),
            True,  # Uniform antes
            0,     # No ante
            (20, 40),  # SB/BB
            80,    # Min-bet
            tuple([stack_size] * num_players),
            num_players
        )
        return self.state
    
    def end_game(self):
        """
        Ends the current game and resets the state.
        """
        self.state = None
        self.winnings = 0
        self.actions = []
        self.player_hands = []
        self.hand_pots = [0]
        
    
    def get_current_player_index(self) -> int:
        """
        Returns the index of the current player.
        Raises:
            Exception: If the game has not started or if the state is None.
        """
        if self.state is None:
            raise GameNotStartedException("Game not started.")
        return self.state.actor_index
    
    def deal_board(self):
        """
        Deals the flop by burning a card and dealing 3 cards to the board.
        Raises:
            Exception: If the game has not started or if the state is None.
        """
        if self.state is None:
            raise GameNotStartedException("Game not started.")
        self.state.burn_card()
        return self.state.deal_board() 
    
    def fold(self, action:str):
        if self.state is None:
            raise GameNotStartedException("Game not started.")
        if not self.state.can_fold():
            raise InvalidActionException("Cannot fold right now.")
        
        current_player_index = self.get_current_player_index()
        self.state.fold()
        self.actions.append(f"{action}:")
        return self.advance_game_state(current_player_index)

    def check_or_call(self, action:str):
        if self.state is None:
            raise GameNotStartedException("Game not started.")
        current_player_index = self.get_current_player_index()
        try:
            self.state.check_or_call()
            self.actions.append(f"{action}:")
        except ValueError as e:
            raise InvalidActionException(f"Cannot check or call: {str(e)}")
        
        return self.advance_game_state(current_player_index)

    def complete_bet_or_raise_to(self, action: str, amount: int):
        if self.state is None:
            raise GameNotStartedException("Game not started.")
        if not self.state.can_complete_bet_or_raise_to():
            raise InvalidActionException("Cannot bet or raise right now.")
        
        current_player_index = self.get_current_player_index()
        try:
            self.state.complete_bet_or_raise_to(amount)
            if action == "allin":
                self.actions.append(f"{action}:")
            else:
                self.actions.append(f"{action}{amount}")
        except ValueError as e:
            raise InsufficientBetsOrRaiseException(f"Cannot complete bet or raise to {amount}: {str(e)}")

        return self.advance_game_state(current_player_index)
    
    def allin(self, action):
        curr_player = self.get_current_player_index()
        amount = self.state.stacks[curr_player]
        return self.complete_bet_or_raise_to(action, amount)

    def preflop_response(self):
        """
        Deals hole cards to players and returns the preflop response.
        Returns:
            PreflopResponse: Contains indices of small blind, big blind, dealer, and the dealt hole cards.
        """
        num_players = 6
        hole_cards = generate_unique_hole_cards(num_players)
        if self.state is None:
            raise Exception("Game state is not initialized")

        for cards in hole_cards:
            self.state.deal_hole(cards)

        actor_indices = self.state.actor_indices
        first_actor = actor_indices[0]
        dealer_index = (first_actor - 2) % num_players
        small_blind_index = (dealer_index + 1) % num_players
        big_blind_index = (dealer_index + 2) % num_players

        preflop_dealings = hole_cards
        self.player_hands = preflop_dealings

        self.dealer_index = dealer_index

        print(f"Dealer index: {dealer_index}, Small blind index: {small_blind_index}, Big blind index: {big_blind_index}")
        print(f"Preflop dealings: {preflop_dealings}")
        print(type(preflop_dealings[0]))

        return PreflopResponse(
            small_blind_index=small_blind_index,
            big_blind_index=big_blind_index,
            dealer_index=dealer_index,
            preflop_dealings=preflop_dealings
        )
    
    def advance_game_state(self, current_player_index) -> GameStateResponse:
        """
        Advances the game state to the next round if applicable.
        Returns:
            GameStateResponse: The current game state after advancing.
        """
        is_round_changed = False
        if self.state is None:
            raise GameNotStartedException("Game not started.")
        card_str = None
        is_game_over = False
        final_pot_amount = list(self.state.pot_amounts)
        print(final_pot_amount)

        if final_pot_amount and final_pot_amount[0] != 0:
            self.hand_pots.append(final_pot_amount[0])

        if not self.state.actor_indices:
            if self.state.street_index is not None:
                public_card = self.deal_board()
                is_round_changed = True
                card_str = card_formatter(public_card.cards)
                self.actions.append(f" {card_str} ")
            else:
                is_game_over = True
                self.persist_hand()

            
        return GameStateResponse(
            indices=list(self.state.actor_indices),
            is_round_changed=is_round_changed,
            is_game_over=is_game_over,
            hand_id=str(self.hand_id),
            final_pot=self.hand_pots[-1],
            street_index=self.state.street_index,
            current_player_index=current_player_index,
            status=str(self.state.status),
            board=card_str,
            bets=list(self.state.bets),
            stacks=list(self.state.stacks)
        )

    def persist_hand(self):
        if self.state is None:
            raise GameNotStartedException("Game not started yet")   

        hand = PokerHand(
            hand_id=self.hand_id,
            winnings=self.state.payoffs,  
            stack_size=self.stack_size,  
            dealer=self.dealer_index,
            actions=self.actions,
            player_hands=self.player_hands
        )

        with get_connection() as conn:
            repo = PokerHandRepository(conn)
            repo.save(hand)