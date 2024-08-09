# Chess Game with Evaluation

A Python application that allows users to play chess and evaluates their moves in real-time using Stockfish. The application features a GUI built with PyQt6 and a 3D chessboard visualization.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features
- Interactive chessboard where users can play against themselves.
- Real-time move evaluation using the Stockfish engine.
- Evaluation bar to display the current position score.
- Move quality indicator to show the quality of the last move.
- Reset button to start a new game.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/chess-game-evaluation.git
    cd chess-game-evaluation
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Download and place the Stockfish engine in the project directory. You can download it from [the official website](https://stockfishchess.org/download/).

## Usage
1. Run the application:
    ```sh
    python main.py
    ```
2. Play the game by clicking on the chessboard squares to move the pieces.
3. Observe the evaluation bar and move quality indicator for feedback on your moves.
4. Click the `Reset` button to start a new game.

## Dependencies
- Python 3.x
- python-chess
- PyQt6
- Stockfish chess engine

To install the dependencies, you can use the following command:
```sh
pip install python-chess PyQt6
