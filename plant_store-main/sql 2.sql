CREATE DATABASE CollegeDB;
GO

USE CollegeDB;
GO

CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Course VARCHAR(50),
    Marks INT,
    City VARCHAR(50)
);
GO

INSERT INTO Students (StudentID, Name, Age, Course, Marks, City)
VALUES
(1, 'Rahul', 20, 'CSE', 85, 'Nagpur'),
(2, 'Priya', 21, 'IT', 92, 'Pune'),
(3, 'Amit', 20, 'CSE', 67, 'Mumbai'),
(4, 'Sneha', 22, 'AIML', 88, 'Nagpur'),
(5, 'Riya', 21, 'IT', 95, 'Pune'),
(6, 'Karan', 23, 'CSE', 72, 'Delhi'),
(7, 'Neha', 20, 'AIML', 81, 'Mumbai'),
(8, 'Vishal', 22, 'IT', 60, 'Nagpur');
GO