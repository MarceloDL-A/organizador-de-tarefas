# models/task.py

from datetime import datetime


class Task:
    def __init__(self, title, is_done=False, date_created=None, date_modified=None, notes="", subtasks=None):
        self.title = title
        self.is_done = is_done
        self.date_created = date_created if date_created else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.date_modified = date_modified if date_modified else self.date_created
        self.notes = notes
        self.subtasks = subtasks if subtasks else []

    def to_dict(self):
        return {
            "title": self.title,
            "is_done": self.is_done,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "notes": self.notes,
            "subtasks": [subtask.to_dict() for subtask in self.subtasks]
        }

    @staticmethod
    def from_dict(data):
        subtasks = [Task.from_dict(subtask_data) for subtask_data in data.get("subtasks", [])]
        return Task(
            data["title"],
            data["is_done"],
            data["date_created"],
            data.get("date_modified", data["date_created"]),
            data.get("notes", ""),
            subtasks
        )

    def update_date_modified(self):
        self.date_modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
