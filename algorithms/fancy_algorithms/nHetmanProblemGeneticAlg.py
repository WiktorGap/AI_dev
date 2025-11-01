import sys
import random
from heapq import heappop, heappush
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QGridLayout, QSpinBox
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problem N-Hetmanów - Algorytm Genetyczny")
        self.setGeometry(100, 100, 600, 500)
        self.UiComponents()

    def generateSolution(self):
        n = self.setRangeSpinBtn.value()
        if n <= 3:
            self.populLabel.setText("Zakres N musi być większy od 3!")
            return None
         
        oneSolution = random.sample(range(n), n) 
  
        return oneSolution
    
    def generatePopulation(self):
        size = self.populationBtnSpin.value()
        if size <= 1:
            self.populLabel.setText("Ustaw co najmniej dwa chromosomy!")
            return None
        
        population = []
        for _ in range(size):
            solution = self.generateSolution()
            if solution is None:
                self.populLabel.setText("Błąd przy generowaniu osobnika (N<=3?).")
                return None
            population.append(solution)

        self.populLabel.setText(f"Wygenerowano {size} osobników.")
        return population

    def calculateFitness(self, chromosome):
        n = len(chromosome)
        collisionnCtr = 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(i - j) == abs(chromosome[i] - chromosome[j]):
                    collisionnCtr += 1
        return collisionnCtr 

    def crossover_two_children(self, parent1, parent2, n):
      
        k = n // 2  
        
        child1 = parent1[:k]
        fill_with_1 = [gene for gene in parent2 if gene not in child1]
        child1.extend(fill_with_1)
        

        child2 = parent2[:k]
        fill_with_2 = [gene for gene in parent1 if gene not in child2]
        child2.extend(fill_with_2)
        
        return child1, child2

    def mutate(self, chromosome):

        i, j = random.sample(range(len(chromosome)), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]

        return chromosome


    def runAlg(self):

        
        n = self.setRangeSpinBtn.value()
        if n <= 3:
            self.populLabel.setText("N musi być > 3, aby uruchomić algorytm.")
            return

        limitOfItretion = self.setLimitOfIteration.value()
        populationSize = self.populationBtnSpin.value()
        

        mutation_rate = self.mutationRateSpin.value() / 100.0
        crossover_rate = self.crossoverRateSpin.value() / 100.0
        
     
        elite_size = int(populationSize * 0.1) 
        if elite_size < 1:
             elite_size = 1

        population = self.generatePopulation()
        if population is None:
            self.populLabel.setText("Inicjalizacja populacji się nie powiodła")
            return 
        
        best_fitness_overall = float('inf')

        for generation in range(limitOfItretion):
            populationWithFitness = []
            for chromosome in population:
                fitness = self.calculateFitness(chromosome)
                if fitness == 0:
           
                    self.populLabel.setText(f"Rozwiązanie (N={n}): {chromosome}")
                    self.generationLabel.setText(f"Generacja: {generation + 1}")
                    self.bestFitnessLabel.setText(f"Najlepsze dopasowanie: 0 (Perfekcyjnie!)")
                    print(f"*** Rozwiązanie znalezione w generacji {generation + 1}! ***")
                    print(f"Rozwiązanie: {chromosome}")
                    return 
                heappush(populationWithFitness, (fitness, chromosome))


            sorted_population = [heappop(populationWithFitness)[1] for _ in range(populationSize)]
            
            best_fitness_so_far = self.calculateFitness(sorted_population[0])
            if best_fitness_so_far < best_fitness_overall:
                 best_fitness_overall = best_fitness_so_far
            
          
            self.generationLabel.setText(f"Generacja: {generation + 1} / {limitOfItretion}")
            self.bestFitnessLabel.setText(f"Najlepsze dopasowanie: {best_fitness_so_far} kolizji")
            
       
            QApplication.processEvents() 
            
            new_population = []
            
       
            new_population.extend(sorted_population[:elite_size])
            
       
            while len(new_population) < populationSize:
                
              
                parent1 = random.choice(sorted_population[:populationSize // 2])
                parent2 = random.choice(sorted_population[:populationSize // 2])
                
                child1 = parent1 
                child2 = parent2
                
             
                if random.random() < crossover_rate:
                    child1, child2 = self.crossover_two_children(parent1, parent2, n)
                
           
                if random.random() < mutation_rate:
                   
                    child1_to_mutate = list(child1) 
                    self.mutate(child1_to_mutate)
                    child1 = child1_to_mutate
                
                if random.random() < mutation_rate:
                    child2_to_mutate = list(child2)
                    self.mutate(child2_to_mutate)
                    child2 = child2_to_mutate

                new_population.append(child1)
             
                if len(new_population) < populationSize:
                    new_population.append(child2)
            
           
            population = new_population

    
        self.populLabel.setText(f"Nie znaleziono idealnego rozwiązania po {limitOfItretion} generacjach.")
        self.bestFitnessLabel.setText(f"Najlepszy wynik: {best_fitness_overall} kolizji. Najlepszy osobnik: {sorted_population[0]}")
        print(f"Nie znaleziono rozwiązania. Najlepszy osobnik: {sorted_population[0]} z {best_fitness_so_far} kolizjami.")


    def UiComponents(self):
        main_widget = QWidget()
        main_layout = QGridLayout(main_widget)

        confAlgGroup = QGroupBox("Konfiguruj algorytm genetyczny")
        confLayot = QVBoxLayout(confAlgGroup)
        
   
        self.labelInfo = QLabel("Rozmiar planszy (N):")
        self.setRangeSpinBtn = QSpinBox()
        self.setRangeSpinBtn.setValue(8)
        self.setRangeSpinBtn.setMinimum(4) 
        self.setRangeSpinBtn.setMaximum(100)
        
        confLayot.addWidget(self.labelInfo)
        confLayot.addWidget(self.setRangeSpinBtn)
        
     
        self.populationLabelInfo = QLabel("Rozmiar populacji:") 
        self.populationBtnSpin = QSpinBox()
        self.populationBtnSpin.setValue(100)
        self.populationBtnSpin.setMaximum(10000) 
        self.populationBtnSpin.setMinimum(10) 
        
        confLayot.addWidget(self.populationLabelInfo)
        confLayot.addWidget(self.populationBtnSpin)


        self.labelIteration = QLabel("Limit iteracji (generacji):")
        self.setLimitOfIteration = QSpinBox()
        self.setLimitOfIteration.setValue(1000) 
        self.setLimitOfIteration.setMaximum(100000)
        self.setLimitOfIteration.setMinimum(10)
        
        confLayot.addWidget(self.labelIteration)
        confLayot.addWidget(self.setLimitOfIteration)


        self.crossoverLabel = QLabel("Współczynnik krzyżowania (%):")
        self.crossoverRateSpin = QSpinBox()
        self.crossoverRateSpin.setValue(80)
        self.crossoverRateSpin.setMaximum(100)
        confLayot.addWidget(self.crossoverLabel)
        confLayot.addWidget(self.crossoverRateSpin)

        self.mutationLabel = QLabel("Współczynnik mutacji (%):")
        self.mutationRateSpin = QSpinBox()
        self.mutationRateSpin.setValue(5)
        self.mutationRateSpin.setMaximum(100)
        confLayot.addWidget(self.mutationLabel)
        confLayot.addWidget(self.mutationRateSpin)

 
        resultsGroup = QGroupBox("Uruchomienie i wyniki")
        resultsLayout = QVBoxLayout(resultsGroup)

        self.runBtn = QPushButton("Uruchom algorytm")
        self.runBtn.clicked.connect(self.runAlg)
        self.runBtn.setStyleSheet("font-size: 16px; padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px;")
        resultsLayout.addWidget(self.runBtn)

        self.generationLabel = QLabel("Generacja: -")
        self.generationLabel.setStyleSheet("font-size: 14px; margin-top: 10px;")
        resultsLayout.addWidget(self.generationLabel)

        self.bestFitnessLabel = QLabel("Najlepsze dopasowanie: -")
        self.bestFitnessLabel.setStyleSheet("font-size: 14px;")
        resultsLayout.addWidget(self.bestFitnessLabel)

    
        self.populLabel = QLabel(" Ustaw parametry i uruchom algorytm.")
        self.populLabel.setStyleSheet("font-size: 14px; margin-top: 10px; font-weight: bold;")
        self.populLabel.setWordWrap(True)
        resultsLayout.addWidget(self.populLabel)
        
        resultsLayout.addStretch() 

  
        main_layout.addWidget(confAlgGroup, 0, 0)
        main_layout.addWidget(resultsGroup, 0, 1)
        main_layout.setColumnStretch(1, 1) 

        self.setCentralWidget(main_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
