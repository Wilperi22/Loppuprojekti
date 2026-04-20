import sqlite3
from datetime import datetime
from pathlib import Path
import time
from tabulate import tabulate
from data.database import (
    add_room,
    delete_room,
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
       if (r_number,) in get_rooms() or r_number < 0:
           raise ValueError("Room already exists.")
       
       r_type = input("Give room type:")
       if r_type.strip() == "":
           raise ValueError("Room type cannot be empty")
       r_price = int(input("Give roomprice:"))
       if r_price < 1:
           raise ValueError("Room price cannot be under 1")
       
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
                   headers=["ID","Name","Room number","check-in","check-out","Total price"
                   ""],
                    tablefmt="grid"))
    
    
def book_room_main():
    view_rooms_main()
    try:
        r_number = int(input("Give room number:"))
        if (r_number,) not in [(room[0],) for room in get_rooms()]:
            raise ValueError("Room not found")
        exists = any(item[0] == r_number for item in get_bookings())
        if exists == False:
            raise ValueError("Room not")
        c_name = input("Give customer name:")
        c_check_in = input("Give check in date (dd-mm-yyyy):")
        c_check_out = input("Give check out date (dd-mm-yyyy):")

        datetime.strptime(c_check_in, DATE_FORMAT)
        datetime.strptime(c_check_out,DATE_FORMAT)
    except ValueError as e:
        print(f"An Error has ocuired: {e}")
        return 
    create_booking(c_name,r_number,c_check_in,c_check_out)
    print("Booking created succesfully")

def cancel_booking_main():
        view_bookings_main()
        try:
            r_number = int(input("Give booking id:"))
            exists = any(item[0] == r_number for item in get_bookings())

            if exists == False:
                raise ValueError("Room id not found")
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
    view_rooms_main()


def modify_bookings_main():
    view_bookings_main()
    try:
        id = int(input("Input booking ID:"))
        new_name = input("New name(leave empty for no change):")
        new_number = input("New room number(leave empty for no change):")
        new_check_in = input(f"New check in format {DATE_FORMAT} (leave empty for no change): ")
        new_check_out = input(f"New check out format {DATE_FORMAT}(leave empty for no change):")

        new_total_price = input("Input new total price(leave empty for no change):")
        if new_total_price == "":
            new_total_price = None
        else:
            new_total_price = float(new_total_price)
        

        modify_bookings(id,new_name,new_number,new_check_in,new_check_out,new_total_price)

    except ValueError as e:
        print(f"Error occurred {e}")
        return
    view_bookings_main()
    
def delete_room_main():
    view_rooms_main()
    try:
        r_num = int(input("Input room number:"))
        exists = any(item[0] == r_num for item in get_rooms())
        if exists == False:
            raise ValueError("Room number not found")
        delete_room(r_num)
    except ValueError as e:
        print(f"Error on deleting room {e}")
        return
    view_rooms_main()
    

def menu():
    print("Hotel Room Booking System")
    print("1. Modify rooms:")
    print("2. Modify bookings:")
    print("3. Add room:")
    print("4. Book room:")
    print("5. View bookings:")
    print("6. View rooms:")
    print("7. Cancel booking:")
    print("8. Delete room:")
    print("0. Exit:")

def main():
    init_db()

    mainions = {
        "1":modify_room_main,
        "2":modify_bookings_main,
        "3": add_room_main,
        "4": book_room_main,
        "5": view_bookings_main,
        "6": view_rooms_main, 
        "7": cancel_booking_main,
        "8": delete_room_main
    }

    while True:
        try:
            menu()
            choice = input("Choose an option: ").strip()

            if choice == "0":
                print("Goodbye.")
                break
            elif choice == "" or choice == " ":
                continue
            else:
                mainions[choice]()
                time.sleep(1)
            
           
        except Exception as exc:
            print(f"An error occurred: {exc}")
if __name__ == "__main__":
    main()

