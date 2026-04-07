import sqlite3
from datetime import date,datetime

def init_db():
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_number INTEGER PRIMARY KEY,
            room_type TEXT NOT NULL,
            price_per_night REAL NOT NULL,
            is_avible INTEGER DEFAULT 1
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
    print("Database intialized succesfully!")

def add_room(number,r_type,price):

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
    finally:
        conn.close()

def get_rooms():
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    data = cursor.fetchall()
    conn.close()
    return data

def get_bookings():
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    data1 = cursor.fetchall()
    conn.close()
    return data1                        #jesaia söi pilttiä tuolla eturivissä

def total_price(check_in,check_out,number):
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT price_per_night FROM rooms WHERE room_number = ?""",
    (number,)             
    )
    row = cursor.fetchone()
    print(row,"row")
    if not row:
        print("Room does not exist")
        conn.close()
        return
    
    cursor.execute("""
       SELECT check_in,check_out FROM bookings WHERE check_in = ? AND check_out = ?            
    """,(check_in,check_out))
    
    dates = cursor.fetchone()

    print(dates,"dates")    

def create_booking(name,number,check_in,check_out):
    conn =sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()
    check_in_dt = datetime.strptime(check_in,"%Y-%m-%d")
    check_out_dt = datetime.strptime(check_out,"%Y-%m-%d")
    print("HAlooo")


    check_in_db = check_in_dt.date().isoformat()
    check_out_db = check_out_dt.date().isoformat()

    if check_in_dt >= check_out_dt:
        print("Check-out must be after check-in")
        return
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
    print(cursor.fetchone(),"FETSI")
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
                """,(name,number,check_in_db,check_out_db,50)
                ) 
            conn.commit()
            conn.close()
            return
        
        except sqlite3.Error as e:
            print(f"{e} occured while trying to insert")
            conn.close()
            return
    conn.commit()
    conn.close()
    return

def modify_booking():
    check = input("Enter what do you want to modify? 1:name, 2:number, 3:check in or 4:check out")
    check.strip(" ")
    conn = sqlite3.connect("data/hotel.db")
    cursor = conn.cursor()
    check = check[0]

    if check == "1":
        cursor.execute("""
        UPDATE bookings
        SET 
        """)

    

   
    
    cursor.execute("""
    UPDATE bookings
    SET name = ?, number = ?,check_in = ?, check_out = ?            
    """)

def cancel_booking(number:int):
    try:
        conn = sqlite3.connect("data/hotel.db")
        cursor = conn.cursor()

        cursor.execute("""
        DELETE
        FROM bookings
        WHERE room_number = ?               
        """,(number,))

        conn.commit()
        conn.close()
        print("room cancelled succesfully")
    except:
        print("Error on canceling booking")
print(create_booking("Jussi",5,"2020-03-10","2020-04-10"))
#"print(get_rooms())
print(get_bookings())