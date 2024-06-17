import json
import requests
import pandas as pd
from keys import helloTess_key

HEADERS = {
    "accept": "application/json",
    "hellotess-api-key": helloTess_key
}

def get_stores_json():
    global HEADERS
    url_stores = "https://gelateriadiberna.bo7.hellotess.com/api/basedata/v1/stores"
    response = requests.get(url_stores, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve invoices. Status code:", response.status_code)
        return None

def get_all_stores() -> list[dict[str,]]:
    return get_stores_json["items"]
    
def get_invoices_json():
    global HEADERS
    url_stores = "https://gelateriadiberna.bo7.hellotess.com/api/finance/v1/invoices"
    response = requests.get(url_stores, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve invoices. Status code:", response.status_code)
        return None

def get_all_invoices() -> list[dict[str,]]:
    invoice_json = get_invoices_json()
    if invoice_json:
        return invoice_json["items"]
    else:
        return None

def save_invoices() -> None:
    with open("docs/json/invoices.json", mode="w") as file:
        json.dump(get_invoices_json(), file)

def save_stores() -> None:
    with open("docs/json/stores.json", mode="w") as file:
        json.dump(get_stores_json(), file)

def create_dataframe_csv() -> pd.DataFrame:
    data = {}
    data["location"] = []
    data["date"]  = []
    data["price"] = []

    for invoice in get_all_invoices():
        for article in invoice["articles"]:
            location = None
            date = None
            price = None
            try:
                location = invoice["location"]["store"]["name"]
            except:
                pass
            try:
                date = article["dateAdded"]
            except:
                pass
            try:
                price = article["totalPrice"]
            except:
                pass

            data["location"].append(location)
            data["date"].append(date)
            data["price"].append(price)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df

def save_dataframe_csv(df: pd.DataFrame) -> None:
    df.to_csv("./docs/dataframes/dataframe.csv", index=False)

save_dataframe_csv(create_dataframe_csv())
df = pd.read_csv("./docs/dataframes/dataframe.csv")