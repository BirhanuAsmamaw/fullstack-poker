# tests/test_hand_routes.py
from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from fastapi import status
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

def test_start_game():
    response = client.post("/hand/start/game", json={"stack_size": 10000})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hole cards dealt successfully"
    assert "cards" in data
    # you can also assert on the shape of preflop_response if you know it:
    assert isinstance(data["cards"]["preflop_dealings"], list)


from src.services.game_state_manager_service import GameStateManagerService

# Automatically reset the singleton before each test
@pytest.fixture(autouse=True)
def reset_game_manager():
    GameStateManagerService._instance = None
    yield
    GameStateManagerService._instance = None


def test_start_game_success():
    payload = {"stack_size": 10000}
    resp = client.post("/hand/start/game", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    # Should have a success message and a "cards" object
    assert data["message"] == "Hole cards dealt successfully"
    assert "cards" in data

    cards = data["cards"]
    # "cards" should be a dict with small_blind_index, big_blind_index, dealer_index, preflop_dealings
    assert isinstance(cards, dict)
    assert isinstance(cards["small_blind_index"], int)
    assert isinstance(cards["big_blind_index"], int)
    assert isinstance(cards["dealer_index"], int)
    assert isinstance(cards["preflop_dealings"], list)
    # There should be exactly 6 hole‐card strings (one per player)
    assert len(cards["preflop_dealings"]) == 6


def test_fold_without_start_game_returns_400():
    # If we call /action/fold before starting, GameNotStartedException should bubble up as HTTP 400
    resp = client.post("/hand/action/fold", json={"action": "f"})
    assert resp.status_code == 400
    detail = resp.json().get("detail", "")
    assert "Game not started" in detail or "Cannot fold" in detail or "GameNotStartedException"

def test_check_or_call_without_start_game_returns_400():
    resp = client.post("/hand/action/check_or_call", json={"action": "c"})
    assert resp.status_code == 400
    detail = resp.json().get("detail", "")
    assert "Game not started" in detail

def test_complete_bet_or_raise_to_without_game_started_returns_400():
    # Even if we supply amount, calling this before start_game should return 400
    resp = client.post("/hand/action/complete_bet_or_raise_to", json={"action": "b", "amount": 500})
    assert resp.status_code == 400
    detail = resp.json().get("detail", "")
    assert "Game not started" in detail


def test_allin_without_start_game_returns_400():
    resp = client.post("/hand/action/allin", json={"action": "allin"})
    assert resp.status_code == 400
    detail = resp.json().get("detail", "")
    assert "Game not started" in detail

def test_invalid_route_returns_404():
    resp = client.get("/hand/this-does-not-exist")
    assert resp.status_code == 404
