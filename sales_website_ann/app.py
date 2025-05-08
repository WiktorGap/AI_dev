import pyodbc
import flask
import torch 
import torch.nn as nn 
import torch.optim as optim
import numpy as np 
from sklearn.preprocessing import MinMaxScaler



connection_string_ = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=THINKBOOK_CODE;'
    r'DATABASE=shop;'
    r'Trusted_Connection=yes;'
)

def connection():
    choice = input("Do you want to use your own connection parameters? (t/n): ").lower().strip()

    if choice == "t":
        server_address = input("Add server address: ")
        database_name = input("Add database name: ")
        user_name = input("User name: ")
        passwd = input("Password: ")

        connection_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server_address};"
            f"DATABASE={database_name};"
            f"UID={user_name};"
            f"PWD={passwd};"
            f"TrustServerCertificate=yes;"
        )
    else:
        connection_string = connection_string_

    try:
        con = pyodbc.connect(connection_string)
        print("Connection established successfully.")
        return con
    except Exception as e:
        print(f"Connection error: {e}")
        return None

model = nn.Sequential(
    nn.Linear(2,8),
    nn.ReLU(),
    nn.Linear(8,1)


)

loss_fun = nn.MSELoss() 
optimizer = optim.Adam(model.parameters(),lr=0.001)

epoches = 100
batch_size = 10 

def getData(con):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Sales;")
        records = cursor.fetchall()
        for r in records:
            r = list(r)
        return records
    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return None

def divadeData(records):
    idxOfProductAndName = []
    priceQunitityTotal = []
    for record in records:
        idxOfProductAndName.append(tuple(record[0:2]))
    for record in records:

        triple = [record[2],record[3],record[5]]
        priceQunitityTotal.append(triple)

    scaler = MinMaxScaler()
    scaled_tab = scaler.fit_transform(priceQunitityTotal)

    scaled_tensor= torch.tensor(scaled_tab,dtype=torch.float32)

    return idxOfProductAndName , scaled_tensor,scaler
        
        


if __name__ == "__main__":
    con = connection()
    if con:
        records = getData(con)
        print(records)
        idxes, nums, scaler = divadeData(records)

        
        print(idxes)
        print("\n")
        print(nums)

       
        X = nums[:, :2]     
        y = nums[:, 2:3]    

        
        for epoch in range(epoches):
            y_pred = model(X)
            loss = loss_fun(y_pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.6f}")
