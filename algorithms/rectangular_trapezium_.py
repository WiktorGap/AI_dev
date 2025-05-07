
def insertFunc(a, b, c, x):
    return a * x**2 + b * x + c


def f(x):
    return -x**2 + 6*x + 1

def trapezy():
    pole = 0
    begin = int(input("Wpisz początek przedziału : "))
    end =  int(input("Wpisz koniec przedziału : "))
    n = int(input("Wpisz ilość przedziału (im większa wartość tym dokładniejszy wynik) : "))
    xTab = []
    yTab = []
    dx = (end - begin) / n  # szerokość prostokąta(odległość między dwoma sąsiednimi punktami)
    print("Chcesz uzupełnic współczynniki całkowanej funkcji kwadratowej ręcznie ręcznie? y/n")
    choice = input()
    if choice.lower() == "y":
        a = float(input("Podaj współczynnik a: "))
        b = float(input("Podaj współczynnik b: "))
        c = float(input("Podaj współczynnik c: "))
        for i in range(n+1):
            x = begin + i * dx  # lewy koniec każdego trapezu
            y = insertFunc(a,b,c,x)
            xTab.append(x)
            yTab.append(y)
        for i in range(len(yTab) - 1):
            pole += ((yTab[i] + yTab[i+1]) / 2) * dx


    else:
        for i in range(n+1):
            x = begin + i * dx  
            y = f(x)
            xTab.append(x)
            yTab.append(y)
        for i in range(len(yTab) - 1):
            pole += ((yTab[i] + yTab[i+1]) / 2) * dx



    return pole, xTab, yTab, dx

def prostokaty():
    begin = int(input("Wpisz początek przedziału : "))
    end =  int(input("Wpisz koniec przedziału : "))
    n = int(input("Wpisz ilość przedziału (im większa wartość tym dokładniejszy wynik) : "))
    xTab = []
    yTab = []
    dx = (end - begin) / n  # szerokość prostokąta(odległość między dwoma sąsiednimi punktami)
    print("Chcesz uzupełnic współczynniki całkowanej funkcji kwadratowej ręcznie ręcznie? y/n")
    choice = input()
    if choice == "y":
        a = float(input("Podaj współczynnik a: "))
        b = float(input("Podaj współczynnik b: "))
        c = float(input("Podaj współczynnik c: "))
        for i in range(n):
            x = begin + i * dx  # lewy koniec każdego prostokąta
            y = insertFunc(a,b,c,x)
            xTab.append(x)
            yTab.append(y)
    else:
        for i in range(n):
            x = begin + i * dx  
            y = f(x)
            xTab.append(x)
            yTab.append(y)



    pole = sum([y * dx for y in yTab])
    return pole, xTab, yTab, dx

#wynik, xTab, yTab, dx = prostokaty()
#print(f"Przybliżona całka metodą prostokątów: {wynik}")


def menu():
    active = True
    while active:
        print("--METODA PROSTOKĄTÓW--")
        wynik,xtab,ytab , dx = prostokaty()
        print("--METODA TRAPEZÓW--")
        wynik1, xTab1, yTab1, dx1 = trapezy()
        print(f"Przybliżona całka metodą prostokątów: {wynik}")
        print(f"Przybliżona całka metodą trapezów: {wynik1}")
        print("Zakończ program: napisz-> end ,aby kontunować nacisnij cokolwiek ")
        end = input()
        if end == "end":
            active = False



menu()