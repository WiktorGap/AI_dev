from heapq import heappop, heappush
import os 
import math
from PySide6.QtWidgets import QApplication , QWidget , QLabel , QMainWindow , QPushButton , QGridLayout , QComboBox, QSpinBox, QVBoxLayout, QGroupBox, QPushButton
from PySide6.QtCore import QSize, Qt , QTimer
import pyqtgraph as pg
import numpy as np
import sys 



pwd = os.path.abspath(os.getcwd())


graph= os.path.join(pwd,"coded1.txt")


def h(point, endPoint):
    x, y = point
    xEnd, yEnd = endPoint
    return math.sqrt((xEnd - x)**2 + (yEnd - y)**2)

def distance(p1, p2):

    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def getPath(parent_map,current,start):
    path = [current]

    while current != start:
         if current not in parent_map:
              return []
         current = parent_map[current]
         path.append(current)
    path.reverse()
    return path



def processGraph(graphPath):

            pointDict = {}

            prassedLines = []
            prassedPoints = []
            with open(graphPath,"r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip("\n")
                    prassedLines.append(line)
            lenOfDoc =len(prassedLines)
            numOfNodes = int(prassedLines[0])


            nodesPosition = prassedLines[1:numOfNodes+1] 

            splittedPoints = []
            for point in nodesPosition:
                splittedPoint= point.split()
                splittedPoints.append(splittedPoint)

            points= []
            for element in splittedPoints:
                element = [int(el) for el in element]
                x,y = element
                point = (x,y)
                points.append(point)

            for i in range(numOfNodes):
                val = points[i]
                pointDict[i+1] = val


            
            relationsPosStart = numOfNodes + 1
            relations = prassedLines[relationsPosStart::]
            

            procRel = []
            relationDict = {}
            listOfRelated = []


  

            finalDict = {}

            for i, relation in enumerate(relations):
                relation = relation.split()
                vals = [int(el) for el in relation[1:]]  
                key = i + 1                               
                point = pointDict[key]
                finalDict[key] = (point, vals)

            


            return finalDict

        
def aStar_generator(startNodeIdx, finalNodeIdx):
    graph_ = processGraph(graph)

    if startNodeIdx not in graph_ or finalNodeIdx not in graph_:
        return [] , []

    visited_nodes_order = []

    g_score = { node : float('inf') for node in graph_.keys()}
    g_score[startNodeIdx] = 0

    cameFrom = {}

    priorityQue = []

    startCords = graph_[startNodeIdx][0]
    finalCords = graph_[finalNodeIdx][0]

    f_score_start = g_score[startNodeIdx] + h(startCords, finalCords)

    heappush(priorityQue, (f_score_start, startNodeIdx))

    while priorityQue:
        currentFScore , currentNode = heappop(priorityQue)

        if currentNode not in visited_nodes_order:
             visited_nodes_order.append(currentNode)

        yield visited_nodes_order , cameFrom , currentNode

        
        if currentNode == finalNodeIdx:
            return 
        
      
        for neighbourIdx in graph_[currentNode][1]: 
            
            currentCords = graph_[currentNode][0]
            neighbourCords = graph_[neighbourIdx][0] 

            costToNeighbour = distance(currentCords, neighbourCords)

            tempCost = g_score[currentNode] + costToNeighbour


            if tempCost < g_score.get(neighbourIdx, float('inf')): 
                
                cameFrom[neighbourIdx] = currentNode
                
                g_score[neighbourIdx] = tempCost
                
                h_score = h(neighbourCords, finalCords)
                f_score = tempCost + h_score
                
                heappush(priorityQue, (f_score, neighbourIdx))
                
    yield visited_nodes_order , cameFrom , currentNode
                 


def bfsForceGen(startNodeIdx, finalNodeIdx):
    graph_ = processGraph(graph)

    if startNodeIdx not in graph_ or finalNodeIdx not in graph_:
        return [] , []

    visited_nodes_order = []

    h_scores = { node : float('inf') for node in graph_.keys()}


    cameFrom = {}

    priorityQue = []

    startCords = graph_[startNodeIdx][0]
    finalCords = graph_[finalNodeIdx][0]

    start_h  = h(startCords,finalCords)
    h_scores[startNodeIdx] = start_h

    heappush(priorityQue, (start_h, startNodeIdx))

    while priorityQue:
        currentHScore , currentNode = heappop(priorityQue)

        if currentNode not in visited_nodes_order:
             visited_nodes_order.append(currentNode)

        yield visited_nodes_order , cameFrom , currentNode

        
        if currentNode == finalNodeIdx:
            return 
        
      
        for neighbourIdx in graph_[currentNode][1]: 

            if neighbourIdx in visited_nodes_order:
                continue
            
            neighbourCords = graph_[neighbourIdx][0] 

                
            new_h_score = h(neighbourCords,finalCords)

            if new_h_score < h_scores.get(neighbourIdx, float('inf')):
                cameFrom[neighbourIdx] = currentNode
                h_scores[neighbourIdx] = new_h_score
            
            
                heappush(priorityQue, (new_h_score, neighbourIdx))
                
    yield visited_nodes_order , cameFrom , currentNode


class Window(QMainWindow):
    def __init__(self): 
        super().__init__()
        
        
        self.graph_data = processGraph(graph)
        self.nodes = sorted(list(self.graph_data.keys()))
        self.max_node_index = self.nodes[-1] if self.nodes else 1
        
      
        self.current_generator = None
        self.is_running = False
        self.cameFrom = {} 
        self.current_node = None 
        self.visited_nodes = []

        self.start_node = self.nodes[0] if self.nodes else 1
        self.final_node = self.nodes[-1] if self.nodes else 1
        
       
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)

        
        self.setWindowTitle("Wizualizacja Algorytmów Grafowych (A* / BFS(force))")
        self.setGeometry(100, 100, 1200, 800)
        self.UiComponents()
        
   
    def start_search(self):
        try:
            
            start_node = self.start_spinbox.value()
            final_node = self.final_spinbox.value()
            alg_choice = self.alg_combo.currentText()
            
            
            if start_node not in self.graph_data or final_node not in self.graph_data:
                print(f"Błąd: Węzeł startowy ({start_node}) lub końcowy ({final_node}) nie istnieje w grafie.")
                return

        
            self.start_node = start_node
            self.final_node = final_node
            self.visited_nodes = []
            self.cameFrom = {}
            self.is_running = True
            self.timer.stop() 

            if alg_choice.startswith("A*"):
                self.aStar_step = aStar_generator(start_node, final_node)
            else: 
                self.aStar_step = bfsForceGen(start_node, final_node)
                
           
            self.visited_plot.setData([], [])
            self.path_plot.setData([], [])
            self.update_goal_markers() 
            
           
            self.timer.start(int(self.speed_spinbox.value()))

        except Exception as e:
            print(f"Błąd podczas uruchamiania algorytmu: {e}")
            self.is_running = False


  
    def update_goal_markers(self):
       
        
        start_coord = self.graph_data[self.start_node][0]
        final_coord = self.graph_data[self.final_node][0]
        
        self.start_marker.setData([start_coord[0]], [start_coord[1]])
        self.final_marker.setData([final_coord[0]], [final_coord[1]])
        
        
    def UiComponents(self):
        widget = QWidget()
        main_layout = QGridLayout(widget)
        
    
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        
        alg_group = QGroupBox("Wybór Algorytmu")
        alg_layout = QVBoxLayout(alg_group)
        self.alg_combo = QComboBox()
        self.alg_combo.addItem("A* (A-Gwiazdka)")
        self.alg_combo.addItem("BFS (Zachłanne Przeszukiwanie)")
        alg_layout.addWidget(self.alg_combo)
        control_layout.addWidget(alg_group)
        
       
        nodes_group = QGroupBox(f"Wybór Węzłów (1 do {self.max_node_index})")
        nodes_layout = QGridLayout(nodes_group)
        
        nodes_layout.addWidget(QLabel("Start:"), 0, 0)
        self.start_spinbox = QSpinBox()
        self.start_spinbox.setRange(1, self.max_node_index)
        self.start_spinbox.setValue(self.start_node)
        nodes_layout.addWidget(self.start_spinbox, 0, 1)

        nodes_layout.addWidget(QLabel("Koniec:"), 1, 0)
        self.final_spinbox = QSpinBox()
        self.final_spinbox.setRange(1, self.max_node_index)
        self.final_spinbox.setValue(self.final_node)
        nodes_layout.addWidget(self.final_spinbox, 1, 1)
        
        control_layout.addWidget(nodes_group)
        
      
        speed_group = QGroupBox("Szybkość Animacji (ms)")
        speed_layout = QVBoxLayout(speed_group)
        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setRange(50, 2000)
        self.speed_spinbox.setValue(200) 
        speed_layout.addWidget(self.speed_spinbox)
        control_layout.addWidget(speed_group)
        
        self.start_button = QPushButton("START WYSZUKIWANIA")
        self.start_button.setStyleSheet("background-color: lightgreen;")
        self.start_button.clicked.connect(self.start_search)
        control_layout.addWidget(self.start_button)
        
        control_layout.addStretch(1) 
        
        main_layout.addWidget(control_panel, 0, 0, 1, 1, Qt.AlignTop) 
        
      
        self.plt = pg.plot()
        self.plt.showGrid(x=True, y=True)
        self.plt.addLegend()
        self.plt.setLabel('left', 'Y Coords')
        self.plt.setLabel('bottom', 'X Coords')
        
        nodes = list(self.graph_data.keys())
        cords = [self.graph_data[node][0] for node in nodes]
        relations = [self.graph_data[node][1] for node in nodes]
        
        
        line_x_coords, line_y_coords = [], []
        for i, nodeIdx in enumerate(nodes):
            startPoint = cords[i]
            for neighbourIdxOne in relations[i]:
                if nodeIdx < neighbourIdxOne and neighbourIdxOne <= len(cords): 
                    end_point = cords[neighbourIdxOne - 1]
                    line_x_coords.extend([startPoint[0], end_point[0], np.nan])
                    line_y_coords.extend([startPoint[1], end_point[1], np.nan])

        self.plt.plot(line_x_coords, line_y_coords, pen='g', connect='finite', name='Edges')
        
       
        x_all = [c[0] for c in cords]
        y_all = [c[1] for c in cords]
        self.plt.plot(x_all, y_all, pen=None, symbol='o', symbolPen='g', 
                      symbolBrush='g', symbolSize=10, name='Nodes')
        
        self.visited_plot = self.plt.plot([], [], pen=None, symbol='o', symbolPen='y', 
                                         symbolBrush=(255, 255, 0, 150), symbolSize=14, name='Visited')
        self.path_plot = self.plt.plot([], [], pen={'color': 'b', 'width': 3}, name='Path')
        
 
        self.start_marker = self.plt.plot([], [], pen=None, symbol='s', symbolBrush='lime', symbolSize=16, name='Start')
        self.final_marker = self.plt.plot([], [], pen=None, symbol='t', symbolBrush='r', symbolSize=16, name='Goal')
        
        main_layout.addWidget(self.plt, 0, 1) 
        self.setCentralWidget(widget)
        
        self.update_goal_markers()
        
    def update_plot(self):
        if not self.is_running:
            return

        try:
          
            self.visited_nodes, self.cameFrom, self.current_node = next(self.aStar_step)
            
            
            visited_coords = [self.graph_data[idx][0] for idx in self.visited_nodes]
            visited_x = [c[0] for c in visited_coords]
            visited_y = [c[1] for c in visited_coords]
            self.visited_plot.setData(visited_x, visited_y)

           
            if self.current_node:
                path_to_current = getPath(self.cameFrom, self.current_node, self.start_node)
                path_coords = [self.graph_data[idx][0] for idx in path_to_current]
                path_x = [c[0] for c in path_coords]
                path_y = [c[1] for c in path_coords]
                self.path_plot.setData(path_x, path_y)
            
           
            QApplication.processEvents()

        except StopIteration:
            self.timer.stop()
            self.is_running = False
            
       
            final_path_indices = getPath(self.cameFrom, self.final_node, self.start_node)
            if final_path_indices:
                final_path_coords = [self.graph_data[idx][0] for idx in final_path_indices]
                final_path_x = [c[0] for c in final_path_coords]
                final_path_y = [c[1] for c in final_path_coords]
                self.path_plot.setData(final_path_x, final_path_y) 
            
            print(f"Algorytm zakończony. Ścieżka (indeksy): {final_path_indices}")







if __name__ == '__main__':

    graph_check = processGraph(graph)
    if not graph_check:
        print(f"BŁĄD: Plik grafu '{graph}' jest pusty lub niepoprawny.")
        sys.exit(1)
    print(f"DIAGNOSTYKA: Wczytano {len(graph_check)} węzłów. Uruchamiam GUI...")

    
    App = QApplication(sys.argv)
    window = Window()
    window.show() 
    sys.exit(App.exec())