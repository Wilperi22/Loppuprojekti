# Hotel Room Booking System

A command-line Python application for managing hotel rooms and bookings with an SQLite database.

## Project Goal

This project demonstrates a modular Python CRUD application with:
- room management
- booking management
- date and input validation
- persistent storage using SQLite

## Implemented Features

### Room management
- Add a new room
- View all rooms
- Modify room number, type, and price
- Delete a room

### Booking management
- Create a booking
- View all bookings
- Modify booking fields
- Cancel booking by booking ID

### Booking logic
- Prevent booking for a room that does not exist
- Prevent overlapping bookings for the same room
- Calculate total booking price from room price and number of nights

### Persistence
- Automatic database initialization on startup
- SQLite tables for rooms and bookings

## Project Structure

- [main.py](main.py): CLI menu, user interaction, input handling
- [data/database.py](data/database.py): Database schema and CRUD operations
- [data/hotel.db](data/hotel.db): SQLite database file
- [requirements.txt](requirements.txt): Python dependencies

## Requirements

- Python 3.10+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Menu Options

1. Modify rooms
2. Modify bookings
3. Add room
4. Book room
5. View bookings
6. View rooms
7. Cancel booking
8. Delete room
0. Exit

## Dependencies

- tabulate
