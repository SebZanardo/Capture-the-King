import asyncio  # For running the game in browser
import chess
from stockfish import Stockfish
from config.core import Core


"""
Most external libraries don't work with web compilation natively when using pygbag.
Having a web build was priority for us since it this project is for a game jam.
Therefore, we decided it was best to program our own chess engine as it gave us
more freedom with board shapes and unique piece types and allowed us to compile for web.
"""

def main():
    app = Core()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
