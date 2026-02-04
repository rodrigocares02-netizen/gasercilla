import pandas as pd
import os
from datetime import datetime

DB_FILE = "pedidos.csv"

def get_orders():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Fecha", "Cliente", "Pedido", "Dirección", "Total", "Pago"])

def save_order(order_data):
    df = get_orders()
    new_row = pd.DataFrame([order_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return df
