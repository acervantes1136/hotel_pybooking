"""
-----------------------------------------------------------------------
ASSIGNMENT Mid-Project Audit: HOTEL BOOKING
-----------------------------------------------------------------------
[ ] 1. Ask the user for their age
[ ] 2. Ask how many people are staying and for how long (# of nights)
[ ] 3. Asks the user for personal information (First&Last name, Email, and Phone Number
[ ] 4. Asks the user if they have read the cancellation policy/understand it
[ ] 5. The program should have two different messages for user age and understanding policy (Yes & No)
-----------------------------------------------------------------------
"""

AGE = 21
HOTEL_BOOKING = "hotel_bookings.txt"


class HotelBooking:
    """Represents a hotel booking"""

    def __init__(self):
        self.age = 0
        self.guests = 0
        self.nights = 0
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.understands_policy = "No"

    # Individual Setters
    def set_age(self, age):
        self.age = age

    def set_guests(self, guests):
        self.guests = guests

    def set_nights(self, nights):
        self.nights = nights

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_email(self, email):
        self.email = email

    def set_phone(self, phone):
        self.phone = phone

    def set_policy_confirmation(self, confirmation):
        self.understands_policy = confirmation


def get_positive_number(prompt):
    """Prompts the user for input and ensures a positive whole number is entered.

    Parameters:
        prompt (str): The message displayed to the user.

    Returns:
        int: A validated positive integer."""
    # Makes sure user enters a positive whole number
    while True:
        value = input(prompt)
        if value.isdigit() and int(value) > 0:
            return int(value)
        else:
            print("ERROR: Please enter a valid positive number.\n")


def get_yes_no(prompt):
    """Prompts the user for a Yes/No response and validates the input.

    Parameters:
        prompt (str): The message displayed to the user.

    Returns:
        str: 'yes' or 'no' (validated lowercase response)."""
    # Makes sure the user is responding with a Yes/No
    while True:
        response = input(prompt).strip().lower()
        if response in ["yes", "no"]:
            return response
        else:
            print("ERROR: Please enter Yes or No.\n")


# Collecting the Users inputs
def main():
    """Main controller function (Conductor).

    Coordinates the hotel booking process:
    - Collects age and verifies eligibility
    - Collects booking details
    - Collects personal information
    - Confirms cancellation policy
    - Saves booking to file
    - Displays a formatted booking summary"""

    print("===================================")
    print("        HOTEL BOOKING SYSTEM       ")
    print("===================================\n")

    # Checks users age
    age = get_positive_number("Please enter your age: ")
    # Ends loop if user is not 21 and older
    if age < 21:
        print("\nSorry, you must be 21 or older to book a room.")
        return
    else:
        print("\nGreat! You meet the age requirement.")

    # Receiving more information from user
    guests = get_positive_number("\nHow many people are staying? ")
    nights = get_positive_number("How many nights are you staying? ")

    # Asks for users personal inputs as points of contact
    print("\n--- Personal Information ---")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone Number: ").strip()

    # Cancellation Policy
    cancel_policy = get_yes_no(
        "\nHave you read and understood our Cancellation Policy? (Yes/No): "
    )

    if cancel_policy == "yes":
        understands_policy = "Yes"
        print("\nThank you for confirming that you understand the policy.")
    else:
        understands_policy = "No"
        print(
            "\nIMPORTANT: You must cancel 72 hours before check-in "
            "or you will be charged for the first night."
        )

    # Saving the Booking to File
    raw_data_log = (
        f"Age: {age}\n"
        f"Nights: {nights}\n"
        f"First Name: {first_name}\n"
        f"Last Name: {last_name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Total Guests: {guests}\n"
        f"Understands Cancellation Policy: {understands_policy}\n"
        f"{'-'*40}\n"
    )

    try:
        with open("hotel_bookings.txt", "a") as file:
            file.write(raw_data_log)
    except Exception as e:
        print("ERROR: Could not save booking to file.")
        print(e)
        return

    # Booking Summary Formatted
    print("\n===================================")
    print("           BOOKING SUMMARY         ")
    print("===================================\n")

    print(f"{'Age:':<30}{age}")
    print(f"{'Nights:':<30}{nights}")
    print(f"{'Guest Name:':<30}{first_name} {last_name}")
    print(f"{'Email:':<30}{email}")
    print(f"{'Phone:':<30}{phone}")
    print(f"{'Total Guests:':<30}{guests}")
    print(f"{'Understands Policy:':<30}{understands_policy}")

    print("\nThank you for booking with us! We look forward to your stay.")
    print("\n(Booking has been saved to hotel_bookings.txt)")


# Program Entry Point
main()
