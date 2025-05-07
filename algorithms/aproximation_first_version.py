import random

# f(x) = a0 * x + a1 (aproksymacja liniowa)

# Pobranie liczby węzłów
n = int(input("Podaj liczbę węzłów: "))

# Wybór metody wprowadzania danych
choice = input("Czy chcesz wprowadzić dane ręcznie? (tak/nie): ").strip().lower()

if choice == "tak":
    xTab = [float(input(f"Podaj x[{i}]: ")) for i in range(n)]
    yTab = [float(input(f"Podaj y[{i}]: ")) for i in range(n)]
else:
    xTab = [random.randint(0, 15) for _ in range(n)]
    yTab = [random.randint(0, 15) for _ in range(n)]
    print(f"Wygenerowane wartości x: {xTab}")
    print(f"Wygenerowane wartości y: {yTab}")

# Mnożenie wartości xTab i yTab indeks po indeksie
def mulOfRange(xTab, yTab):
    return [xTab[i] * yTab[i] for i in range(n)]

# Podnoszenie do kwadratu wartości tablicy
def squareOfTab(tab):
    return [val**2 for val in tab]

# Obliczanie współczynników aproksymacji
def approximation(xTab, yTab, n):
    resOfMul = mulOfRange(xTab, yTab)
    sqrTabOfX = squareOfTab(xTab)

    sumX = sum(xTab)
    sumY = sum(yTab)
    sumXY = sum(resOfMul)
    sumX2 = sum(sqrTabOfX)

    a0 = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX ** 2)
    a1 = (sumX2 * sumY - sumXY * sumX) / (n * sumX2 - sumX ** 2)

    return a0, a1

# Obliczanie współczynników
a0, a1 = approximation(xTab, yTab, n)

# Funkcja aproksymująca
def approximating_function(x):
    return a0 * x + a1

# Obliczenie wartości dla konkretnego x
x_value = float(input("Podaj wartość x do obliczenia f(x): "))
fx = approximating_function(x_value)

print(f"Aproksymowana funkcja: f(x) = {a0:.4f} * x + {a1:.4f}")
print(f"Wartość f({x_value}) = {fx:.4f}")
