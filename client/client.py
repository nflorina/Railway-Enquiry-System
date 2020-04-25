import sys, json, requests

# Get details such as source, destination etc from the user
# to form a request.
def get_optimal_route_input():
    print("Introdu detaliile rutei: ")
    source = input("[statie plecare] : ")
    destination = input("[statie destinatie] : ")
    maximum_flights = input("[shimbari] : ")
    day = input("[data] : ")
    return source, destination, maximum_flights, day

def get_route_info():
    print("Please enter the route details.")
    source = input("<source> : ")
    destination = input("<destination> : ")
    day = input("<departure day> : ")
    return source, destination, day

# Compute a request URL from de given details regarding the route.
# Return the service responce.
def send_request(url, source, destination, maximum_flights, day):
    req_url = url + "/getOptimalRoute?" + \
          "source=" + source + "&destination=" + destination + \
          "&maximum_flights=" + maximum_flights + "&departureDay=" + day
    return requests.get(req_url)

def send_all_request(url, source, destination, day):
    req_url = url + "/getAll?" + \
          "source=" + source + "&destination=" + destination + \
           "&departureDay=" + day
    return requests.get(req_url)

# Manage the server response for the `optimal route` request.
# Display the result or a proper message depending on the result.
def get_optimal_route(url):
    (source, destination, maximum_flights, day) = \
        get_optimal_route_input()
    request = send_request(url, source, destination,
        maximum_flights, day)
    if request.text == "":
        print(" > > Mai incearca")
    else:
        text = json.loads(request.text)
        info_flights = text[0]
        info_id = text[1]
        print("\n")
        for flight in info_flights:
            print(" > > > " + flight)
        for id in info_id:
            print(" > > > " + id)

def show_routes(url):
    (source, destination, day) = get_route_info()
    request = send_all_request(url, source, destination, day)
    if request.text == "":
        print(" > > Incearca o noua ruta de tren!")
    else:
        text = json.loads(request.text)
        for info in text:
            print(info)
    result = input("Aplici un filtru in cautare? [y/n]\n")
    if result == "y":
        filter(url, source, destination, day)

def filter_type(url, source, destination, day):
    filterType = input("Tipul trenului: IR/R/P/A/IC/EC/S/EN\n")
    req_url = url + "/filterType?" + \
          "source=" + source + "&destination=" + destination + \
           "&departureDay=" + day + "&filterType=" + filterType
    request = requests.get(req_url)
    if request.text == "":
        print(" > > Incearca iar!")
    else:
        text = json.loads(request.text)
        for info in text:
            print(info)

def filter_price(url, source, destination, day):
    filterPrice = input("Pret maxim calatorie: \n")
    req_url = url + "/filterPrice?" + \
          "source=" + source + "&destination=" + destination + \
           "&departureDay=" + day + "&filterType=" + filterPrice
    request = requests.get(req_url)
    if request.text == "":
        print(" > > Incearca iar!")
    else:
        text = json.loads(request.text)
        for info in text:
            print(info)

def filter_sleep(url, source, destination, day):
    filterSleep = input("Vagon de dormit? 1/0: \n")
    req_url = url + "/filterSleep?" + \
          "source=" + source + "&destination=" + destination + \
           "&departureDay=" + day + "&filterType=" + filterSleep
    request = requests.get(req_url)
    if request.text == "":
        print(" > > Incearca iar!")
    else:
        text = json.loads(request.text)
        for info in text:
            print(info)

def filter_class(url, source, destination, day):
     filterClss = input("Clasa: 1/2 \n")
     req_url = url + "/filterClss?" + \
           "source=" + source + "&destination=" + destination + \
            "&departureDay=" + day + "&filterType=" + filterClss
     request = requests.get(req_url)
     if request.text == "":
         print(" > > Incearca iar!")
     else:
         text = json.loads(request.text)
         for info in text:
             print(info)

def filter(url, source, destination, day):
    print("\n")
    print("#1 Tip tren: IR(InterRegio), A(Accelerat), P(Personal), IC(InterCity), EU(EuroCity), S (Special)")
    print("#2 Pret")
    print("#3 Vagon de dormit")
