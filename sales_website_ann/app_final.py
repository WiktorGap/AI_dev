import pyodbc
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
from flask import Flask , render_template
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)



@app.route('/')
def home():
    con = connection()
    if not con:
        return "Błąd połączenia z bazą."

    records = getData(con)
    return render_template('index.html', records=records)
@app.route('/chart')
def chart():
    results = predict_data()
    if isinstance(results, str):
        return results

    product_ids = [r[0] for r in results]
    demands = [r[2] for r in results]
    profits = [r[3] for r in results]

   
    fig, ax = plt.subplots()
    ax.plot(product_ids, demands, label="Popyt", marker='o')
    ax.plot(product_ids, profits, label="Zysk", marker='x')
    ax.set_xlabel("ID Produktu")
    ax.set_ylabel("Wartość")
    ax.set_title("Prognoza popytu i zysku")
    ax.legend()

   
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    return render_template("chart.html", chart_data=img_data)


connection_string_ = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=THINKBOOK_CODE;'
    r'DATABASE=shop;'
    r'Trusted_Connection=yes;'
)


def connection():
    try:
        con = pyodbc.connect(connection_string_)
        print("Connection established successfully.")
        return con
    except Exception as e:
        print(f"Connection error: {e}")
        return None



model = nn.Sequential(
    nn.Linear(5, 8),  
    nn.ReLU(),
    nn.Linear(8, 2) 
)

loss_fun = nn.MSELoss()  
optimizer = optim.Adam(model.parameters(), lr=0.001)

epoches = 100
batch_size = 10


def getData(con):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Sales;")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return None


def divideData(records):
    idxOfProductAndName = []
    priceQuantityTotal = []
    for record in records:

        product_id = int(record[0])
        date = record[4]
        month = date.month  
        price = record[2]
        quantity = record[3]
        total = record[5]

        idxOfProductAndName.append((product_id, month))
        priceQuantityTotal.append([product_id, month, price, quantity, total])

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(priceQuantityTotal)
    scaled_tensor = torch.tensor(scaled_data, dtype=torch.float32)

    return idxOfProductAndName, scaled_tensor, scaler

def predict_data():
    con = connection()
    if not con:
        return "Błąd połączenia z bazą."

    records = getData(con)
    if not records:
        return "Brak danych."

    idxes, nums, scaler = divideData(records)

    X = nums[:, :5]
    y = nums[:, 3:]

    for epoch in range(epoches):
        y_pred = model(X)
        loss = loss_fun(y_pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    results = []
    with torch.no_grad():
        for i, product_data in enumerate(nums):
            sample_data = product_data[:5].unsqueeze(0)
            prediction = model(sample_data)
            product_id, month = idxes[i]
            demand = prediction[0][0].item()
            profit = prediction[0][1].item()
            results.append((product_id, month, round(demand, 2), round(profit, 2)))

    return results




if __name__ == "__main__":
    app.run()
