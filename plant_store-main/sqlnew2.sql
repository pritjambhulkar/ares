-- ============================================
-- 1. CREATE DATABASE
-- ============================================

CREATE DATABASE CompanyDB;
GO

-- Use the database
USE CompanyDB;
GO


-- ============================================
-- 2. CREATE EMPLOYEE TABLE
-- ============================================

CREATE TABLE Employee
(
    EmployeeID INT PRIMARY KEY,
    Name VARCHAR(50),
    Department VARCHAR(50),
    Salary INT,
    City VARCHAR(50)
);
GO


-- ============================================
-- 3. INSERT DATA INTO TABLE
-- ============================================

INSERT INTO Employee
(EmployeeID, Name, Department, Salary, City)
VALUES
(1, 'Rahul', 'IT', 30000, 'Nagpur'),
(2, 'Priya', 'HR', 35000, 'Pune'),
(3, 'Amit', 'IT', 40000, 'Mumbai'),
(4, 'Sneha', 'Finance', 45000, 'Nagpur'),
(5, 'Rohan', 'Marketing', 32000, 'Pune');
GO


-- ============================================
-- 4. DISPLAY ALL DATA
-- ============================================

SELECT * FROM Employee;
GO


-- ============================================
-- 5. UPDATE ONE COLUMN
-- Change Rahul's salary
-- ============================================

UPDATE Employee
SET Salary = 40000
WHERE EmployeeID = 1;
GO


-- Check the updated data
SELECT * FROM Employee;
GO


-- ============================================
-- 6. UPDATE MULTIPLE COLUMNS
-- Change Rahul's department and city
-- ============================================

UPDATE Employee
SET Department = 'Software',
    City = 'Pune'
WHERE EmployeeID = 1;
GO


-- Check the updated data
SELECT * FROM Employee;
GO


-- ============================================
-- 7. UPDATE MULTIPLE ROWS
-- Increase salary of all IT employees by 5000
-- ============================================

UPDATE Employee
SET Salary = Salary + 5000
WHERE Department = 'IT';
GO


-- Check the updated data
SELECT * FROM Employee;
GO


-- ============================================
-- 8. UPDATE USING A CONDITION
-- Increase salary of employees earning less than 35000
-- ============================================

UPDATE Employee
SET Salary = Salary + 2000
WHERE Salary < 35000;
GO


-- Check the updated data
SELECT * FROM Employee;
GO


-- ============================================
-- 9. DELETE ONE RECORD
-- ============================================

DELETE FROM Employee
WHERE EmployeeID = 5;
GO


-- Check remaining records
SELECT * FROM Employee;
GO


-- ============================================
-- 10. DISPLAY SELECTED COLUMNS
-- ============================================

SELECT EmployeeID, Name, Salary
FROM Employee;
GO


-- ============================================
-- 11. DISPLAY EMPLOYEES FROM IT
-- ============================================

SELECT *
FROM Employee
WHERE Department = 'IT';
GO


-- ============================================
-- 12. DISPLAY EMPLOYEES WITH SALARY > 40000
-- ============================================

SELECT *
FROM Employee
WHERE Salary > 40000;
GO