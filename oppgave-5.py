# Oppgave 5 - Miniprosjekt: aktivitetsplanlegger
import csv
from datetime import datetime
from pathlib import Path

DATE_FORMAT = "%d.%m.%Y"
FIELDNAMES = ["title", "category", "date", "estimated_minutes", "status"]


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
        date_text = self.date.strftime(DATE_FORMAT)
        return (f"{self.title} ({self.category}), {date_text}, "
                f"{self.estimated_minutes} min, {self.status}")

    def to_row(self):
        """Return the activity as a dictionary that can be written to a CSV file."""
        return {
            "title": self.title,
            "category": self.category,
            "date": self.date.strftime(DATE_FORMAT),
            "estimated_minutes": self.estimated_minutes,
            "status": self.status,
        }

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
                date = datetime.strptime(text, DATE_FORMAT).date()
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


def get_valid_option(prompt, options, hint):
    """Ask the user for one of the allowed words until the answer is valid.

    Parameters:
        prompt (str): The question shown to the user.
        options (tuple): The allowed answers, in lower case.
        hint (str): The allowed answers as text, used in the error message.

    Returns:
        str: The answer in lower case, one of the options.
    """
    answer = ""
    valid = False

    while not valid:
        answer = input(prompt).strip().lower()

        if answer in options:
            valid = True
        else:
            print_error(f"Invalid answer. Enter {hint}.")

    return answer


def get_number_in_range(prompt, highest):
    """Ask the user for a whole number from 1 to highest until it is valid.

    Parameters:
        prompt (str): The question shown to the user.
        highest (int): The highest allowed number.

    Returns:
        int: The number the user entered.
    """
    number = 0
    valid = False

    while not valid:
        text = input(prompt).strip()

        try:
            number = int(text)
        except ValueError:
            print_error("Enter a whole number from the list.")
        else:
            if number < 1 or number > highest:
                print_error(f"The number must be between 1 and {highest}.")
            else:
                valid = True

    return number


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


def get_date(activity):
    """Return the date of an activity (used as the sort key)."""
    return activity.date


def get_minutes(activity):
    """Return the estimated minutes of an activity (used as the sort key)."""
    return activity.estimated_minutes


def sort_activities(activities, sort_by):
    """Sort the activities by date (earliest first) or duration (longest first).

    Parameters:
        activities (list): The Activity objects to sort.
        sort_by (str): Either "date" or "duration".

    Returns:
        list: A new sorted list. The original list keeps its order.
    """
    if sort_by == "date":
        return sorted(activities, key=get_date)

    return sorted(activities, key=get_minutes, reverse=True)


def calculate_statistics(activities):
    """Calculate the number of activities, the total time and the completed count.

    Parameters:
        activities (list): The Activity objects to count.

    Returns:
        tuple: The number of activities (int), the total estimated minutes (int)
        and the number of completed activities (int).
    """
    total_minutes = 0
    completed_count = 0

    for activity in activities:
        total_minutes += activity.estimated_minutes

        if activity.status == "completed":
            completed_count += 1

    return len(activities), total_minutes, completed_count


def find_row_problem(row):
    """Check one row from the data file and describe the first problem found.

    Parameters:
        row (dict): One row from the CSV file (all values are text).

    Returns:
        str: A short description of the problem, or "" if the row is valid.
    """
    for field in FIELDNAMES:
        if row[field].strip() == "":
            return f"missing value in '{field}'"

    date_text = row["date"].strip()

    if len(date_text) != 10:
        return f"date '{date_text}' must have the format dd.mm.yyyy"

    try:
        datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        return f"date '{date_text}' is not a real date in the format dd.mm.yyyy"

    try:
        minutes = int(row["estimated_minutes"])
    except ValueError:
        return f"estimated_minutes '{row['estimated_minutes']}' is not a whole number"

    if minutes <= 0:
        return f"estimated_minutes '{row['estimated_minutes']}' must be positive"

    status = row["status"].strip().lower()

    if status != "planned" and status != "completed":
        return f"status '{row['status']}' must be 'planned' or 'completed'"

    return ""


