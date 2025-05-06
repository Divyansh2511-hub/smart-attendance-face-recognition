# Student Attendance System with Face Detection

This is a Python-based student attendance system that uses face detection and recognition to automatically mark attendance. The system prevents duplicate attendance entries and provides a user-friendly interface for managing student records.

## Features

- Face detection and recognition using OpenCV and face_recognition
- Student registration with face capture
- Automatic attendance marking
- Duplicate attendance prevention
- Real-time attendance reporting
- SQLite database for data storage
- Automatic CSV generation for student records

## Requirements

- Python 3.7 or higher
- Webcam
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone this repository or download the source code.

2. Install the required packages:
```bash
pip install -r requirements.txt
```

Note: For Windows users, you might need to install dlib separately. You can download the appropriate wheel file from [here](https://github.com/jloh02/dlib/releases) and install it using:
```bash
pip install path_to_downloaded_wheel_file
```

## Usage

1. Run the main application:
```bash
python main.py
```

2. Register a new student:
   - Click "Start Camera" to activate the webcam
   - Fill in the student details (ID, Name, Age)
   - Click "Capture" to take a photo of the student's face
   - Click "Register Student" to save the student's information
   - The system will automatically add the student to both the database and students.csv file

3. Mark attendance:
   - Click "Start Camera" to activate the webcam
   - The system will automatically detect faces and mark attendance
   - A notification will appear when attendance is marked

4. View attendance report:
   - Click "Refresh Report" to see the current day's attendance
   - The report shows student ID, name, and attendance time

## Data Storage

The system uses two types of storage:

1. SQLite Database (student_attendance.db):
   - Stores student information (ID, name, age, face encoding)
   - Stores attendance records (student ID, date, time)

2. CSV File (students.csv):
   - Automatically generated and updated
   - Contains student records with registration timestamps
   - Format: Student ID, Name, Age, Registration Date/Time
   - Created automatically when the program starts
   - Updated automatically when new students are registered

## Security Features

- Face recognition prevents proxy attendance
- Duplicate attendance entries are prevented
- Student IDs must be unique

## Troubleshooting

1. If the camera doesn't start:
   - Make sure your webcam is properly connected
   - Check if another application is using the webcam
   - Try restarting the application

2. If face detection is not working:
   - Ensure good lighting conditions
   - Make sure the face is clearly visible
   - Try adjusting the camera position

3. If you get an error about missing packages:
   - Make sure all requirements are installed
   - Try reinstalling the packages
   - Check if you have the correct Python version

## License

This project is open source and available under the MIT License. 