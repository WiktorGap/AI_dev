import matplotlib.pyplot as plt
carats = [0.23, 0.45, 0.31, 0.76, 0.61]
prices = [326, 845, 500, 1800, 1500]
n = len(carats)




def avgCarats(carats):
    avg = sum(carats)/len(carats)
    return avg
def avgPrice(price):
    avg = sum(price)/len(price)
    return avg

def fit_regression_line(carats, prices, n):
    avgX = avgCarats(carats)
    avgY = avgPrice(prices)
    sum_x_squered = 0
    for i in range(n):
        ans = (carats[i] - avgX) ** 2
        sum_x_squered += ans
    sumMulti = 0
    for i in range(n):
        ans = (carats[i] - avgX) * (prices[i] - avgY)
        sumMulti += ans

    b1 = sumMulti / sum_x_squered
    b0 = avgY - (b1 * avgX)
    min_x = min(carats)
    max_x = max(carats)
    y1 = b0 + b1 * min_x
    y2 = b0 + b1 * max_x

    return b0, b1, (min_x, y1), (max_x, y2)


b0, b1, (min_x, y1), (max_x, y2) = fit_regression_line(carats, prices, n)


plt.scatter(carats, prices, color='blue', label='Dane')
plt.plot([min_x, max_x], [y1, y2], color='red', label='Linia regresji')

plt.xlabel('Karaty')
plt.ylabel('Cena')
plt.title('Regresja liniowa: cena ~ karaty')
plt.legend()
plt.grid(True)
plt.show()
