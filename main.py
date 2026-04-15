import sqlite3
from datetime import datetime
from pathlib import Path
import time
from tabulate import tabulate
from data.database import (
    add_room,
    cancel_booking,
    create_booking,
    get_rooms,
    get_bookings,
    init_db,
    total_price,
    modify_bookings,
    modify_room
)

DATE_FORMAT = "%d-%m-%Y"
DB_PATH = Path(__file__).with_name("data").joinpath("hotel.db")

def add_room_main():
    try: 
       r_number = int(input("Give room number:"))
       if r_number in get_rooms():
           raise ValueError("Room already exists.")
       r_type = input("Give room type:")
       r_price = int(input("Give roomprice:"))
       
    except ValueError as e:
        print(f"An Error has ocuired: {e}")
        return 
    add_room(r_number,r_type.title(),r_price)


def view_rooms_main():
    #rows = rooms.fetchall
    rows = get_rooms()
    print(tabulate(rows,
                   headers=["Room number","Room type","Price per night"],
                    tablefmt="grid"))




def view_bookings_main():
    rows = get_bookings()
    print(tabulate(rows,
                   headers=["Room number","Room type","Price per night"],
                    tablefmt="grid"))
    
def book_room_main():
    view_rooms_main()
    try:
        r_number = int(input("Give room number:"))
        if r_number not in get_rooms():
            print("Room does not exist.")
            return
        c_name = input("Give customer name:")
        c_date = input("Give booking date (dd-mm-yyyy):")
        datetime.strptime(c_date, DATE_FORMAT)
    except ValueError as e:
        print(f"An Error has ocuired: {e}")
        return 
    create_booking(r_number,c_name,c_date)

def cancel_booking_main():
        try:
            r_number = int(input("Give room number:"))
            cancel_booking(r_number)
        except ValueError as e:
            print(f"Error has occurred: {e}")

def modify_room_main():
    view_rooms_main()
    try:
        orginal_r_num = int(input("Give original room number:"))
        new_r_num = int(input("Give new room number(leave empty for no change):"))
        new_r_type = input("Give new room type(leave empty for no change):")
        new_r_price = input("Give new room price (leave empty for no change):")
        modify_room(orginal_r_num,new_r_num,new_r_type,new_r_price)
    except ValueError as e:
        print(f"Error has occurred: {e}")
def modify_bookings_main():
    view_bookings_main()
    try:
        id = int(input("Input booking ID:"))
        new_name = input("New name(leave empty for no change):")
        new_number = input("New room number(leave empty for no change):")
        new_check_in = input(f"New check in format {DATE_FORMAT} (leave empty for no change): ")
        new_check_out = input(f"New check out format {DATE_FORMAT}(leave empty for no change):")
        new_total_price = int(input("Input new total price(leave empty for no change):"))
        modify_bookings(id,new_name,new_number,new_check_in,new_check_out,new_total_price)

    except ValueError as e:
        print(f"Error occurred {e}")
    

def menu():
    print("Hotel Room Booking System")
    print("1. Mofify rooms:")
    print("2. Modify bookings:")
    print("3. Add room:")
    print("4. View rooms:")
    print("5. View bookings:")
    print("6. Book room:")
    print("7. Cancel booking:")
    print("0. Exit:")

def main():
    init_db()

    mainions = {
        "1":modify_room_main,
        "2":modify_bookings_main,
        "3": add_room_main,
        "4": view_rooms_main,
        "5": view_bookings_main,
        "6": book_room_main, 
        "7": cancel_booking_main,
    }

    while True:
        try:
            menu()
            choice = input("Choose an option: ").strip()

            if choice == "0":
                print("Goodbye.")
                break
            else:
                mainions[choice]()
                time.sleep(1)
            
           
        except Exception as exc:
            print(f"An error occurred: {exc}")
if __name__ == "__main__":
    main()

