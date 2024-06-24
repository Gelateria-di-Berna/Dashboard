import requests
import pandas as pd
from ..keys import helloTess_key

HEADERS = {
    "accept": "application/json",
    "hellotess-api-key": helloTess_key
}

def _fetch_stores_json() -> list[dict[str,]]:
    global HEADERS
    url_stores = "https://gelateriadiberna.bo7.hellotess.com/api/basedata/v1/stores"
    response = requests.get(url_stores, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print("Failed to retrieve invoices. Status code:", response.status_code)
        return None
    
def _fetch_invoices_json() -> list[dict[str,]]:
    global HEADERS
    url_invoices = "https://gelateriadiberna.bo7.hellotess.com/v1/invoices/last/10000"
    response = requests.get(url_invoices, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve invoices. Status code:", response.status_code)
        return None

def get_hello_tess_invoice_df() -> pd.DataFrame:
    data = {}
    data["location"] = []
    data["date"]  = []
    data["price"] = []

    for invoice in _fetch_invoices_json():
        location = None
        date = None
        price = None
        try:
            location = invoice["location"]["store"]["name"]
        except:
            pass
        try:
            date = invoice["dateAdded"]
        except:
            pass
        try:
            price = invoice["totals"]["net"]
        except:
            pass

        data["location"].append(location)
        data["date"].append(date)
        data["price"].append(price)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])    
    
    return df
