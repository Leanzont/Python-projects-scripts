class Student:
    def __init__(self, name, age, notes=None):
        self.name = name
        self.age = int(age)
        self.notes = notes if notes is not None else []
    def add_notes(self):
        print(f"Adding notes for {self.name}:")
        note1 = int(input("Note 1: "))
        note2 = int(input("Note 2: "))
        note3 = int(input("Note 3: "))
        self.notes = [note1, note2, note3]    # Now they're being saved
        print(f"Notes saved: {self.notes}")

    def average(self):
        if not self.notes:                    # If there are no notes, avoid dividing by 0
            return 0
        return sum(self.notes) / len(self.notes)
        
    def state(self):                          
        avg = self.average()
        if avg < 51:
            return "Failed"
        return "Approved"

    def summary(self):
        print(f"\nStudent : {self.name}")
        print(f"Age     : {self.age}")
        print(f"Notes   : {self.notes}")
        print(f"Average : {self.average():.1f}")
        print(f"State   : {self.state()}")

# dinamic list — here stored all created studends 

students = []

print("=" * 40)
print("      STUDENT MANAGEMENT SYSTEM")
print("=" * 40)

while True:
    print("\n1. Create student")
    print("2. Add notes to student")
    print("3. See average and state")
    print("0. Exit")
    choice = int(input("Select: "))
    if choice == 0:
        print("Goodbye!")
        break
    elif choice == 1:
        name = input("Student name: ")
        age  = input("Student age: ")
        new_student = Student(name, age)
        students.append(new_student)
        print(f"Student '{name}' created.")
        
    elif choice == 2:
        if not students:
            print("No students yet. Create one first.")
            continue
        for i, s in enumerate(students):      # enumerate index + object
            print(f"\t{i+1}. {s.name}")
        idx = int(input("Choose student: ")) - 1
        if 0 <= idx < len(students):
            students[idx].add_notes()
        else:
            print("Invalid option.")
            
    elif choice == 3:
        if not students:
            print("No students yet.")
            continue
        for i, s in enumerate(students):
            print(f"\t{i+1}. {s.name}")
        idx = int(input("Choose student: ")) - 1
        
        if 0 <= idx < len(students):
            students[idx].summary()
        else:
            print("Invalid option.")
