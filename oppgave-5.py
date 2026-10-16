# Oppgave 5 - Miniprosjekt: aktivitetsplanlegger
from datetime import datetime


class Activity:
    """One activity in the planner.

    Attributes:
        title (str): The name of the activity.
        category (str): The category, for example "study".
        date (datetime.date): The date of the activity.
        estimated_minutes (int): The estimated time in minutes.
        status (str): Either "planned" or "completed".
    """

    def __init__(self, title, category, date, estimated_minutes, status="planned"):
        self.title = title
        self.category = category
        self.date = date
        self.estimated_minutes = estimated_minutes
        self.status = status

    def describe(self):
        """Return the activity as one line of text."""
        date_text = self.date.strftime("%d.%m.%Y")
        return (f"{self.title} ({self.category}), {date_text}, "
                f"{self.estimated_minutes} min, {self.status}")

    def mark_completed(self):
        """Change the status of the activity to "completed"."""
        self.status = "completed"


def print_error(message, prefix="Error: "):
    """Print an error message in the terminal."""
    print(f"{prefix}{message}")


def get_valid_text(prompt, name):
    """Ask the user for text until it is not empty.

    Parameters:
        prompt (str): The question shown to the user.
        name (str): What the text is, used in the error message.

    Returns:
        str: The text without spaces at the start and end.
    """
    text = ""
    valid = False

    while not valid:
        text = input(prompt).strip()

        if text == "":
            print_error(f"The {name} cannot be empty. Try again.")
        else:
            valid = True

    return text


def get_valid_date(prompt):
    """Ask the user for a date until it is valid.

    Parameters:
        prompt (str): The question shown to the user.

    Returns:
        datetime.date: The date the user entered (format dd.mm.yyyy).
    """
    date = None
    valid = False

    while not valid:
        text = input(prompt).strip()

        if len(text) != 10:
            print_error("Invalid date. Use exactly the format dd.mm.yyyy, "
                        "for example 05.03.2026.")
        else:
            try:
                date = datetime.strptime(text, "%d.%m.%Y").date()
            except ValueError:
                print_error("Invalid date. Use the format dd.mm.yyyy "
                            "and a date that exists.")
            else:
                valid = True

    return date


def get_positive_integer(prompt, name="number"):
    """Ask the user for a positive whole number until it is valid.

    Parameters:
        prompt (str): The question shown to the user.
        name (str): What the number is, used in the error message.

    Returns:
        int: The number the user entered (1 or higher).
    """
    number = 0
    valid = False

    while not valid:
        text = input(prompt).strip()

        try:
            number = int(text)
        except ValueError:
            print_error(f"The {name} must be a whole number, for example 45.")
        else:
            if number <= 0:
                print_error(f"The {name} must be a positive whole number.")
            else:
                valid = True

    return number


def get_valid_status(prompt):
    """Ask the user for a status until it is "planned" or "completed".

    Parameters:
        prompt (str): The question shown to the user.

    Returns:
        str: Either "planned" or "completed".
    """
    status = ""
    valid = False

    while not valid:
        status = input(prompt).strip().lower()

        if status == "planned" or status == "completed":
            valid = True
        else:
            print_error("The status must be 'planned' or 'completed'.")

    return status


def register_activity(activities):
    """Ask the user for the details of a new activity and add it to the list.

    Parameters:
        activities (list): The list of Activity objects to add to.
    """
    title = get_valid_text("Title: ", "title")
    category = get_valid_text("Category: ", "category").lower()
    date = get_valid_date("Date (dd.mm.yyyy): ")
    minutes = get_positive_integer("Estimated minutes: ", "estimated time")

    activities.append(Activity(title, category, date, minutes))
    print(f"Registered: {title}")


def show_activities(activities):
    """Print a numbered list of activities, or a message if there are none.

    Parameters:
        activities (list): The Activity objects to show.
    """
    if len(activities) == 0:
        print("There are no activities to show.")
    else:
        number = 1

        for activity in activities:
            print(f"{number}. {activity.describe()}")
            number += 1


def find_activities(activities, search_text):
    """Find the activities where the title or category contains the text.

    Parameters:
        activities (list): The Activity objects to search in.
        search_text (str): The text to look for (upper or lower case).

    Returns:
        list: A new list with the matching activities.
    """
    search_text = search_text.lower()
    matches = []

    for activity in activities:
        if search_text in activity.title.lower() or search_text in activity.category:
            matches.append(activity)

    return matches


def filter_by_status(activities, status):
    """Find the activities that have the given status.

    Parameters:
        activities (list): The Activity objects to filter.
        status (str): Either "planned" or "completed".

    Returns:
        list: A new list with the activities that have that status.
    """
    matches = []

    for activity in activities:
        if activity.status == status:
            matches.append(activity)

    return matches


def search_activities(activities):
    """Ask for a search text and show the matching activities."""
    search_text = get_valid_text("Search for title or category: ", "search text")
    matches = find_activities(activities, search_text)

    if len(matches) == 0:
        print(f"No activities match '{search_text}'.")
    else:
        show_activities(matches)


def show_by_status(activities):
    """Ask for a status and show the activities that have it."""
    status = get_valid_status("Status (planned/completed): ")
    matches = filter_by_status(activities, status)

    if len(matches) == 0:
        print(f"No activities have the status '{status}'.")
    else:
        show_activities(matches)


def show_menu():
    """Print the menu."""
    print()
    print("=== Aktivitetsplanlegger ===")
    print("1. Registrere og vise aktiviteter")
    print("2. Søke etter tittel eller kategori")
    print("3. Filtrere etter status")
    print("4. Sortere etter dato eller varighet")
    print("5. Markere en aktivitet som fullført")
    print("6. Vise antall, samlet estimert tid og antall fullførte")
    print("7. Lagre til fil og lese inn igjen")
    print("8. Avslutte programmet")


def run_menu():
    """Show the menu again and again until the user chooses to quit."""
    activities = []
    running = True

    while running:
        show_menu()
        choice = input("Choose (1-8): ").strip()

        if choice == "1":
            register_activity(activities)
            show_activities(activities)
        elif choice == "2":
            search_activities(activities)
        elif choice == "3":
            show_by_status(activities)
        elif choice in ("4", "5", "6", "7"):
            print("This option is not ready yet.")
        elif choice == "8":
            print("Goodbye!")
            running = False
        else:
            print_error("Invalid choice. Enter a number from 1 to 8.")


run_menu()