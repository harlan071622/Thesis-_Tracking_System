import mysql.connector
import bcrypt

COURSE_OPTIONS = []
SUBJECT_OPTIONS = []
PROFESSOR_OPTIONS = []
ADVISOR_OPTIONS = []
PANEL_OPTIONS = []
CHAIRMAN_OPTIONS = []
THESIS_ACTIVE_STATUS_OPTIONS = ["Active", "Inactive"]

def get_connection():
   return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "thesis_db"
   )

def create_user(email, role, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, role, password_hash) VALUES (%s, %s, %s)",
            (email, role, password_hash)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def validate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False

    stored_hash = result[0]
    if stored_hash is None:
        return False

    return bcrypt.checkpw(password.encode(), stored_hash.encode())
def get_all_students_with_status():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "thesis_db"
    )
    cursor = conn.cursor()

    query = """
        SELECT
            s.id, s.name, s.email, s.course, s.subject, s.professor,
            s.advisor, s.panel, s.chairman,
            COALESCE(p.status, 'N/A') AS status,
            COALESCE(s.active_status, 'Active') AS active_status,
            (
                SELECT COUNT(*)
                FROM status_change_history
                WHERE student_id = s.id
            ) AS status_change_count
        FROM students s
        LEFT JOIN progress p ON s.id = p.student_id
        WHERE s.id NOT IN (SELECT id FROM archived_students)
        ORDER BY s.name
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results

def get_subjects_by_course(course):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM subject WHERE course = %s", (course,))
        results = cursor.fetchall()
        return [row[0] for row in results]
    finally:
        cursor.close()
        conn.close()

def fetch_dropdown_options(course = None):
    global COURSE_OPTIONS, SUBJECT_OPTIONS, PROFESSOR_OPTIONS, ADVISOR_OPTIONS, PANEL_OPTIONS, CHAIRMAN_OPTIONS

    COURSE_OPTIONS = ["Select an option"]
    SUBJECT_OPTIONS = ["Select an option"]
    PROFESSOR_OPTIONS = ["Select an option"]
    ADVISOR_OPTIONS = ["Select an option"]
    PANEL_OPTIONS = ["Select an option"]
    CHAIRMAN_OPTIONS = ["Select an option"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT course_id FROM course")
        results = cursor.fetchall()
        COURSE_OPTIONS += [row[0] for row in results]
        
        cursor.execute("SELECT name FROM subject")
        results = cursor.fetchall()
        SUBJECT_OPTIONS += [row[0] for row in results]

        cursor.execute("SELECT name FROM professor")
        results = cursor.fetchall()
        profs = [row[0] for row in results]
        PROFESSOR_OPTIONS += profs
        ADVISOR_OPTIONS += profs

        cursor.execute("SELECT name FROM panel")
        results = cursor.fetchall()
        PANEL_OPTIONS += [row[0] for row in results]
        CHAIRMAN_OPTIONS += [row[0] for row in results]

    finally:
        cursor.close()
        conn.close()

def archive_student(student_id):
    """
    Move a student and their current progress into your archive tables,
    then delete them from the live tables.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, name, email, course, subject, professor,
                   advisor, panel, chairman
            FROM students
            WHERE id = %s
        """, (student_id,))
        stud = cursor.fetchone()
        if stud:
            cursor.execute("""
                INSERT INTO archived_students
                  (id, name, email, course, subject, professor,
                   advisor, panel, chairman)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, stud)

        cursor.execute("""
            SELECT student_id, student_name, status
            FROM progress
            WHERE student_id = %s
        """, (student_id,))
        prog = cursor.fetchone()
        if prog:
            cursor.execute("""
                INSERT INTO archived_progress
                  (student_id, student_name, status)
                VALUES (%s,%s,%s)
            """, prog)

        cursor.execute("DELETE FROM progress WHERE student_id = %s", (student_id,))
        cursor.execute("DELETE FROM students  WHERE id         = %s", (student_id,))

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def get_archived_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.id, s.name, s.email, s.course, s.subject, s.professor,
            s.advisor, s.panel, s.chairman,
            p.status, s.enrollment_date, s.date_added, s.archived_date
        FROM archived_students s
        LEFT JOIN archived_progress p ON s.id = p.student_id
        ORDER BY s.archived_date DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def unarchive_student(student_id):
    """
    Move an 
    student back into the live tables,
    then remove their records from the archived tables.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, name, email, course, subject, professor,
                   advisor, panel, chairman,enrollment_date, date_added, archived_date
            FROM archived_students
            WHERE id = %s
        """, (student_id,))
        stud = cursor.fetchone()
        if stud:
            cursor.execute("""
                INSERT INTO students
                  (id, name, email, course, subject, professor,
                   advisor, panel, chairman, enrollment_date)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, stud[:10])

        cursor.execute("""
            SELECT student_id, status
            FROM archived_progress
            WHERE student_id = %s
        """, (student_id,))
        prog = cursor.fetchone()
        if prog:
            cursor.execute("""
                INSERT INTO progress (student_id, status)
                VALUES (%s,%s)
            """, prog)

        cursor.execute("DELETE FROM archived_progress  WHERE student_id = %s", (student_id,))
        cursor.execute("DELETE FROM archived_students WHERE id = %s", (student_id,))

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def update_password(email, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        cursor.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_pw, email))
        conn.commit()
        return cursor.rowcount > 0  # returns True if a row was updated
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def create_student(name, email, course, subject, professor, advisor, panel, chairman, active_status, enrollment_date):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (name, email, course, subject, professor, advisor, panel, chairman, active_status, enrollment_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, email, course, subject, professor, advisor, panel, chairman, active_status, enrollment_date))
        student_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO progress (student_id, student_name, status)
            VALUES (%s, %s, %s)
        """, (student_id, name, 'Pending'))
        conn.commit()
        return student_id
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT name, email, course, subject, professor, advisor,
                   panel, chairman, active_status, enrollment_date
            FROM students WHERE id = %s
        """, (student_id,))
        student = cursor.fetchone()
        cursor.execute("SELECT status FROM progress WHERE student_id = %s", (student_id,))
        status_row = cursor.fetchone()
        return student, (status_row[0] if status_row else None)
    finally:
        cursor.close()
        conn.close()

def update_student(student_id, name, email, course, subject, professor, advisor, panel, chairman, active_status, enrollment_date, status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE students
            SET name=%s, email=%s, course=%s, subject=%s, professor=%s,
                advisor=%s, panel=%s, chairman=%s, active_status=%s, enrollment_date=%s
            WHERE id=%s
        """, (name, email, course, subject, professor, advisor, panel, chairman, active_status, enrollment_date, student_id))

        cursor.execute("UPDATE progress SET status=%s, student_name=%s WHERE student_id=%s", (status, name, student_id))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO progress (student_id, student_name, status) VALUES (%s, %s, %s)", (student_id, name, status))

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def get_professor_names():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM professor")
        return [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

