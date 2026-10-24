"""One-off script to seed the database with dummy student records for testing.
Run with: python seed_dummy_students.py
"""
import random
from datetime import date, timedelta

import database

FIRST_NAMES = [
    "Juan", "Maria", "Jose", "Ana", "Pedro", "Rosa", "Carlos", "Liza",
    "Miguel", "Carmen", "Antonio", "Elena", "Francisco", "Isabel", "Rafael",
    "Teresa", "Manuel", "Patricia", "Ricardo", "Angela", "Eduardo", "Sofia",
    "Fernando", "Beatriz", "Alberto", "Cristina", "Roberto", "Veronica",
    "Diego", "Monica", "Gabriel", "Andrea", "Luis", "Camille", "Vincent",
]
LAST_NAMES = [
    "Dela Cruz", "Santos", "Reyes", "Garcia", "Torres", "Mendoza", "Ramos",
    "Villanueva", "Bautista", "Aquino", "Castillo", "Flores", "Rivera",
    "Gonzales", "Del Rosario", "Fernandez", "Pascual", "Salazar", "Navarro",
    "Domingo", "Cruz", "Morales", "Ocampo", "Manalo", "Padilla",
]

PROFESSORS = ["Dr. Maria Santos", "Dr. Juan Dela Cruz", "Prof. Ana Reyes"]
PANELS = ["Dr. Roberto Garcia", "Dr. Liza Torres", "Prof. Carlos Mendoza"]
STATUS_OPTIONS = ["Pending", "Re-Defense", "Revise", "Hard Bound", "Re-present"]

# (course, subject) pairs, grouped by which Student List tab they should land in
SOFTWARE_ENGINEERING_GROUP = [
    ("BSCS", "Software Engineering Thesis 1"),
    ("BSIT", "Software Engineering Capstone"),
    ("BSCpE", "Software Engineering Project"),
]
CAPSTONE_GROUP = [
    ("BSCS", "Thesis Writing 1"),
    ("BSCS", "Thesis Writing 2"),
    ("BSIT", "Capstone Project 1"),
    ("BSIT", "Capstone Project 2"),
    ("BSCpE", "Undergraduate Thesis"),
]
MIT_MIS_GROUP = [
    ("MIT", "Graduate Thesis"),
    ("MIS", "Information Systems Research"),
]

used_emails = set()


def random_name():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}", first, last


def random_email(first, last):
    base = f"{first}.{last}".lower().replace(" ", "").replace("ñ", "n")
    email = f"{base}@example.com"
    n = 1
    while email in used_emails:
        n += 1
        email = f"{base}{n}@example.com"
    used_emails.add(email)
    return email


def random_date():
    start = date(2024, 1, 1)
    days = random.randint(0, 900)
    return (start + timedelta(days=days)).strftime("%Y-%m-%d")


def seed_group(group, count):
    created_ids = []
    for _ in range(count):
        course, subject = random.choice(group)
        name, first, last = random_name()
        email = random_email(first, last)
        professor = random.choice(PROFESSORS)
        advisor = random.choice(PROFESSORS)
        panel = random.choice(PANELS)
        chairman = random.choice(PANELS)
        active_status = "Active" if random.random() > 0.15 else "Inactive"

        student_id = database.create_student(
            name, email, course, subject, professor, advisor, panel, chairman,
            active_status, random_date(),
        )
        created_ids.append(student_id)
    return created_ids


def randomize_statuses(student_ids):
    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        for sid in student_ids:
            status = random.choice(STATUS_OPTIONS)
            cursor.execute("UPDATE progress SET status = %s WHERE student_id = %s", (status, sid))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def main():
    all_ids = []
    all_ids += seed_group(SOFTWARE_ENGINEERING_GROUP, 12)
    all_ids += seed_group(CAPSTONE_GROUP, 12)
    all_ids += seed_group(MIT_MIS_GROUP, 8)

    randomize_statuses(all_ids)

    print(f"Created {len(all_ids)} dummy students.")


if __name__ == "__main__":
    main()
