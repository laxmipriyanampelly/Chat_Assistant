import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Drop tables if they exist (for re-initialization)
cursor.execute("DROP TABLE IF EXISTS Employees")
cursor.execute("DROP TABLE IF EXISTS Departments")

# Create Employees Table
cursor.execute('''
    CREATE TABLE Employees (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        Salary INTEGER NOT NULL,
        Hire_Date TEXT NOT NULL
    )
''')

# Create Departments Table
cursor.execute('''
    CREATE TABLE Departments (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Manager TEXT NOT NULL
    )
''')

# Insert More Employees
cursor.executemany("INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?)", [
    ("Alice", "Sales", 50000, "2021-01-15"),
    ("Bob", "Engineering", 70000, "2020-06-10"),
    ("Charlie", "Marketing", 60000, "2022-03-20"),
    ("David", "Engineering", 75000, "2019-05-12"),
    ("Eve", "Sales", 55000, "2023-07-25"),
    ("Frank", "Marketing", 62000, "2022-11-10"),
    ("Grace", "HR", 58000, "2021-09-15"),
    ("Hank", "Engineering", 80000, "2018-12-05"),
    ("Ivy", "HR", 59000, "2023-01-10")
])

# Insert More Departments
cursor.executemany("INSERT INTO Departments (Name, Manager) VALUES (?, ?)", [
    ("Sales", "Alice"),
    ("Engineering", "Bob"),
    ("Marketing", "Charlie"),
    ("HR", "Grace")
])

# Commit and close connection
conn.commit()
conn.close()

print("Database setup complete with additional rows! ")

