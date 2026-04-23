import sqlite3
from datetime import datetime

def init_db():
    #Creating the database
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_number INTEGER PRIMARY KEY,
            room_type TEXT NOT NULL,
            price_per_night REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            room_number INTEGER,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            total_price REAL,
            FOREIGN KEY (room_number) REFERENCES rooms (room_number)
        )
    ''')    
    conn.commit()
    conn.close()

   


def to_datetime(date_text: str):
    return datetime.strptime(date_text, "%d-%m-%Y")


def add_room(number,r_type,price):
    #Adding rooms to Table rooms

    try:
        conn = sqlite3.connect("data/hotel.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rooms (room_number, room_type, price_per_night) VALUES (?,?,?)",
            (number,r_type,price)
        )
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Error room {number} dont exist")
        conn.close()
    finally:
        conn.close()


def modify_room(orginal_number, new_number=None, r_type=None, price=None):
    #Modifying rooms
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()
    try:
   
        if r_type != None:
            cursor.execute("""
                       UPDATE rooms
                       SET room_type=?
                       WHERE room_number=?""",
                       (r_type,orginal_number)
                       )
            conn.commit()
    
        if price != None:
      
            cursor.execute("""
                       UPDATE rooms
                       SET price_per_night=?
                       WHERE room_number=?
                       """,
                       (price,orginal_number))
            conn.commit()

      
        if new_number != None:
      
            cursor.execute("""
                       UPDATE rooms
                       SET room_number = ?
                       WHERE room_number = ?""",
                       (new_number,orginal_number,)
                       )    
            conn.commit()
    except sqlite3.KeyError as e:
            print(f"SQL error occurred: {e}")
            conn.close()
    
    conn.close()
   
    
def modify_bookings(ID,new_name=None,new_number=None,new_check_in=None,new_check_out=None,new_total_price=None):
        #Used for modifying bookings
        conn = sqlite3.connect("data/hotel.db")
        cursor = conn.cursor()

        updates = {
            "guest_name":new_name,
            "room_number":new_number,
            "check_in":new_check_in,
            "check_out":new_check_out,
            "total_price":new_total_price
            }
        #Clears updates if value = None deletes it.
        updates = {key: value for key, value in updates.items() if value is not None and value != ""}
        try:
            query = f"UPDATE bookings SET {(", ".join(f"{k}=?" for k in updates.keys()))} WHERE ID=?"
    
            cursor.execute(query,(tuple(updates.values())+(ID,)))
        except ValueError as e:
            print(f"Error: {e}")
            conn.close()
        conn.commit()
        conn.close()


def get_rooms():
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM rooms")
        data = cursor.fetchall()
    except sqlite3.KeyError as e:
        print(f"Error fetching rooms: {e}")
    finally:
        conn.close()
    return data

def get_bookings():
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    data1 = cursor.fetchall()
    conn.close()
    return data1                        

def total_price(number,check_in,check_out):
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()

    check_in = datetime.strptime(check_in,"%d-%m-%Y")
    check_out = datetime.strptime(check_out,"%d-%m-%Y")
    cursor.execute("""
    SELECT price_per_night
     FROM rooms
     WHERE room_number = ?
    """,
    (number,)             
    )

    row = cursor.fetchone()
    
    try:
        if not row:
            raise ValueError("Room does not exist")
    except ValueError as e:
        print(f"Error loading room {e}")
    finally:
        conn.close()    
    
    nights = (check_out-check_in).days
    price = nights*row[0]
    
    
    return price
    
def create_booking(name,number,check_in,check_out):
    conn =sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()

    check_in_dt = datetime.strptime(check_in,"%d-%m-%Y")
    check_out_dt = datetime.strptime(check_out,"%d-%m-%Y")
    
    check_in_db = check_in_dt.date().isoformat()
    check_out_db = check_out_dt.date().isoformat()

    pena =  cursor.execute("""
                   SELECT room_number
                   FROM rooms
                   """)
    if (number,) not in pena.fetchall():
        raise ValueError("Room not found!")
    
    try:
        if check_in_dt >= check_out_dt:
            raise ValueError("Check-out must be after check-in")


    except ValueError as e:
        conn.close()
        print(f"Error on check-in/check-out dates {e}")
        raise
        
        
    #Tarkistus onko päivälle jo varaus
    cursor.execute(
        """
        SELECT 1
        FROM bookings
        WHERE room_number = ?
            AND NOT (check_out <= ? OR check_in >= ? )
        LIMIT 1
    """,(number,check_in_db,check_out_db),
    )

    is_booked = cursor.fetchone() is not None
    is_free = not is_booked
  
    cursor.execute(
    "SELECT * FROM rooms WHERE room_number = ?",
    (number,)
    )

    if is_free:    
        try:
            cursor.execute("""
                INSERT INTO bookings (guest_name, room_number, check_in, check_out,total_price)
                VALUES (?,?,?,?,?)
                """,(name,number,check_in_db,check_out_db,total_price(number,check_in,check_out))
                ) 
            conn.commit()

            return
        
        except sqlite3.Error as e:
            print(f"{e} occured while trying to insert")
        finally:
            conn.close()
        
    conn.commit()
    conn.close()
    return

def delete_room(r_num:int):
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
        DELETE
        FROM rooms
        WHERE room_number = ?
            """,(r_num,))
        conn.commit()
    except (sqlite3.Error,ValueError) as e:
        print(f"{e}")
    finally:
        conn.close()

def cancel_booking(number:int):
    try:
        conn = sqlite3.connect("data/hotel.db")
        cursor = conn.cursor()

        cursor.execute("""
        DELETE
        FROM bookings
        WHERE id = ?               
        """,(number,))

        conn.commit()
        print("room cancelled succesfully")
    except:
        print("Error on canceling booking")
    finally:
        conn.close()
    


