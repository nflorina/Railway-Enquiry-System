import mysql.connector
config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'airplaneservice',
    'auth_plugin': 'mysql_native_password'
}
def db_down(connection, cursor):
    cursor.close()
    connection.close()

# Establish the connection to databases using the global configuration.
def db_connection():
    global config
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    return connection, cursor

# Execute a given sql query.
def execute_query(query):
    (connection, cursor) = db_connection()
    cursor.execute(query)
    connection.commit()
    db_down(connection, cursor)
    print(" > > > DONE")


# Get all content from databases and display it.
def see_all():
    (connection, cursor) = db_connection()
    cursor.execute('select * from flights')
    for route in cursor:
        output = "id: " + str(route[8]) + \
                " clasa: " + str(route[10]) + \
                " tip tren: " + route[11] + \
                " vagon dormit:" + str(route[12]) + \
                " plecare: " + route[0] + \
                " sosire: " + route[1] + " ora: " + str(route[2]) + \
                " data: " + str(route[3]) + " durata: " + str(route[4]) + \
                " locuri pe scaun: " + str(route[5]) + \
                " cumparate: " + str(route[7])

#          output = flight[11] + " : " + str(flight[8]) + " pleaca la " + \
#                   str(flight[2]) + " din " + flight[0] + " -> " +  flight[1]  + \

        print(output)
    db_down(connection, cursor)

# Compute an insert sql query from given parameters.
def insert_query(id, source, destination, dep_hour, dep_day, duration, nr_seats, price, clasa, tip):
    booked = str(int(1.1 * int(nr_seats)))
    query = "insert into flights values (" + \
            "'" + source + "', " + "'" + \
            destination + "', '" + dep_hour + \
            "', '" + dep_day + "', '" + \
            duration + "', '" + nr_seats + \
            "', '" +  booked + "', 0,'" + id + "', " + \
            "'" + price + "', " + "'" + clasa + "', " + \
            "'" + tip + "', 1)"
    return query

# Request parameters from the user. These are used to
# compute an insert sql query.
def get_insert_input():
    print("Introdu detaliile rutei CFR: ")

    id = str(input("[id ruta CFR] : ") or "")

    source = input("[statie plecare] : ")
    destination = input("[statie sosire] : ")

    dep_hour = str(input("[ora plecare]: ") or "")
    dep_day = str(input("[ziua plecarii] : ") or "")
    duration = str(input("[durata ruta] : ") or "")
    nr_seats = str(100)
    price = str(input("[pretul calatoriei] : ") or "")
    clasa = str(input("[clasa calatoriei, ex: 1 sau 2] : ") or "")

    tiptren = input("[tipul trenului, ex: RI, IC, EN, EC, S, P, A, R] : ")

    return (id, source, destination, dep_hour,
            dep_day, duration, nr_seats, price, clasa, tiptren)

# Execute an insert query in database.
def insert_new_route():
    (id, source, destination, dep_hour, dep_day,
    duration, nr_seats, price, clasa, tiptren) = get_insert_input()
    query = insert_query(id, source, destination,
                dep_hour, dep_day, duration,
                nr_seats, price, clasa, tiptren)
    execute_query(query)

# Execute a delete query in database.
def delete_route():
    id = input("[id routa]: ")
    query = "delete from flights where id=" + str(id) + ";"
    execute_query(query)

# Print a welcome board when `admin` page is opened.
def print_welcome():
    print("\n\n")
    print("                        ______")
    print("                       / .===. /\/")
    print("                       \/ 6 6 \/")
    print("                       ( \___/ )")
    print("      _____________ooo__\_____/__________________")
    print("    //                                           /|")
    print("    |                Bine ai venit!               |")
    print("    |         ADMINISTRATIA CFR Calatori          |")
    print("    |                                             |")
    print("     /\___________________________ooo_____________//")
    print("                        |  |  |")
    print("                        |_ | _|")
    print("                        |  |  |")
    print("                        |__|__|")
    print("                        /-'Y'-|")
    print("                       (__/ \__)")

# Decide which operation has to be done depending on the
# given index.
def choose_operation(idx):
    option = int(idx)
    if option == 2:
        insert_new_route()
    elif option == 3:
        delete_route()
    elif option == 1:
        see_all()
    else:
        print("> > > > > > > > > > Iesire administrator CFR < < < < < < < < < < < ")
        exit()


if __name__ == '__main__':
    print_welcome()
    while 1:
        print("\nSelecteaza una din operatiile de mai jos:\n")
        print("- - - - - - - - #1 Vizualizeaza baza de date CFR - - - - - - -")
        print("- - - - - - - - #2 Adauga ruta CFR - - - - -  - - - - - - - - ")
        print("- - - - - - - - #3 Sterge ruta CFR - - - - - - - - - - - - - ")
        print("- - - - - - - - #4 Iesi din admin panel - - - - - - - - - - - ")
        index = input("Operatia: ")
        if (index.isnumeric() and (not 1 <= int(index) <= 4)) or (not index.isnumeric()):
            print("\n. . . . . . . Introdu alt index! . . . . . . . .\n ")
            continue
        choose_operation(index)
