#from pprint import pprint
import requests
from dotenv.main import load_dotenv
import os

load_dotenv()

SHEETY_PRICES_ENDPOINT = os.environ['SHEETY_PRICES_ENDPOINT']  # url contains api key giving access to a Google sheet

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        # print(data)
        self.destination_data = data["prices"]
        for dest in self.destination_data:
            if ";" in dest["email"]:
                lst = dest["email"].split(";")
                dest["email"] = lst
            else:
                email = dest["email"]
                dest["email"] = [email]
        print(self.destination_data)
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)
