from tabulate import tabulate
from data.database import (
    add_room,
    cancel_booking,
    create_booking,
    get_rooms,
    get_bookings,
    init_db,
    total_price,
    modify_bookings
)
def view_bookings_main():
    rows = get_bookings()
    print(tabulate(rows,
                   headers=["ID","Name","Room number","check-in","check-out","Total price"
                   ""],
                    tablefmt="grid"))
exists = any(item[0] == 3 for item in get_rooms())
print(exists)
