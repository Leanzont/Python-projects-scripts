# Student Management System

A simple Python console application to manage students, their grades, and academic status.  
Built with OOP principles – each student is an instance of the `Student` class.

## Features

- Create a student with name and age
- Add three grades (notes) for a student
- Calculate the student’s average grade
- Determine approval status (pass if average ≥ 51, otherwise fail)
- Display a complete summary (name, age, grades, average, status)
- Interactive menu to repeat operations until exit

## Class Diagram

### `Student`

| Attribute | Type         | Description                         |
|-----------|--------------|-------------------------------------|
| `name`    | `str`        | Student’s name                      |
| `age`     | `int`        | Student’s age (converted to integer)|
| `notes`   | `list[int]`  | List of three grades (initially empty) |

| Method          | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `__init__`      | Constructor. Accepts `name`, `age`, and optional `notes` (default `[]`).    |
| `add_notes()`   | Prompts for three integer grades and stores them in `self.notes`.           |
| `average()`     | Returns the arithmetic mean of `notes`. Returns `0` if no notes exist.      |
| `state()`       | Returns `"Approved"` if `average() >= 51`, otherwise `"Failed"`.            |
| `summary()`     | Prints all student details (name, age, notes, average, state).              |

## Usage

Run the script in a Python 3 environment.

```bash
python student_management.py
```

### Main Menu

```
1. Create student
2. Add notes to student
3. See average and state
4. Exit
```

- **Option 1**: Enter name and age → student is added to the internal list.
- **Option 2**: Choose a student from the list → input three grades.
- **Option 3**: Choose a student → see their summary (including average and approval).
- **Option 0**: Exit the program.

## Code Walkthrough

### 1. Student Class

```python
class Student:
    def __init__(self, name, age, notes=None):
        self.name = name
        self.age = int(age)
        self.notes = notes if notes is not None else []
```

- `age` is explicitly converted to `int` to avoid type errors later.
- `notes` defaults to an empty list to prevent accidental sharing of mutable default arguments.

### 2. Adding Grades

```python
def add_notes(self):
    print(f"Adding notes for {self.name}:")
    note1 = int(input("Note 1: "))
    note2 = int(input("Note 2: "))
    note3 = int(input("Note 3: "))
    self.notes = [note1, note2, note3]
    print(f"Notes saved: {self.notes}")
```

> **Note**: This method overwrites any existing grades. It is designed for exactly three grades per student.

### 3. Average Calculation

```python
def average(self):
    if not self.notes:
        return 0
    return sum(self.notes) / len(self.notes)
```

### 4. Approval Status

```python
def state(self):
    avg = self.average()
    if avg < 51:
        return "Failed"
    return "Approved"
```

### 5. Summary Output

```python
def summary(self):
    print(f"\nStudent : {self.name}")
    print(f"Age     : {self.age}")
    print(f"Notes   : {self.notes}")
    print(f"Average : {self.average():.1f}")
    print(f"State   : {self.state()}")
```

### 6. Interactive Menu

- A `while True` loop presents the menu.
- Students are stored in a dynamic list `students = []`.
- Options 2 and 3 use `enumerate()` to display a numbered list of existing students.
- Input validation ensures a valid index is chosen.
