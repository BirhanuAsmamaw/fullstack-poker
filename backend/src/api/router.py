from fastapi import APIRouter, HTTPException
from src.db.db_setup import get_connection
from src.repositories.poker_repository import PokerHandRepository
from src.models.models import PlayerActionRequest, StartGameRequest
from src.services.game_state_manager_service import GameStateManagerService
from math import inf

router = APIRouter()

@router.post("/start/game", status_code=200)
def start_game(req: StartGameRequest):
    manager = GameStateManagerService.get_instance()
    state = manager.start_game(stack_size=req.stack_size)
    preflop_response = GameStateManagerService.get_instance().preflop_response()

    try:
        return {"message": "Hole cards dealt successfully", "cards": preflop_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to deal hole cards: {str(e)}")

@router.post("/action/fold")
def fold_action(req: PlayerActionRequest):
    manager = GameStateManagerService.get_instance()
    try:
        return manager.fold(req.action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/action/check_or_call")
def check_or_call_action(req: PlayerActionRequest):
    manager = GameStateManagerService.get_instance()
    try:
        return manager.check_or_call(req.action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/action/complete_bet_or_raise_to")
def complete_bet_or_raise_to_action(req: PlayerActionRequest):
    manager = GameStateManagerService.get_instance()
    try:
        if req.amount is None:
            raise HTTPException(status_code=400, detail="Amount is required for betting or raising.")
        return manager.complete_bet_or_raise_to(req.action, req.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/action/allin")
def allin(req: PlayerActionRequest):
    manager = GameStateManagerService.get_instance()
    try:
        return manager.allin(req.action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/history")
def list_all_hands():
    with get_connection() as conn:
        repo = PokerHandRepository(conn)
        return repo.list_all()