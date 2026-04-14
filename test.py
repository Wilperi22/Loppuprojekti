updates = {
            "ID":0,
            "new_name":1,
            "new_number":2,
            "new_check_in":3,
            "new_check_out":4,
            "new_total_price":5
            }
first_key = next(iter(updates))
query = f"UPDATE bookings SET {(", ".join(f"{k}=?" for k in updates.keys()))} WHERE ID=?"
print(query,(tuple(updates.values())+(updates["ID"],)))