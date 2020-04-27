import mysql.connector, sys, json

from flask import Flask, request
from collections import defaultdict
from copy import deepcopy
from threading import Lock
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.3')

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'airplaneservice'
}

bought_bookings = []
booked_routes = []
book_index = 0
bookings = {}
bought_seats_per_id = {}

HOURS_IN_DAY = 24
MAX_VALUE = sys.maxsize
lock = Lock()

# Close database connection.
def close_db(cursor, connection):
    cursor.close()
    connection.close()

# Compute a select query to be executed.
def compute_select_query(id, col):
    return "select " + col + " from flights where id=" + str(id) + ";"

# Compute update query to be executed.
def compute_update_query(id, col, value):
    return "update flights set " + col + "=" + \
            str(value) + " where id=" + str(id) + ";"

# Check for two flights if the end of the first one is
# overlapping the start of the second.
def overlapping_flights(first, second):
    end_of_first = first[3] * HOURS_IN_DAY + first[2] + first[4]
    start_of_second =  second[3] * HOURS_IN_DAY + second[2]

    return end_of_first <= start_of_second

# Given two flights compute the time cost from the start of the
# first one until the end of the second one including
# waiting time between these two.
def time_cost(curr, prev):
    end_of_prev =  prev[3] * HOURS_IN_DAY + prev[2] + prev[4]
    start_of_curr = curr[3] * HOURS_IN_DAY + curr[2]
    waiting_time = start_of_curr - end_of_prev

    return curr[4] + waiting_time


# Class to manage flights.
class AirPlaneService:
    def __init__(self, locations, id_flight_map, maximum_flights):
        self.paths = []
        self.graph = defaultdict(list)
        self.id_flight_map = deepcopy(id_flight_map)
        self.locations = deepcopy(locations)
        self.maximum_flights = maximum_flights
    
    def add_edges(self, src, flights):
        self.graph.update({src : flights})

    # Compute all possible routes given a source and a destination.
    def compute_possible_routes(self, source, visited, path, destination):
        if len(path) <= self.maximum_flights and source == destination:
            self.paths.append(deepcopy(path))
            return
        elif len(path) == self.maximum_flights:
            return

        visited.update({source : True})
        for flight in self.graph[source]:
            if len(path) >= 1 and not overlapping_flights(self.id_flight_map.get(path[-1]), flight):
                    continue
            if not visited.get(flight[1]):
                path.append(flight[8])
                self.compute_possible_routes(flight[1], visited, path, destination)
                path.pop()
        visited.update({source : False})

    def all_routes(self, source, destination):
        path = []
        visited = {key: False for key in self.locations}
        self.compute_possible_routes(source, visited, path, destination)
        return self.paths

    # Get the optimal way between source and destination
    # taking into consideration the maximum flights number.
    def compute_optimal_way(self, source, destination):
        all_routes = self.all_routes(source, destination)
        if not all_routes:
            return []

        minimum_path = None
        minimum_cost = MAX_VALUE
        for route in all_routes:
            current = route[0]
            cost = self.id_flight_map.get(current)[4]
            for _, route_hop in enumerate(route, start = 1):
                second = self.id_flight_map.get(route_hop)
                first = self.id_flight_map.get(current)
                cost += time_cost(second, first)
                current = route_hop
            if cost < minimum_cost:
                minimum_cost = cost
                minimum_path = route

        return minimum_path

# Connect to database to execute any query.
def connect_to_db():
    global config
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    return connection, cursor

# Collect locations from flights which are living after
# the given day.
def get_locations_after(start_day):
    locations = []
    (connection, cursor) = connect_to_db()
    sql_query = 'select source, dest from flights where departureDay>=' + str(start_day)
    cursor.execute(sql_query)
    records = cursor.fetchall()
    for record in records:
        source = record[0]
        if source not in locations:
            locations.append(source)

        dest = record[1]
        if dest not in locations:
            locations.append(dest)
    close_db(cursor, connection)

    return locations

# Get flights per id after the given day from database and
# flights given the source location after the given day.
def get_records_after(start_day):
    id_flight_map = {}
    source_flight_map = {}

    (connection, cursor) = connect_to_db()
    sql_query = 'select * from flights where departureDay>=' + str(start_day)
    cursor.execute(sql_query)
    records = cursor.fetchall()

    for record in records:
        source = record[0]
        id = record[8]
        id_flight_map.update({id: record})
        if source not in source_flight_map:
            source_flight_map.update({source: [record]})
        else:
            source_flight_map[source].append(record)
    close_db(cursor, connection)

    return id_flight_map, source_flight_map

# Get route parameters from the user.
def get_route_details():
    source = str(request.args.get('source') or "")
    destination = str(request.args.get('destination') or "")
    maximum_flights = int(request.args.get('maximum_flights') or 0)
    departure_day = int(request.args.get('departureDay') or 0)
    return source, destination, maximum_flights, departure_day

