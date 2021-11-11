# reference from https://github.com/SiLingTan/TaxiBookingAPI/blob/master/app.py
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# define the list of drivers and customers
drivers = [
    {
        'name': 'Embryo Mithen',
        'location': {'x': 1, 'y': 2},
        'willDrivenDistance': 12,
        'carCapacity': 4
    },
    {
        'name': 'Maximillian Berger',
        'location': {'x': 2, 'y': 4},
        'willDrivenDistance': 25,
        'carCapacity': 6
    },
    {
        'name': 'Margie Donnelly',
        'location': {'x': 9, 'y': 3},
        'willDrivenDistance': 31,
        'carCapacity': 2
    },
]

users = [
    {
        'customerName': 'Raymond Reddignton',
        'customerLocation': {'x': 3, 'y': 0},
        'customerDestination': {'x': 6, 'y': 4},
        'customerGuestCount': 2

    },
]


class Users(Resource):
    pass


class Driver(Resource):
    def post(self):
        data_parser = reqparse.RequestParser()  # declare normal parser

        data_parser.add_argument('name', required=True)  # start data parsing
        data_parser.add_argument('loc', required=True)
        data_parser.add_argument('des', required=True)
        data_parser.add_argument('guest_count', required=True)
        argsParser = data_parser.parse_args()  # declaring the arguments parsing
        # splitting the data for location and destination
        current_loc_X, current_loc_Y = argsParser['loc'].split(',')
        to_X, to_Y = argsParser['des'].split(',')

        user_request = {
            'user_name': argsParser['name'],
            'req_loc': {
                'x': int(current_loc_X),
                'y': int(current_loc_Y)
            },
            'destination': {
                'x': int(to_X),
                'y': int(to_Y)
            },
            'guestCount': int(argsParser['guest_count'])
        }
        willDriveDistance = distance_cal([user_request['req_loc']['x'], user_request['req_loc']['y']],
                                         [user_request['destination']['x'], user_request['destination']['y']])
        carCapacity = user_request['guestCount']  # the guest count
        driverAssigned = findSuitableDriver(drivers, user_request)
        return jsonify({
            'driverFound': driverAssigned,
            'totalDistanceTravel': willDriveDistance,
            'totalGuest': carCapacity
        })


def findSuitableDriver(driverList, userData):
    driverAssign = None
    shortestDistance = 0
    temp_distance = 0

    for Driver in driverList:
        driver_X = Driver['location']['x']  # current driver location
        driver_y = Driver['location']['y']
        to_X = userData['req_loc']['x']  # user request location
        to_y = userData['req_loc']['y']

        temp_distance = distance_cal(
            [driver_X, driver_y], [to_X, to_y])

        if shortestDistance == 0:
            driverAssign = Driver
            shortestDistance = temp_distance
        elif shortestDistance >= temp_distance:
            driverAssign = Driver
            shortestDistance = temp_distance
    return driverAssign


def distance_cal(from_loc, to_loc):
    return abs(to_loc[0]-from_loc[0]) + abs(to_loc[1]-from_loc[1])


api.add_resource(Driver, '/api/search/drivers')
api.add_resource(Users, '/users')

# Default page(to avoid display error message)


@app.route('/')
def blank():
    return "THIS IS A CLONE GRAB API"

# Error Handling (When error happened, jump error 404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=False)


# api/search/drivers?name=Raymond&loc=1,1&des=3,2&guest_count=2
