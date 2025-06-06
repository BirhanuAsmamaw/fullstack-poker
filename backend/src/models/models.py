from pydantic import BaseModel, Field
from typing import List, Optional

class StartGameRequest(BaseModel):
    stack_size: int = Field(
        ...,
        gt=0,
        description="Initial stack size for all players (must be a positive integer)"
    )

class PreflopResponse(BaseModel):
    small_blind_index: int
    big_blind_index: int
    dealer_index: int
    preflop_dealings: List[str]

class GameStateResponse(BaseModel):
    indices: List[int]
    is_game_over : bool
    hand_id : Optional[str] = None
    final_pot : Optional[int] = None
    is_round_changed: bool
    street_index: Optional[int]
    current_player_index : int
    status: str
    bets: List[int]
    board : Optional[str] = None
    stacks: List[int]

class PlayerActionRequest(BaseModel):
    # Fold -> f
    # Check -> x
    # Call -> c
    # Bet AMOUNT -> bAMOUNT
    # Raise AMOUNT -> rAMOUNT
    # Allin -> allin
    action: str 
    amount: Optional[int] = None