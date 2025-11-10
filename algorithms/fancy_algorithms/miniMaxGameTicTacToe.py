import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QPushButton, QGroupBox, QGridLayout, QSpinBox, QComboBox
)
from PySide6.QtCore import Qt 
from PySide6.QtGui import QFont




class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Kółko i Krzyżyk - Minimax")
        self.setGeometry(100, 100, 400, 700) 
        self.UiComponents()
        self.show()

    def getChoose(self, index):
        print(f"Wybrano gracza o indeksie: {index}")
        return index

    def UiComponents(self):
        
        mainWidget = QWidget()
        
        self.mainLayout = QGridLayout(mainWidget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop) 

        controlPanelGroup = QGroupBox("Wybierz parametry algorytmu")
        controlLayout = QVBoxLayout(controlPanelGroup)

        self.chooseBoardLbl = QLabel("Wybierz rozmiar tablicy n x n")
        self.setGeometryOfBoard = QSpinBox()
        self.setGeometryOfBoard.setValue(3)
        self.setGeometryOfBoard.setMinimum(3)
        self.setGeometryOfBoard.setMaximum(6)
        
        self.chooseAgent = QLabel("Wybierz pierwszego gracza")
        self.chooseOfAgentBtn = QComboBox()
        self.chooseOfAgentBtn.addItems(["Gracz (X)", "Agent (O)"])
        self.chooseOfAgentBtn.currentIndexChanged.connect(self.getChoose)

        self.chooseDepthLbl = QLabel("Ustaw głębokość")
        self.setDepth = QSpinBox()
        self.setDepth.setValue(3) 
        self.setDepth.setMinimum(1) 
        self.setDepth.setMaximum(10) 
                  
        self.startBtn = QPushButton("Zacznij grę")
        self.startBtn.clicked.connect(self.runGame)
        
        controlLayout.addWidget(self.chooseBoardLbl)
        controlLayout.addWidget(self.setGeometryOfBoard)
        controlLayout.addWidget(self.chooseAgent)
        controlLayout.addWidget(self.chooseOfAgentBtn)
        controlLayout.addWidget(self.chooseDepthLbl)
        controlLayout.addWidget(self.setDepth)
        controlLayout.addWidget(self.startBtn) 
        
        self.mainLayout.addWidget(controlPanelGroup, 0, 0) 
        
        self.setCentralWidget(mainWidget)
        self.mainLayout.setRowStretch(4, 1)

    def runGame(self):
       
        self.PLAYER_SYMBOL = "X"
        self.AGENT_SYMBOL = "O" 

        self.n = self.setGeometryOfBoard.value()
        self.max_depth = self.setDepth.value()
        
     
        self.board_state = [[' ' for _ in range(self.n)] for _ in range(self.n)]
        
       
        if hasattr(self, 'gameBoardGroup'):
            self.gameBoardGroup.deleteLater()
        if hasattr(self, 'label'):
            self.label.deleteLater()
        if hasattr(self, 'reset_game_button'):
            self.reset_game_button.deleteLater()
    
        
        self.turn = 0 # 0 = Gracz (X), 1 = Agent (O)
        self.times = 0 # Licznik ruchów

        self.push_list = []
        
        self.gameBoardGroup = QGroupBox("Plansza Gry")
        gameLayout = QGridLayout(self.gameBoardGroup)
        gameLayout.setSpacing(5)

        for i in range(self.n):
            temp = []
            for j in range(self.n):
                button = QPushButton(self)
                button.setFixedSize(50, 50) 
                button.setFont(QFont('Times', 17))
                button.clicked.connect(self.action_called)
                
                gameLayout.addWidget(button, i, j) 
                temp.append(button)
            self.push_list.append(temp)
        
        self.mainLayout.addWidget(self.gameBoardGroup, 1, 0) 

        self.label = QLabel(self)
        self.label.setMinimumHeight(60) 
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid black;"
                                 #"background : white;"
                                 "}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Times', 15))
       
        self.mainLayout.addWidget(self.label, 2, 0) 

        self.reset_game_button = QPushButton("Reset-Game", self)
        self.reset_game_button.setMinimumHeight(50) 
        self.reset_game_button.clicked.connect(self.runGame)
    
        self.mainLayout.addWidget(self.reset_game_button, 3, 0) 

        # Sprawdzenie kto zaczyna
        if self.chooseOfAgentBtn.currentIndex() == 1: # Indeks 1 to "Agent (O)"
            self.agent_starts = True
            self.turn = 1 # Ustaw turę na Agenta (O)
            self.label.setText("Agent (O) zaczyna...")
            QApplication.processEvents()
            self.agent_move() # Wywołanie pierwszego ruchu agenta
        else:
            self.agent_starts = False
            self.turn = 0 # Ustaw turę na Gracza (X)
            self.label.setText("Gracz (X) zaczyna")

   

    def action_called(self):
        
        if self.turn != 0: 
            return

        button = self.sender()
        found_button = False

        clicked_i, clicked_j = -1, -1
        for i in range(self.n):
            for j in range(self.n):
                if button == self.push_list[i][j]:
                    clicked_i, clicked_j = i, j
                    found_button = True
                    break
            if found_button:
                break
        
        if not found_button:
            print("Błąd: Nie znaleziono klikniętego przycisku")
            return 
    
   
        if self.board_state[clicked_i][clicked_j] == ' ':
            
            self.board_state[clicked_i][clicked_j] = self.PLAYER_SYMBOL
            button.setText(self.PLAYER_SYMBOL)
            button.setEnabled(False)
            self.times += 1
            
            if self.check_game_over(): 
                return 

            # Przekaż turę agentowi
            self.turn = 1
            self.label.setText("Agent (O) myśli...")
            QApplication.processEvents() 
            
            self.agent_move() 
    
    def check_game_over(self):
        
 
        winner = self.check_winner(self.board_state) 
   
        
        text = ""
        is_over = False

        if winner: 
            if winner == self.PLAYER_SYMBOL:
                text = "Gracz (X) Wygrywa!"
            else:
                text = "Agent (O) Wygrywa!"
            is_over = True
        
        elif self.check_draw(self.board_state):
            text = "Remis!"
            is_over = True

        if is_over:
            self.label.setText(text)
            # Wyłącz wszystkie przyciski
            for row in self.push_list:
                for btn in row:
                    btn.setEnabled(False)
            return True
            
        return False



    def check_winner(self, board):
        """Sprawdza, czy na podanej planszy 'board' jest zwycięzca."""
    
        # Sprawdzanie RZĘDÓW
        for r in range(self.n):
            symbol = board[r][0]
            if symbol == ' ':
                continue
            if all(board[r][j] == symbol for j in range(1, self.n)):
                return symbol 

        # Sprawdzanie KOLUMN
        for c in range(self.n):
            symbol = board[0][c]
            if symbol == ' ':
                continue
            if all(board[i][c] == symbol for i in range(1, self.n)):
                return symbol 

        # Sprawdzanie GŁÓWNEJ PRZEKĄTNEJ ( \ )
        symbol = board[0][0]
        if symbol != ' ':
            if all(board[i][i] == symbol for i in range(1, self.n)):
                return symbol 

        # Sprawdzanie ANTY-PRZEKĄTNEJ ( / )
        symbol = board[0][self.n - 1]
        if symbol != ' ':
            if all(board[i][self.n - 1 - i] == symbol for i in range(1, self.n)):
                return symbol 
        
        return None

    def check_draw(self, board):
        """Sprawdza, czy na podanej planszy 'board' jest remis."""
        # Remis jest tylko wtedy, gdy NIE MA zwycięzcy I nie ma pustych pól
        if self.check_winner(board) is None:
            for r in range(self.n):
                for c in range(self.n):
                    if board[r][c] == ' ':
                        return False # Znaleziono puste pole, to nie remis
            return True # Nie ma pustych pól i nie ma zwycięzcy
        return False
    
    def get_empty_cells(self, board):
        """Zwraca listę tupli (r, c) wszystkich pustych pól."""
        empty_cells = []
        for i in range(self.n):
            for j in range(self.n):
                if board[i][j] == ' ':
                    empty_cells.append((i, j))
        return empty_cells



    def agent_move(self):
   
        empty_cells = self.get_empty_cells(self.board_state)
        if not empty_cells:
            return
        
      
        move = self.find_best_move()
        
        if move is None:
            
            print("Błąd: find_best_move nie zwrócił ruchu. Wybieranie losowego.")
            move = empty_cells[0]
            
        (row, col) = move
        
        # Wykonaj ruch na planszy 
        self.board_state[row][col] = self.AGENT_SYMBOL
        self.push_list[row][col].setText(self.AGENT_SYMBOL)
        self.push_list[row][col].setEnabled(False)
        self.times += 1

       
        if self.check_game_over():
            return

        
        self.turn = 0
        self.label.setText("Tura Gracza (X)")
        

    def find_best_move(self):
      
        best_score = -math.inf  # Agent chce MAKSYMALIZOWAĆ wynik
        best_move = None
        
        initial_depth_limit = self.max_depth 

        for (r, c) in self.get_empty_cells(self.board_state):
            
            self.board_state[r][c] = self.AGENT_SYMBOL
            
            move_score = self.minimax(self.board_state, initial_depth_limit - 1, False)
            
            self.board_state[r][c] = ' '
            
            if move_score > best_score:
                best_score = move_score
                best_move = (r, c)
        
        return best_move

    def minimax(self, board, depth, is_maximizing):
   
        
        winner = self.check_winner(board)
        if winner:
            if winner == self.AGENT_SYMBOL:
                return 1000 + depth  # Wygrana agenta jest lepsza im szybciej
            else:
                return -1000 - depth # Przegrana jest gorsza im szybciej
        
        if self.check_draw(board):
            return 0 
        

        if depth == 0:
            return 0 

  
        
        if is_maximizing:
            # Tura Agenta (Maksymalizującego)
            best_score = -math.inf
            
            for (r, c) in self.get_empty_cells(board):
                board[r][c] = self.AGENT_SYMBOL
                score = self.minimax(board, depth - 1, False)
                board[r][c] = ' ' # Cofnij ruch
                best_score = max(best_score, score) 
            return best_score
        
        else: # (is_maximizing == False)
            # Tura Gracza (Minimalizującego)
            best_score = math.inf 
            
            for (r, c) in self.get_empty_cells(board):
                board[r][c] = self.PLAYER_SYMBOL
                score = self.minimax(board, depth - 1, True)
                board[r][c] = ' ' # Cofnij ruch
                best_score = min(best_score, score)
            return best_score


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())