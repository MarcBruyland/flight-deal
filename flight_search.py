#from pprint import pprint
import requests
from flight_data import FlightData
from dotenv.main import load_dotenv
import os

load_dotenv()

TEQUILA_ENDPOINT = os.environ['TEQUILA_ENDPOINT']
TEQUILA_API_KEY = os.environ['TEQUILA_API_KEY']

class FlightSearch:

    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, nights_in_dst_from, nights_in_dst_to, nrOfPersons):
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": nights_in_dst_from,
            "nights_in_dst_to": nights_in_dst_to,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR",
            "adults": nrOfPersons
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )

        try:
            data = response.json()["data"][0]
            via_city = ""
        except IndexError:
            print(f"{destination_city_code}: No direct flights found.")
            query["max_stopovers"] = 2
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=headers,
                params=query,
            )
            try:
                data = response.json()["data"][0]
                via_city = data['route'][0]["cityTo"]
                flight_data = FlightData(
                    price=data["price"] // nrOfPersons,
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=via_city,
                    route=data["route"]
                )
                print(f"{flight_data.destination_city}: {flight_data.price} EUR (via {via_city})")
                return flight_data
            except:
                print(f"{destination_city_code}: No flights with 1 stop either")
                return None
        flight_data = FlightData(
            price=data["price"] // nrOfPersons,
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0],
            stop_overs=0,
            via_city="",
            route=data["route"]
        )
        print(f"{flight_data.destination_city}: {flight_data.price} EUR")
        return flight_data
