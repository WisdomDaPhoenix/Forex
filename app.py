import requests
import pandas as pd
import time
from pprint import pprint
source = input("Enter source or base currency: ").upper()
n = eval(input("How many output currencies do you like to see: "))
currencies = ""
for i in range(n):
  curr = input("Pls enter output currency: ").upper()+","
  currencies = currencies + curr
currencies = currencies[ :-1]
print(currencies)

def getQuotes():
  url = f"https://api.apilayer.com/currency_data/live?source={source}&currencies={currencies}"
  payload = {}
  headers = {
    "apikey": "Xw3SK9l9Cl88sFLexTANbiAhK0A7Xs5T"
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  status_code = response.status_code
  # print(type(response.content))  # Returns bytes
  print("Status of request: ",status_code)
  result = response.json()
  # pprint(result)
  print(result["quotes"])
  others_vals = list(result["quotes"].values())
  others_cur = [key[3:] for key in result["quotes"]]
  # print(type(result["quotes"]))
  print(others_cur)
  print(others_vals)


  ratestab = pd.DataFrame({
    "Currency": others_cur,
    "Rate": others_vals
  })
  ratestab.index = ratestab.index + 1
  print(f"-------------RATES TABLE FOR {source.upper()}---------------")
  print(ratestab)
  quotes = dict(zip(others_cur, others_vals))
  return quotes

try:
  pricedict = getQuotes()
  mytrdcur = input("Trade on: ").upper()
  while mytrdcur == "":
    mytrdcur = input("Invalid currency! Trade on: ").upper()
  current = pricedict[mytrdcur]
  print(f"Current Price: {current}")
except ConnectionError as ce:
  print("Bad Connection".format(ce))
except ValueError:
  print("Wrong value type input! ")
else:
  if mytrdcur in pricedict:
    decision = input("Price decision - Up (U) or Down (D) ? : ").upper()
    trade_time = eval(input("Trading time (10secs, 30secs, 45secs or 1 min): "))
    time.sleep(trade_time)
    pricedict = getQuotes()
    new = pricedict[mytrdcur]
    print(f"New Price: {new}")
    if new > current and decision == "U":
      print("You won the trade!")
    elif new < current and decision == "U":
      print("You lost the trade!")
    elif new < current and decision == "D":
      print("You won the trade!")
    elif new > current and decision == "D":
      print("You lost the trade!")
    else:
      print("You neither won nor lost!")






