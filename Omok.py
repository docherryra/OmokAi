import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import inf as infinity
import datetime
import copy
from os import system
#기본적인 UI구성요소를 제공하는 클레스들은 PyQt5.QtWidgets모듈에 포함되어 있음
#https://codetorial.net/entry/reimplement2
#https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py
#https://oceancoding.blogspot.com/2019/03/blog-post.html
#https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
width = 900 #화면 size
height = 670
board_l = 640 #board size
BLACK = +1 #흑돌 ,백돌
WHITE = 0
HIGH = 3  #level
MID = 2
LOW = 1
ALPHABETA = 1
#evaluation function - state, score // 오목 7개의 상태와 8번째에 score입력
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = [[-1 for x in range(15)] for y in range(15)] #바둑 있는 곳들 표시하는 15 * 15 배열
        # Level box에서 선택한 level - 탐색 depth를 나타냄
        self.level = LOW
        # 3 by 3  rule
        self.rule = 1
        # first player를 표시 - 선수는 무조건 흑돌
        self.human = BLACK
        self.computer = WHITE
        # algorithm 표시
        self.algorithm = ALPHABETA
        self.counter = 1

        self.initUI()

    #UI 초기 설정
    def initUI(self):
        self.setWindowTitle('OMOK')
        self.setWindowIcon(QIcon('board.png'))
        self.resize(width, height)  # 스크린의 크기 조정
        self.center()  # 화면 정중앙에 프로그램 배치
        #수평 layout - 2개의 수직 layout을 뒷부분에서 추가할 것
        formbox = QHBoxLayout()
        self.setLayout(formbox)
        #수직 layout
        left = QVBoxLayout()    #오목판
        right = QVBoxLayout()   #설정 - option , start button, exit button

        # 좌 레이아웃 박스에 그래픽 뷰 추가 - 오목판
        self.graphicsView = QGraphicsView(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setFixedSize(board_l, board_l)
        self.init_board()
        self.graphicsView.setHorizontalScrollBarPolicy((Qt.ScrollBarAlwaysOff))
        self.graphicsView.setVerticalScrollBarPolicy((Qt.ScrollBarAlwaysOff))
        left.addWidget(self.graphicsView)

        #우 레이아웃 박스에 widget 추가
        #new game button
        newGame_B = QPushButton('new game', self)
        right.addWidget(newGame_B)
        newGame_B.resize(newGame_B.sizeHint())
        newGame_B.clicked.connect(self.init_board) #init_board()함수로 연결돼 보드를 초기화 한다.
        # 그룹박스에 사용할 위젯

        # quit button
        quit_B = QPushButton('Exit', self)
        right.addWidget(quit_B)
        quit_B.resize(quit_B.sizeHint())
        quit_B.clicked.connect(QCoreApplication.instance().quit) #프로그램을 종료

        #전체 폼박스에 좌우 박스 배치
        formbox.addLayout(left)
        formbox.addLayout(right)
        formbox.setStretchFactor(left, 1)
        formbox.setStretchFactor(right, 0)

#        self.setMouseTracking(True)

        self.show()

    # 창을 화면의 중심으로 설정
    def center(self):
        qr = self.frameGeometry()  # 창의 위치와 크기 정보 가져옴
        cp = QDesktopWidget().availableGeometry().center()  # 모니터 화면의 가운데 위치 파악
        qr.moveCenter(cp)  # 창의 위치를 화면의 중심의 위치로 이동
        self.move(qr.topLeft())  # 창을 qr위치로 이동

    # 오목판 초기화 및 관련 설정 초기화
    def init_board(self):
        self.grid = [[-1 for x in range(15)] for y in range(15)] #바둑 위치 표시하는 배열을 -1로 reset
        # minimax에서 탐색할 boundary로 사용 - b_x1, b_y1, b_x2, b_y2
        self.b_x1 = infinity
        self.b_y1 = infinity
        self.b_x2 = -infinity
        self.b_y2 = -infinity
        #오목판 UI 만들기 - 틀, 15 * 15 선
        #board 틀
        brush = QBrush(QColor(204, 153, 0))
        pen = QPen(QColor(204, 153, 0))
        rect = QRectF(-320, -320, board_l, board_l)
        self.scene.addRect(rect, pen, brush)
        pen = QPen(Qt.black)
        rect = QRectF(-280, -280, board_l-80, board_l-80)
        self.scene.addRect(rect, pen, brush)
        #board 내부 선 15 * 15
        for i in range(1, 14):
            line = QLineF(-280+i*40, -280, -280+i*40, 280)
            self.scene.addLine(line, pen)
            line = QLineF(-280, -280+i*40, 280, -280+i*40)
            self.scene.addLine(line, pen)


    #옵션의 combo box들에 대한 정보 처리
    #param : combo box의 click된 text


    #화면상 x,y 좌표를 grid위 i, j로 바꾸기
    #return : grid위 (i, j)
    def xyTogrid(self, x, y):
        x_q, x_r = divmod(x, 40) #칸 사이 간격이 40이므로
        y_q, y_r = divmod(y, 40)
        if x_r >= 20:
            x_q += 1
        if y_r >= 20:
            y_q += 1

        return x_q, y_q

    # 바둑돌 배치
    # param : grid위 (i, j), 돌의 색상(0이면 흰색, 1이면 검은색)
    def draw_baduk(self, x_q, y_q, baduk):
        y = -280 + (y_q) * 40
        x = -280 + (x_q) * 40

        if baduk % 2 == 0:  # 0이면 흰색돌
            self.grid[x_q][y_q] = 0  # 흰색 바둑돌 set - grid에 표시
            pen = QtGui.QPen(QtCore.Qt.white)
            brush = QtGui.QBrush(QtCore.Qt.white)
            rect = QRectF(QPointF(x-18, y-18), QSizeF(36, 36))
            self.scene.addEllipse(rect, pen, brush)
            if self.wins(self.grid, 0):
                sys.exit(app.exec_())
        elif baduk % 2 == 1:
            self.grid[x_q][y_q] = 1  # 검은색 바둑돌 set - grid에 표시
            pen = QtGui.QPen(QtCore.Qt.black)
            brush = QtGui.QBrush(QtCore.Qt.black)
            rect = QRectF(QPointF(x - 18, y - 18), QSizeF(36, 36))
            self.scene.addEllipse(rect, pen, brush)
            if self.wins(self.grid, 1):
                sys.exit(app.exec_())
        self.counter += 1

    def mousePressEvent(self, e):
        x = e.x() - 55
        y = e.y() - 55
        # 보드내 위치할 경우
        if x >= 0 and x <= 560 and y >= 0 and y <= 560:
            x, y = self.xyTogrid(x, y)  # grid위 (i, j)로 가져오기
            if (self.grid[x][y] != -1):  # 해당 grid[i][j]가 이미 오목 놓여진 경우 인식 안됨
                return
            self.draw_baduk(x, y, self.counter)

    def wins(self, state, player):
        for i in range(0,15): #x
            for j in range(0, 15): #y
                flag = True #5줄이 모두 같을 경우 유지됨 아닐경우 false
                # row
                for k in range(0, 5):
                    if j+4 > 14 or state[i][j+k] != player:
                        flag = False
                        break
                if flag == True:
                    return True #5줄 찾은 경우 true 반환
                flag = True  # 5줄이 모두 같을 경우 유지됨 아닐경우 false
                # column
                for k in range(0, 5):
                    if i+4 > 14 or state[i+k][j] != player:
                        flag = False
                        break
                if flag == True:
                    return True  # 5줄 찾은 경우 true 반환
                # right_diagonals
                flag = True  # 5줄이 모두 같을 경우 유지됨 아닐경우 false
                for k in range(0, 5):
                    if i+4 > 14 or j+4 > 14 or state[i+k][j + k] != player:
                        flag = False
                        break
                if flag == True:
                    return True  # 5줄 찾은 경우 true 반환
                # left_diagonals
                flag = True  # 5줄이 모두 같을 경우 유지됨 아닐경우 false
                for k in range(0, 5):
                    if i-4 < 0 or j+4 > 14 or state[i-k][j + k] != player:
                        flag = False
                        break
                if flag == True:
                    return True  # 5줄 찾은 경우 true 반환
        return False #모든 행을 다 찾았지만 없을 경우 false 반환


if __name__ == '__main__':  # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv)  # 모든 pyqt5 어플리케이션은 application 객체를 생성
    ex = MyApp()
    sys.exit(app.exec_())