#     print("#4 Class")
    index = input("\nIndex: ")
    operation = int(index)
    if operation == 1:
        filter_type(url, source, destination, day)
    elif operation == 2:
        filter_price(url, source, destination, day)
    elif operation == 3:
        filter_sleep(url, source, destination, day)
    elif operation == 4:
        filter_class(url, source, destination, day)



# Compute a `book` request URL for the service.
# Get the service's response.
def send_book_request(url, count_flights):
    req_url = url + "/bookTicket?"
    for x in range(count_flights):
        flight = input("<flight id> : ")
        req_url += "flight=" + flight
        if x != count_flights - 1:
            req_url += "&"
    return requests.get(req_url)

# Manage the `book` request response received from the server.
# Display the Reservation ID or a proper message in case of issue.
def book_ticket(url):
    count_flights = int(input("<how many flights you book> : "))
    request = send_book_request(url, count_flights)
    if request.text == "NO_SEATS":
        print("\n> > Unfortunatelly no seats are available or " +
              "one of your flights was canceled! :( ")
    else:
        print("\n > > Your reservation_ID is: " + request.text)


# Send a `buy` request to the server.
# Get the result from the server.
def send_buy_request(url, booking_id):
    req_url = url + "/buyTicket?" + "id=" + booking_id
    return requests.get(req_url)

# Manage a `buy` request response received from the server.
# Display a proper message.
def buy_ticket(url):
    booking_id = input("<reservation id> : ")
    _ = input("<credit card number made of 4 digits> : ")
    request = send_buy_request(url, booking_id)
    if request.text == "NO_AVAILABLE_SEATS":
        print("\n > > Unfortunatelly it's already full!")
    elif request.text == "ID_NOT_BOOKED":
        print("\n > > Flight not previously booked! CHECK YOUR " +
              "RESERVATION ID! It must be like: " +
              "[Book: book_index] > > id > > id ...")
    elif request.text == "BOUGHT_ALREADY":
        print("\n > > Unfortunatelly it's already bought!")
    else:
        print("\n> > This is your boarding pass: \n " + request.text)


# Print a welcome board for the `client` page.
def print_welcome():
    print("\n\n")
    print("                        ______")
    print("                       / .===. /\/")
    print("                       \/ 8 8 \/")
    print("                       ( \___/ )")
    print("      _____________ooo__\_____/__________________")
    print("    //                                           /|")
    print("    |                Bine ai venit!               |")
    print("    |             Aplicatia CFR Calatori          |")
    print("    |                                             |")
    print("     /\___________________________ooo_____________//")
    print("                        |  |  |")
    print("                        |_ | _|")
    print("                        |  |  |")
    print("                        |__|__|")
    print("                       _/--'Y'-|_")
    print("                     (____/ \____)")

# Choose the operation depenfing on the index of the user.
def choose_operation(idx, url):
    operation = int(idx)
    if operation == 1:
        show_routes(url)
    elif operation == 2:
        get_optimal_route(url)
    elif operation == 3:
        book_ticket(url)
    elif operation == 4:
        buy_ticket(url)
    else:
        print("> > > > > > > > > > EXIT CFR Calatori < < < < < < < < < < < ")
        exit()

       
if __name__ == '__main__':
    sys_url = sys.argv[1] if len(sys.argv) > 1 else '.'

    print_welcome()
    while 1:
            print("\n# # # # # # # Alege ce doresti sa faci:  # # # # # # #\n")
            print("- - - - - - - - #1 Vizualizare rute  - - - - - - - - - - - - - -")
            print("- - - - - - - - #2 Cea mai rapida ruta - - - - - - - - - - - - - ")
            print("- - - - - - - - #3 Rezervare bilet - - - - - - - - - - - - - - - ")
            print("- - - - - - - - #4 Cumparare bilet - - -  - - - - - - - - - - - -")
            print("- - - - - - - - #5 Iesire - - - - - - - - - - - - - - - -- - - - ")

            try:
                index = input("Index is: ")
                if (index.isnumeric() and (not 1 <= int(index) <= 5)) or (not index.isnumeric()):
                    print("\n# # # # # # # TRY AGAIN! Please enter a valid number! # # # # # #\n")
                    continue
                choose_operation(index, sys_url)
            except EOFError as e:
                break
