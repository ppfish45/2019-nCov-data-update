from const.raw import raw_flight_code, raw_car_code

flight_code = [element["code"] for element in raw_flight_code]

car_code = [element["code"] for element in raw_car_code]

train_code = [
    "G", "C", "D", "S", "Z", "T", "K", "L", "Y"
]
