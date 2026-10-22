"""
Sample Data Generator for SRM Institute of Science and Technology, Tiruchirappalli
"""
from database.database import Database
from models.student import Student
from models.subject import Subject
from models.faculty import Faculty
from models.room import Room
from models.timeslot import TimeSlot


def populate_srm_sample_data(db: Database):
    """Resets and populates the database with realistic SRM IST Tiruchirappalli examination data."""
    db.reset_database()

    # 1. Subjects
    subjects = [
        Subject("CS301", "Data Structures and Algorithms", "Computer Science", 3, 180),
        Subject("CS302", "Operating Systems", "Computer Science", 3, 180),
        Subject("CS303", "Database Management Systems", "Computer Science", 3, 180),
        Subject("MA301", "Discrete Mathematics", "Mathematics", 3, 180),
        Subject("IT301", "Web Technologies", "Information Technology", 3, 180),
        Subject("EC301", "Digital Electronics", "Electronics & Communication", 3, 180),
    ]
    for sub in subjects:
        db.create_subject(sub)

    # 2. Students & Enrollments
    # 35 CSE Students enrolled in CS301, CS302, CS303, MA301
    cse_students = [
        Student(f"RA23110030100{i:02d}", f"CSE Student {i:02d}", "Computer Science", 3, ["CS301", "CS302", "CS303", "MA301"])
        for i in range(1, 36)
    ]
    for stu in cse_students:
        db.create_student(stu)

    # 25 IT Students enrolled in IT301, CS303, MA301
    it_students = [
        Student(f"RA23110030200{i:02d}", f"IT Student {i:02d}", "Information Technology", 3, ["IT301", "CS303", "MA301"])
        for i in range(1, 26)
    ]
    for stu in it_students:
        db.create_student(stu)

    # 20 ECE Students enrolled in EC301
    ece_students = [
        Student(f"RA23110030300{i:02d}", f"ECE Student {i:02d}", "Electronics & Communication", 3, ["EC301"])
        for i in range(1, 21)
    ]
    for stu in ece_students:
        db.create_student(stu)

    # 3. Faculty
    faculty_list = [
        Faculty("FAC01", "Dr. Ramanathan K", "Computer Science", is_available=True),
        Faculty("FAC02", "Dr. Priya Sharma", "Computer Science", is_available=True),
        Faculty("FAC03", "Prof. Anand Babu", "Information Technology", is_available=True),
        Faculty("FAC04", "Prof. Meenakshi S", "Mathematics", is_available=True),
        Faculty("FAC05", "Dr. Suresh Kumar", "Electronics & Communication", is_available=True),
        Faculty("FAC06", "Dr. Karthik V", "Computer Science", is_available=False),  # Unavailable faculty
    ]
    for fac in faculty_list:
        db.create_faculty(fac)

    # 4. Rooms
    rooms = [
        Room("RM-AUDI", "Main Auditorium Hall A", capacity=120, is_available=True),
        Room("RM-LH101", "Lecture Hall 101", capacity=65, is_available=True),
        Room("RM-LH102", "Lecture Hall 102", capacity=50, is_available=True),
        Room("RM-LH103", "Lecture Hall 103", capacity=35, is_available=True),
        Room("RM-SEM", "Seminar Hall Block B", capacity=40, is_available=True),
        Room("RM-CONF", "Conference Room 201", capacity=15, is_available=True),
        Room("RM-REPAIR", "Drawing Hall C (Under Renovation)", capacity=70, is_available=False),  # Unavailable room
    ]
    for rm in rooms:
        db.create_room(rm)

    # 5. Time Slots
    timeslots = [
        TimeSlot("TS01", "2026-10-10", "09:30", "12:30", is_available=True),
        TimeSlot("TS02", "2026-10-10", "13:30", "16:30", is_available=True),
        TimeSlot("TS03", "2026-10-11", "09:30", "12:30", is_available=True),
        TimeSlot("TS04", "2026-10-11", "13:30", "16:30", is_available=True),
        TimeSlot("TS05", "2026-10-12", "09:30", "12:30", is_available=True),
        TimeSlot("TS06", "2026-10-12", "13:30", "16:30", is_available=False),  # Unavailable slot
    ]
    for ts in timeslots:
        db.create_timeslot(ts)

    return {
        "subjects": len(subjects),
        "students": len(cse_students) + len(it_students) + len(ece_students),
        "faculty": len(faculty_list),
        "rooms": len(rooms),
        "timeslots": len(timeslots),
    }
