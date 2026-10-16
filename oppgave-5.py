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


reading = Activity("Read chapter 5", "study", datetime(2026, 10, 20).date(), 45)
walk = Activity("Evening walk", "health", datetime(2026, 10, 18).date(), 30)

print(reading.describe())
print(walk.describe())

reading.mark_completed()
print(reading.describe())
print(walk.describe())