def compute_output(path, id_flight_map):
    flight_details = []
    hops_id = []
    for hop in path:
        flight = id_flight_map[hop]
        route = "<ID>: " + str(flight[8]) + \
                  " source: " + flight[0] + " > > destination: " + flight[1] + \
                  " <departure hour>: " + str(flight[2]) + \
                  " <departure day>: " + str(flight[3]) + \
                  " <duration> : " + str(flight[4])
        flight_details.append(route)
        hops_id.append(str(hop))

    return json.dumps([flight_details, hops_id])

# Flask route for `getOptimalRoute` request type.
# It returns the final result to the client as a path.
@app.route('/getOptimalRoute')
def get_optimal_route() -> str:
    (source, destination, maximum_flights, departure_day) = get_route_details()
    locations = get_locations_after(departure_day)
    (id_flight_map, source_flight_map) = get_records_after(departure_day)
    graph = AirPlaneService(locations, id_flight_map, maximum_flights)

    for key, value in source_flight_map.items():
        graph.add_edges(key, value)

    path = graph.compute_optimal_way(source, destination)
    if len(path) == 0:
        return ""
    return compute_output(path, id_flight_map)


@app.route('/getAll')
def get_all() -> str:
    (connection, cursor) = connect_to_db()
    source = str(request.args.get('source') or "")
    destination = str(request.args.get('destination') or "")
    departure_day = int(request.args.get('departureDay') or 0)
    sql_query = 'select * from flights where departureDay=' + \
            str(departure_day) + " and " + \
            "source='" + source + "' and " + \
            "dest='" + destination + "'"
    cursor.execute(sql_query)
    records = cursor.fetchall()
    result = []

    for route in records:
        output = "id: " + str(route[8]) + \
                " clasa: " + str(route[10]) + \
                " tip tren: " + route[11] + \
                " vagon dormit:" + str(route[12]) + \
                " plecare: " + route[0] + \
                " sosire: " + route[1] + " ora: " + str(route[2]) + \
                " data: " + str(route[3]) + " durata: " + str(route[4]) + \
                " locuri pe scaun: " + str(route[5]) + \
                " cumparate: " + str(route[7])
        result.append(output)
    close_db(cursor, connection)
    return json.dumps(result)

@app.route('/filterPrice')
def filter_price() -> str:
    (connection, cursor) = connect_to_db()
    source = str(request.args.get('source') or "")
    destination = str(request.args.get('destination') or "")
    departure_day = int(request.args.get('departureDay') or 0)
    filterType = int(request.args.get('filterType') or "")
    sql_query = 'select * from flights where departureDay=' + \
            str(departure_day) + " and " + \
            "source='" + source + "' and " + \
            "dest='" + destination + "' and " + \
            "price<='" + str(filterType) + "'"
    cursor.execute(sql_query)
    records = cursor.fetchall()
    result = []

    for route in records:
        output = "id: " + str(route[8]) + \
                " clasa: " + str(route[10]) + \
                " tip tren: " + route[11] + \
                " vagon dormit:" + str(route[12]) + \
                " plecare: " + route[0] + \
                " sosire: " + route[1] + " ora: " + str(route[2]) + \
                " data: " + str(route[3]) + " durata: " + str(route[4]) + \
                " locuri pe scaun: " + str(route[5]) + \
                " cumparate: " + str(route[7])
        result.append(output)
    close_db(cursor, connection)
    return json.dumps(result)

@app.route('/filterType')
def filter_type() -> str:
    (connection, cursor) = connect_to_db()
    source = str(request.args.get('source') or "")
    destination = str(request.args.get('destination') or "")
    departure_day = int(request.args.get('departureDay') or 0)
    filterType = str(request.args.get('filterType') or "")
    sql_query = 'select * from flights where departureDay=' + \
            str(departure_day) + " and " + \
            "source='" + source + "' and " + \
            "dest='" + destination + "' and " + \
            "traintype='" + filterType + "'"
    cursor.execute(sql_query)
    records = cursor.fetchall()
    result = []

    for route in records:
        output = "id: " + str(route[8]) + \
                " clasa: " + str(route[10]) + \
                " tip tren: " + route[11] + \
                " vagon dormit:" + str(route[12]) + \
                " plecare: " + route[0] + \
                " sosire: " + route[1] + " ora: " + str(route[2]) + \
                " data: " + str(route[3]) + " durata: " + str(route[4]) + \
                " locuri pe scaun: " + str(route[5]) + \
                " cumparate: " + str(route[7])
        result.append(output)
    close_db(cursor, connection)
    return json.dumps(result)

