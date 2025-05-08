# AutoConfigMatch

## 🇵🇱 Opis (PL)

**Autor:** Wiktor Gap----

AutoConfigMatch to konsolowy program w C++, który umożliwia:

1. Przeglądanie danych modelu (BMW)
2. Tworzenie własnej konfiguracji samochodu
3. Dopasowanie konfiguracji do najbliższego istniejącego modelu
4. Filtrowanie modeli na podstawie zakresu wartości

---

### 🔧 Instrukcja obsługi



#### 1. Przegląd modeli:
- Program domyślnie przegląda tylko BMW
- Pokazuje:
  - wartość bazową
  - sumę wartości części
  - łączną wartość

#### 2. Tworzenie konfiguracji:
- Podaj nazwę części: dowolny tekst (np. `SilnikX`)
- Podaj wartość części: liczba całkowita dodatnia (np. `5`)
- Czy dodać kolejną część? (t/n): `t` = tak, `n` = nie

#### 3. Dopasowanie:
- Po zakończeniu tworzenia konfiguracji zostanie pokazany model o najbliższej wartości

#### 4. Filtr zakresu:
- Podaj zakres (np. `10 20`)
- Program pokaże modele, których wartość mieści się w tym zakresie

---

### 💡 Przykład

**Wejście:**
Podaj nazwę części: SilnikX
Podaj wartość części: 6
Dodać kolejną część? (t/n): t
Podaj nazwę części: Hamulce
Podaj wartość części: 4
Dodać kolejną część? (t/n): n

**Wyjście:**
Twoja konfiguracja: 10 punktów
Najlepsze dopasowanie: Audi (13 punktów)
Modele w zakresie 5-15: Toyota, Audi





## 🇬🇧 English Version

**Author:** Wiktor Gapi---
AutoConfigMatch is a command-line C++ application that lets you:

1. Browse car model data (BMW)
2. Create your own vehicle configuration
3. Find the closest matching existing model
4. Filter models based on a value range

---

### 🔧 Instructions


#### 1. Model browsing:
- Program browses only BMW by default
- Displays:
  - base value
  - sum of parts
  - total value

#### 2. Configuration creation:
- Enter part name: any text (e.g. `EngineX`)
- Enter part value: positive integer (e.g. `5`)
- Add another part? (t/n): `t` = yes, `n` = no

#### 3. Matching:
- After your config is done, the closest matching model will be shown

#### 4. Value range filter:
- Enter a range (e.g. `10 20`)
- Program shows models whose value falls within that range

---

### 💡 Example

**Input:**
Enter part name: EngineX
Enter part value: 6
Add another part? (t/n): t
Enter part name: Brakes
Enter part value: 4
Add another part? (t/n): n

**Output:**
Your configuration: 10 points
Best match: Audi (13 points)
Models in range 5-15: Toyota, Audi
