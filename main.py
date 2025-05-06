import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import pickle
from PIL import Image, ImageTk
from database import Database
from face_detection import FaceDetector
import threading
import time

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance System")
        self.root.geometry("1200x700")
        
        self.db = Database()
        self.face_detector = FaceDetector()
        self.face_detector.load_known_faces(self.db)
        
        self.camera = cv2.VideoCapture(0)
        self.is_camera_on = False
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main frames
        self.left_frame = ttk.Frame(self.root, padding="10")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Camera view
        self.camera_label = ttk.Label(self.left_frame)
        self.camera_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Camera controls
        self.start_button = ttk.Button(self.left_frame, text="Start Camera", command=self.toggle_camera)
        self.start_button.grid(row=1, column=0, pady=5)
        
        self.capture_button = ttk.Button(self.left_frame, text="Capture", command=self.capture_face)
        self.capture_button.grid(row=1, column=1, pady=5)
        
        # Student registration form
        ttk.Label(self.right_frame, text="Student Registration", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.right_frame, text="Student ID:").grid(row=1, column=0, pady=5)
        self.student_id_entry = ttk.Entry(self.right_frame)
        self.student_id_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.right_frame, text="Name:").grid(row=2, column=0, pady=5)
        self.name_entry = ttk.Entry(self.right_frame)
        self.name_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(self.right_frame, text="Age:").grid(row=3, column=0, pady=5)
        self.age_entry = ttk.Entry(self.right_frame)
        self.age_entry.grid(row=3, column=1, pady=5)
        
        self.register_button = ttk.Button(self.right_frame, text="Register Student", command=self.register_student)
        self.register_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Attendance report
        ttk.Label(self.right_frame, text="Attendance Report", font=('Helvetica', 14, 'bold')).grid(row=5, column=0, columnspan=2, pady=10)
        
        self.report_tree = ttk.Treeview(self.right_frame, columns=("ID", "Name", "Time"), show="headings")
        self.report_tree.heading("ID", text="Student ID")
        self.report_tree.heading("Name", text="Name")
        self.report_tree.heading("Time", text="Time")
        self.report_tree.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.refresh_button = ttk.Button(self.right_frame, text="Refresh Report", command=self.refresh_report)
        self.refresh_button.grid(row=7, column=0, columnspan=2, pady=5)
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
    def toggle_camera(self):
        if not self.is_camera_on:
            self.is_camera_on = True
            self.start_button.config(text="Stop Camera")
            self.update_camera()
        else:
            self.is_camera_on = False
            self.start_button.config(text="Start Camera")
            
    def update_camera(self):
        if self.is_camera_on:
            ret, frame = self.camera.read()
            if ret:
                frame, face_names = self.face_detector.process_frame(frame)
                
                # Convert frame to PhotoImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(image=frame)
                
                self.camera_label.config(image=frame)
                self.camera_label.image = frame
                
                # Check for known faces and mark attendance
                for name in face_names:
                    if name != "Unknown":
                        if self.db.mark_attendance(name):
                            messagebox.showinfo("Attendance Marked", f"Attendance marked for {name}")
                
            self.root.after(10, self.update_camera)
            
    def capture_face(self):
        if not self.is_camera_on:
            messagebox.showerror("Error", "Please start the camera first")
            return
            
        ret, frame = self.camera.read()
        if ret:
            face_encoding = self.face_detector.get_face_encoding(frame)
            if face_encoding is not None:
                self.current_face_encoding = pickle.dumps(face_encoding)
                messagebox.showinfo("Success", "Face captured successfully!")
            else:
                messagebox.showerror("Error", "No face detected in the frame")
                
    def register_student(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        
        if not all([student_id, name, age]):
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
            return
            
        if not hasattr(self, 'current_face_encoding'):
            messagebox.showerror("Error", "Please capture face first")
            return
            
        if self.db.add_student(student_id, name, age, self.current_face_encoding):
            messagebox.showinfo("Success", "Student registered successfully!")
            self.face_detector.load_known_faces(self.db)  # Reload known faces
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Student ID already exists")
            
    def clear_entries(self):
        self.student_id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        if hasattr(self, 'current_face_encoding'):
            delattr(self, 'current_face_encoding')
            
    def refresh_report(self):
        # Clear existing items
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        # Get and display attendance report
        attendance_data = self.db.get_attendance_report()
        for student_id, name, time in attendance_data:
            self.report_tree.insert("", "end", values=(student_id, name, time))
            
    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop() 