@app.route('/filterSleep')
def filter_sleep() -> str:
    (connection, cursor) = connect_to_db()
    source = str(request.args.get('source') or "")
    destination = str(request.args.get('destination') or "")
    departure_day = int(request.args.get('departureDay') or 0)
    filterType = int(request.args.get('filterType') or 0)
    sql_query = 'select * from flights where departureDay=' + \
            str(departure_day) + " and " + \
            "source='" + source + "' and " + \
            "dest='" + destination + "' and " + \
            "sleeproom=" + str(filterType)
    cursor.execute(sql_query)
    records = cursor.fetchall()
    result = []

    for route in records:
        output = "id: " + str(route[8]) + \
                " clasa: " + str(route[10]) + \
                " tip tren: " + route[11] + \
                " vagon dormit:" + str(route[12]) + \
                " plecare: " + route[0] + \
                " sosire: " + route[1] + " ora: " + str(route[2]) + \
                " data: " + str(route[3]) + " durata: " + str(route[4]) + \
                " locuri pe scaun: " + str(route[5]) + \
                " cumparate: " + str(route[7])
        result.append(output)
    close_db(cursor, connection)
    return json.dumps(result)

@app.route('/filterClss')
def filter_class() -> str:
    (connection, cursor) = connect_to_db()
    source = str(request.args.get('source') or "")
    destination = str(request.args.get('destination') or "")
    departure_day = int(request.args.get('departureDay') or 0)
    filterType = int(request.args.get('filterType') or 0)
    sql_query = 'select * from flights where departureDay=' + \
            str(departure_day) + " and " + \
            "source='" + source + "' and " + \
            "dest='" + destination + "' and " + \
            "class=" + str(filterType)
    cursor.execute(sql_query)
    records = cursor.fetchall()
    result = []

    for route in records:
        output = "id: " + str(route[8]) + \
                " clasa: " + str(route[10]) + \
                " tip tren: " + route[11] + \
                " vagon dormit:" + str(route[12]) + \
                " plecare: " + route[0] + \
                " sosire: " + route[1] + " ora: " + str(route[2]) + \
                " data: " + str(route[3]) + " durata: " + str(route[4]) + \
                " locuri pe scaun: " + str(route[5]) + \
                " cumparate: " + str(route[7])
        result.append(output)
    close_db(cursor, connection)
    return json.dumps(result)



# Flask route for `bookTicket` request type.
# It returns the final result to the client as a reservation ID.
@app.route('/bookTicket')
def book_ticket() -> str:
    global book_index
    global lock
    global bookings
    global booked_routes
    ids_path = ""
    ids_to_book = request.args.getlist('flight')
    (connection, cursor) = connect_to_db()

    for id in ids_to_book:
        ids_path += ' > > ' + str(id)
        sql_query = compute_select_query(id, "booked")
        cursor.execute(sql_query)
        booked_seats = cursor.fetchone()[0]
        if booked_seats < 1:
            bookings = {}
            return "NO_SEATS"
        bookings[id] = booked_seats - 1


    lock.acquire()
    for id in ids_to_book:
        sql_query = compute_update_query(id, "booked", bookings[id])
        cursor.execute(sql_query)
        connection.commit()
    lock.release()

    book_index += 1
    close_db(cursor, connection)
    route = '[Book: ' + str(book_index) + ']' + ids_path
    booked_routes.append(route)
    return '\n' + route

# Flask route for `buyTicket` request type.
# It returns the Boarding Pass to the client.
@app.route('/buyTicket')
def buy_ticket() -> str:
    global bought_bookings
    global lock
    global booked_routes
    global bought_seats_per_id

    booking_id = request.args.get('id', type=str, default="")
    if booking_id not in booked_routes:
        return "ID_NOT_BOOKED"
    if booking_id in bought_bookings:
        return "BOUGHT_ALREADY"
    (connection, cursor) = connect_to_db()
    flight_ids = booking_id.split(' > > ')[1:]

    for id in flight_ids:
        sql_query = compute_select_query(id, "seats")
        cursor.execute(sql_query)
        seats = cursor.fetchone()[0]

        sql_query = compute_select_query(id, "bought")
        cursor.execute(sql_query)
        bought_seats = cursor.fetchone()[0]

        if bought_seats > seats - 1:
            return "NO_AVAILABLE_SEATS"
        bought_seats += 1
        bought_seats_per_id[id] = bought_seats

    boarding_pass = " <<  >>: "
    lock.acquire()
    for id in flight_ids:
        boarding_pass += "[<ID> : " + str(id) + "; " + \
                         "<SEAT> : " + str(bought_seats_per_id[id]) + "]  "
        sql_query = compute_update_query(id, "bought", bought_seats_per_id[id])
        cursor.execute(sql_query)
        connection.commit()

    bought_bookings.append(booking_id)
    lock.release()

    close_db(cursor, connection)
    return boarding_pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')
