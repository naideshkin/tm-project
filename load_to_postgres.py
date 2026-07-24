import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw_transfers (
    player_id INTEGER,
    player_name TEXT,
    transfer_date DATE,
    type_raw TEXT,
    team_in TEXT,
    team_out TEXT,
    loaded_at TIMESTAMP DEFAULT now()
);
"""

INSERT_SQL = """
INSERT INTO raw_transfers (player_id, player_name, transfer_date, type_raw, team_in, team_out)
VALUES (:player_id, :player_name, :transfer_date, :type_raw, :team_in, :team_out);
"""


def load(transfers: list[dict]):
    with engine.begin() as conn:
        conn.execute(text(CREATE_TABLE_SQL))
        for row in transfers:
            conn.execute(
                text(INSERT_SQL),
                {
                    "player_id": row["player_id"],
                    "player_name": row["player_name"],
                    "transfer_date": row["transfer_date"],
                    "type_raw": row["type"],
                    "team_in": row["team_in"],
                    "team_out": row["team_out"],
                },
            )
    print(f"Loaded {len(transfers)} rows into raw_transfers")
