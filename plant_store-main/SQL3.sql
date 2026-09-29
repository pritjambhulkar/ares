-- Create Database
CREATE DATABASE CollegeDB;
GO

-- Use the Database
USE CollegeDB;
GO

-- Create Student Table
CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    StudentName VARCHAR(100) NOT NULL,
    Age INT,
    Email VARCHAR(100) UNIQUE,
    Gender VARCHAR(10),
    Course VARCHAR(50),
    Marks DECIMAL(5,2),
    City VARCHAR(50)
);
GO

-- Insert Records
INSERT INTO Students
(StudentID, StudentName, Age, Email, Gender, Course, Marks, City)
VALUES
(1, 'Rahul', 20, 'rahul@gmail.com', 'Male', 'MCA', 85.50, 'Nagpur'),
(2, 'Priya', 21, 'priya@gmail.com', 'Female', 'MCA', 91.00, 'Pune'),
(3, 'Amit', 22, 'amit@gmail.com', 'Male', 'BCA', 76.50, 'Mumbai'),
(4, 'Sneha', 20, 'sneha@gmail.com', 'Female', 'MCA', 88.00, 'Nagpur'),
(5, 'Rohan', 23, 'rohan@gmail.com', 'Male', 'BCA', 69.50, 'Pune');
GO

-- Display All Students
SELECT * FROM Students;
GO

-- Display students with marks greater than 80
SELECT * 
FROM Students
WHERE Marks > 80;
GO

-- Display students from Nagpur
SELECT *
FROM Students
WHERE City = 'Nagpur';
GO

-- Sort students by marks
SELECT *
FROM Students
ORDER BY Marks DESC;
GO

-- Find average marks
SELECT AVG(Marks) AS AverageMarks
FROM Students;
GO

-- Find highest marks
SELECT MAX(Marks) AS HighestMarks
FROM Students;
GO

-- Find lowest marks
SELECT MIN(Marks) AS LowestMarks
FROM Students;
GO

-- Count total students
SELECT COUNT(*) AS TotalStudents
FROM Students;
GO