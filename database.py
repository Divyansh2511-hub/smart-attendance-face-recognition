import sqlite3
from datetime import datetime
import csv
import os

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('student_attendance.db')
        self.create_tables()
        self.students_csv = 'students.csv'
        self.initialize_students_csv()

    def initialize_students_csv(self):
        if not os.path.exists(self.students_csv):
            with open(self.students_csv, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Student ID', 'Name', 'Age', 'Registration Date'])

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                face_encoding BLOB
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                date TEXT,
                time TEXT,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        ''')
        
        self.conn.commit()

    def add_student(self, student_id, name, age, face_encoding):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO students (student_id, name, age, face_encoding)
                VALUES (?, ?, ?, ?)
            ''', (student_id, name, age, face_encoding))
            self.conn.commit()
            
            # Update CSV file
            with open(self.students_csv, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([student_id, name, age, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            
            return True
        except sqlite3.IntegrityError:
            return False

    def get_student(self, student_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        return cursor.fetchone()

    def get_all_students(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM students')
        return cursor.fetchall()

    def mark_attendance(self, student_id):
        cursor = self.conn.cursor()
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Check if attendance already marked for today
        cursor.execute('''
            SELECT * FROM attendance 
            WHERE student_id = ? AND date = ?
        ''', (student_id, current_date))
        
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO attendance (student_id, date, time)
                VALUES (?, ?, ?)
            ''', (student_id, current_date, current_time))
            self.conn.commit()
            return True
        return False

    def get_attendance_report(self, date=None):
        cursor = self.conn.cursor()
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT s.student_id, s.name, a.time
            FROM students s
            LEFT JOIN attendance a ON s.student_id = a.student_id AND a.date = ?
            ORDER BY s.student_id
        ''', (date,))
        return cursor.fetchall()

    def __del__(self):
        self.conn.close() 