from typing import List, Optional
from uuid import UUID
import psycopg2
from psycopg2.extras import RealDictCursor
from src.db.dataclass import PokerHand

class PokerHandRepository:
    def __init__(self, conn):
        self.conn = conn
        self.ensure_table_exists()  # Automatically create table if it doesn't exist

    def ensure_table_exists(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS poker_hands (
                    hand_id UUID PRIMARY KEY,
                    winnings INTEGER[],
                    stack_size INTEGER NOT NULL,
                    dealer INTEGER NOT NULL,
                    actions TEXT[],
                    player_hands TEXT[],
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()

    def save(self, hand: PokerHand) -> PokerHand:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO poker_hands (hand_id, winnings, stack_size, dealer, actions, player_hands)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING created_at
                """,
                (
                    str(hand.hand_id),
                    hand.winnings,
                    hand.stack_size,
                    hand.dealer,
                    hand.actions,
                    hand.player_hands
                )
            )
            created_at = cur.fetchone()[0]
            self.conn.commit()
            hand.created_at = created_at
            return hand

    def get_by_id(self, hand_id: UUID) -> Optional[PokerHand]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM poker_hands WHERE hand_id = %s", (str(hand_id),))
            row = cur.fetchone()
            if row:
                return PokerHand(
                    hand_id=UUID(row['hand_id']),
                    winnings=row['winnings'],
                    stack_size=row['stack_size'],
                    dealer=row['dealer'],
                    actions=row['actions'],
                    player_hands=row['player_hands'],
                    created_at=row['created_at']
                )
            return None

    def list_all(self) -> List[PokerHand]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM poker_hands ORDER BY created_at DESC")
            rows = cur.fetchall()
            return [
                PokerHand(
                    hand_id=UUID(row['hand_id']),
                    winnings=row['winnings'],
                    stack_size=row['stack_size'],
                    dealer=row['dealer'],
                    actions=row['actions'],
                    player_hands=row['player_hands'],
                    created_at=row['created_at']
                )
                for row in rows
            ]
