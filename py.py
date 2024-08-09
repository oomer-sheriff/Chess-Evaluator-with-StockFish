import sys
import os
import chess
import chess.engine
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QPainter, QColor, QPixmap, QPen, QFont
from PyQt6.QtCore import Qt, QRect, QSize

class ChessBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.board = chess.Board()
        self.selected_square = None
        self.setFixedSize(400, 400)
        self.piece_pixmaps = {}
        self.load_pieces()

    def load_pieces(self):
        piece_names = ['p', 'n', 'b', 'r', 'q', 'k']
        colors = ['w', 'b']
        for color in colors:
            for piece in piece_names:
                key = color + piece
                self.piece_pixmaps[key] = QPixmap(f"chess_pieces/{key}.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    def paintEvent(self, event):
        painter = QPainter(self)
        square_size = self.width() // 8

        for row in range(8):
            for col in range(8):
                x = col * square_size
                y = row * square_size
                if (row + col) % 2 == 0:
                    painter.fillRect(x, y, square_size, square_size, QColor(240, 217, 181))
                else:
                    painter.fillRect(x, y, square_size, square_size, QColor(181, 136, 99))

                piece = self.board.piece_at(chess.square(col, 7-row))
                if piece:
                    piece_color = 'w' if piece.color == chess.WHITE else 'b'
                    piece_type = piece.symbol().lower()
                    pixmap = self.piece_pixmaps[piece_color + piece_type]
                    painter.drawPixmap(x, y, pixmap)

        if self.selected_square is not None:
            col, row = self.selected_square % 8, 7 - (self.selected_square // 8)
            painter.setPen(QPen(QColor(255, 0, 0), 3))
            painter.drawRect(col * square_size, row * square_size, square_size, square_size)

    def mousePressEvent(self, event):
        square_size = self.width() // 8
        col = int(event.position().x() // square_size)
        row = 7 - int(event.position().y() // square_size)
        square = chess.square(col, row)

        if self.selected_square is None:
            self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.update()
                self.parent().evaluate_position()
            else:
                self.selected_square = square
        self.update()

class EvaluationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 400)
        self.score = 0

    def set_score(self, score):
        self.score = max(min(score, 1000), -1000) / 20  # Clamp between -1000 and 1000 centipawns
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), Qt.GlobalColor.white)
        
        mid_point = self.height() // 2
        bar_height = int(self.score * mid_point / 50)
        
        if bar_height >= 0:
            painter.fillRect(0, mid_point - bar_height, self.width(), bar_height, Qt.GlobalColor.black)
        else:
            painter.fillRect(0, mid_point, self.width(), -bar_height, Qt.GlobalColor.black)

class ChessGame(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\\stockfish-windows-x86-64-avx2.exe")

    def init_ui(self):
        self.setWindowTitle('Chess Game with Evaluation')
        self.setGeometry(100, 100, 500, 450)

        layout = QHBoxLayout()

        self.chess_board = ChessBoard(self)
        layout.addWidget(self.chess_board)

        self.eval_bar = EvaluationBar(self)
        layout.addWidget(self.eval_bar)

        button_layout = QVBoxLayout()
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_game)
        button_layout.addWidget(self.reset_button)

        self.eval_label = QLabel('Evaluation: 0.00')
        button_layout.addWidget(self.eval_label)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def evaluate_position(self):
        info = self.engine.analyse(self.chess_board.board, chess.engine.Limit(time=0.1))
        score = info['score'].relative.score()
        if score is not None:
            self.eval_bar.set_score(score)
            self.eval_label.setText(f'Evaluation: {score/100:.2f}')
        else:
            mate = info['score'].relative.mate()
            self.eval_label.setText(f'Mate in {abs(mate)}')
            self.eval_bar.set_score(1000 if mate > 0 else -1000)

    def reset_game(self):
        self.chess_board.board.reset()
        self.chess_board.selected_square = None
        self.chess_board.update()
        self.eval_bar.set_score(0)
        self.eval_label.setText('Evaluation: 0.00')

    def closeEvent(self, event):
        self.engine.quit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = ChessGame()
    game.show()
    sys.exit(app.exec())