def save_activities(path, activities):
    """Write the activities to a CSV file (created or overwritten).

    Parameters:
        path (pathlib.Path): The path to the data file.
        activities (list): The Activity objects to save.

    Returns:
        bool: True if the file was written, False if an error happened.
    """
    saved = False

    try:
        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

            for activity in activities:
                writer.writerow(activity.to_row())

        saved = True
    except PermissionError:
        print_error(f"No permission to write the file {path}")
    except FileNotFoundError:
        print_error(f"The folder for {path} does not exist")

    return saved


def load_activities(path):
    """Read the activities from a CSV file.

    Rows with problems are skipped, and a message with the line number and
    the problem is printed. If the file does not exist, a message is printed
    and the result is an empty list.

    Parameters:
        path (pathlib.Path): The path to the data file.

    Returns:
        list: The valid rows as Activity objects.
    """
    activities = []

    try:
        with open(path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file, restval="")

            if reader.fieldnames != FIELDNAMES:
                print_error(f"The file {path.name} does not have the expected columns: "
                            f"{FIELDNAMES}")
            else:
                for row in reader:
                    problem = find_row_problem(row)

                    if problem == "":
                        activities.append(Activity(
                            row["title"].strip(),
                            row["category"].strip().lower(),
                            datetime.strptime(row["date"].strip(), DATE_FORMAT).date(),
                            int(row["estimated_minutes"]),
                            row["status"].strip().lower(),
                        ))
                    else:
                        print(f"Skipped line {reader.line_num}: {problem}")
    except FileNotFoundError:
        print(f"No saved file found ({path.name}). Starting with an empty list.")
    except PermissionError:
        print_error(f"No permission to read the file {path}")

    return activities


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
    status = get_valid_option("Status (planned/completed): ",
                              ("planned", "completed"), "'planned' or 'completed'")
    matches = filter_by_status(activities, status)

    if len(matches) == 0:
        print(f"No activities have the status '{status}'.")
    else:
        show_activities(matches)


def show_sorted(activities):
    """Ask how to sort and show all activities in that order."""
    if len(activities) == 0:
        print("There are no activities to sort.")
    else:
        sort_by = get_valid_option("Sort by (date/duration): ",
                                   ("date", "duration"), "'date' or 'duration'")
        show_activities(sort_activities(activities, sort_by))


def complete_activity(activities):
    """Let the user choose a planned activity and mark it as completed."""
    planned = filter_by_status(activities, "planned")

    if len(planned) == 0:
        print("There are no planned activities to complete.")
    else:
        show_activities(planned)
        number = get_number_in_range("Number of the activity to complete: ",
                                     len(planned))
        planned[number - 1].mark_completed()
        print(f"Marked as completed: {planned[number - 1].title}")


def show_statistics(activities):
    """Show the number of activities, the total time and the completed count."""
    count, total_minutes, completed_count = calculate_statistics(activities)

    print(f"Number of activities: {count}")
    print(f"Total estimated time: {total_minutes} min")
    print(f"Completed activities: {completed_count}")


def save_or_load(activities, path):
    """Ask whether to save or load, and do it.

    Parameters:
        activities (list): The current Activity objects.
        path (pathlib.Path): The path to the data file.

    Returns:
        list: The activities to continue with. The current list if the user
        saved, or the list read from the file if the user loaded.
    """
    action = get_valid_option("Save or load (save/load): ",
                              ("save", "load"), "'save' or 'load'")

    if action == "save":
        if save_activities(path, activities):
            print(f"Saved {len(activities)} activities to {path.name}.")
    else:
        activities = load_activities(path)
        print(f"Loaded {len(activities)} activities from {path.name}.")

    return activities


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


def run_menu(data_path):
    """Show the menu again and again until the user chooses to quit.

    Parameters:
        data_path (pathlib.Path): The path to the data file, read at the start.
    """
    activities = load_activities(data_path)
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
        elif choice == "4":
            show_sorted(activities)
        elif choice == "5":
            complete_activity(activities)
        elif choice == "6":
            show_statistics(activities)
        elif choice == "7":
            activities = save_or_load(activities, data_path)
        elif choice == "8":
            print("Goodbye!")
            running = False
        else:
            print_error("Invalid choice. Enter a number from 1 to 8.")


data_path = Path(__file__).parent / "activities.csv"
run_menu(data_path)