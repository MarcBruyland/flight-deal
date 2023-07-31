from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        destination["home"],
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today,
        nights_in_dst_from=destination["minNrOfDays"],
        nights_in_dst_to=destination["maxNrOfDays"],
        nrOfPersons=destination["nrOfPersons"]
    )
    if flight is None:
        continue
    if flight.price < destination["lowestPricePerPerson"]:
        msg = f"Low price alert! Only {flight.price} EUR per person to fly from {flight.origin_city}-{flight.origin_airport}\
 to {flight.destination_city}-{flight.destination_airport} and back, from {flight.out_date} to {flight.return_date}."
        if flight.via_city:
            msg += f"\nThe flight has a stop-over via {flight.via_city}."
        for route in flight.route:
            airline = route["airline"]
            city_code_from = route["cityCodeFrom"]
            city_code_to = route["cityCodeTo"]
            flight_no = route["flight_no"]
            departure = route["local_departure"][:16].replace('T', '_')
            arrival = route["local_arrival"][:16].replace('T', '_')
            msg += f"\n   {city_code_from}-{city_code_to} {airline}{flight_no} {departure} {arrival}"
        msg += f"\nbooking link: https://www.google.co.uk/flights?hl=en#flt={destination['home']}.{destination['iataCode']}.{flight.out_date}*{destination['iataCode']}.{destination['home']}.{flight.return_date}"

        notification_manager.send_msg(message=msg, lst_emails=destination["email"])