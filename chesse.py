import sys
import chess
import chess.engine
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt6.QtGui import QFont

class ChessEvaluator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.engine = chess.engine.SimpleEngine.popen_uci(r"C:\\Users\\oomer\\OneDrive\\Desktop\\chessevaluator\\stockfish\\stockfish-windows-x86-64-avx2.exe")
        self.board = chess.Board()

    def init_ui(self):
        self.setWindowTitle('Chess Game Evaluator')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # FEN input
        self.fen_input = QTextEdit()
        self.fen_input.setPlaceholderText("Enter FEN string here...")
        layout.addWidget(self.fen_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.evaluate_button = QPushButton('Evaluate Position')
        self.evaluate_button.clicked.connect(self.evaluate_position)
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_board)
        button_layout.addWidget(self.evaluate_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        # Evaluation display
        self.eval_label = QLabel('Evaluation: ')
        self.eval_label.setFont(QFont('Arial', 14))
        layout.addWidget(self.eval_label)

        self.setLayout(layout)

    def evaluate_position(self):
        fen = self.fen_input.toPlainText()
        try:
            self.board.set_fen(fen)
        except ValueError:
            self.eval_label.setText('Invalid FEN string')
            return

        info = self.engine.analyse(self.board, chess.engine.Limit(time=2.0))
        score = info['score'].relative.score()
        if score is not None:
            self.eval_label.setText(f'Evaluation: {score/100:.2f}')
        else:
            self.eval_label.setText('Evaluation: Mate in ' + str(info['score'].relative.mate()))

    def reset_board(self):
        self.board.reset()
        self.fen_input.clear()
        self.eval_label.setText('Evaluation: ')

    def closeEvent(self, event):
        self.engine.quit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChessEvaluator()
    ex.show()
    sys.exit(app.exec())