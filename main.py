import json
import os

# File paths
users_file = 'users.json'
movies_file = 'movies.json'

# Ensure initial files exist
if not os.path.exists(users_file):
    with open(users_file, 'w') as file:
        json.dump({}, file)

if not os.path.exists(movies_file):
    with open(movies_file, 'w') as file:
        json.dump({}, file)

def load_data(filename):
    """Load data from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def sign_up():
    """Prompt user for sign-up and register them."""
    username = input("Enter your username to sign up: ")
    users = load_data(users_file)
    if username in users:
        print("Username already exists.")
        return
    users[username] = {"movies_watched": []}
    save_data(users_file, users)
    print("User registered successfully.")

def login():
    """Prompt user for login and validate."""
    username = input("Enter your username to log in: ")
    users = load_data(users_file)
    if username in users:
        print("Login successful.")
        return username
    else:
        print("User not found.")
        return None

def book_ticket(username):
    """Prompt user to book a ticket."""
    movie_id = input("Enter the movie ID you want to book a ticket for: ")
    seat_number = input("Enter the seat number you want to book: ")
    users = load_data(users_file)
    movies = load_data(movies_file)
    
    if movie_id not in movies or username not in users:
        print("Movie not found or user not registered.")
        return
    
    if seat_number in movies[movie_id]["seats_taken"]:
        print("Seat already booked.")
        return
    
    movies[movie_id]["seats_taken"].append(seat_number)
    users[username]["movies_watched"].append({"movie_id": movie_id, "seat": seat_number})
    
    save_data(movies_file, movies)
    save_data(users_file, users)
    print(f"Ticket booked successfully for seat {seat_number}.")

def show_available_movies():
    """Display all movies and their available seats."""
    movies = load_data(movies_file)
    for movie_id, details in movies.items():
        available_seats = [seat for seat in details["total_seats"] if seat not in details["seats_taken"]]
        print(f"Movie ID: {movie_id}, Available Seats: {available_seats}")

def add_movie():
    """Prompt user to add a new movie."""
    movie_id = input("Enter a new movie ID: ")
    total_seats_input = input("Enter total seats separated by a comma (e.g., A1,A2,A3): ")
    total_seats = total_seats_input.split(",")
    movies = load_data(movies_file)
    if movie_id in movies:
        print("Movie already exists.")
        return
    movies[movie_id] = {"total_seats": total_seats, "seats_taken": []}
    save_data(movies_file, movies)
    print("Movie added successfully.")

def main():
    while True:
        print("\nMovie Ticketing System")
        print("1. Sign Up")
        print("2. Log In")
        print("3. View Available Movies")
        print("4. Add Movie (Admin)")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            username = login()
            if username:
                while True:
                    print("\n1. Book a Ticket")
                    print("2. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        book_ticket(username)
                    elif user_choice == "2":
                        break
        elif choice == "3":
            show_available_movies()
        elif choice == "4":
            add_movie()
        elif choice == "0":
            print("Thank you for using the Movie Ticketing System.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
