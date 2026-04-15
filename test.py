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

new_total_price = input("Input new total price(leave empty for no change):")
if new_total_price == "":
    new_total_price == None
print(float(new_total_price))

