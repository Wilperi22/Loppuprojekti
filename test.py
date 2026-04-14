from data.database import (
    add_room,
    cancel_booking,
    create_booking,
    get_rooms,
    get_bookings,
    init_db,
    total_price,
)
huoneet = get_rooms()
print(huoneet[0][0])  