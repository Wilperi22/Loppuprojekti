import sqlite3
from datetime import datetime
from pathlib import Path

from tabulate import tabulate

from data.database import (
    add_room,
    cancel_booking,
    create_booking,
    get_rooms,
    init_db,
    total_price,
)

DATE_FORMAT = "%d-%m-%Y"
DB_PATH = Path(__file__).with_name("data").joinpath("hotel.db")

def add_room_main():
    try: 
       r_number = int(input("Give room number:"))
       r_type = input("Give room type:")
       r_price = int(input("Give roomprice:"))
       
    except ValueError as e:
        print(f"An Error has ocuired: {e}")
        return 
    add_room(r_number,r_type.title(),r_price)
add_room_main()

def view_rooms_main():
    rows = get_rooms()
    print(tabulate(rows,
                   headers=["Room number","Room type","Price per night"],
                    tablefmt="grid"))
view_rooms_main()

def menu() -> None:
    print("Hotel Room Booking System")
    print("1. Add room:")
    print("3. View bookings")
    print("4. Book room")
    print("5. Cancel booking")
    print("0. Exit")


def main():
    init_db()

    mainions = {
        "1": add_room_main,
        "2": view_rooms_main,
        "3": view_bookings_main,
        "4": book_room_main, 
        "5": cancel_booking_main,
    }

    while True:
        try:
            menu()
            choice = input("Choose an option: ").strip()

            if choice == "0":
                print("Goodbye.")
                break
           
        except Exception as exc:
            print(f"An error occurred: {exc}")

