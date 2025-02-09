from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Function to query the SQLite database
def query_database(sql_query, params=()):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(sql_query, params)
    results = cursor.fetchall()
    conn.close()
    return results

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("query", "").lower()  # Convert input to lowercase for consistency

    if "employees in the" in user_query:
        dept = user_query.split("employees in the ")[1].split(" department")[0]
        sql = "SELECT Name FROM Employees WHERE LOWER(Department) = LOWER(?)"
        results = query_database(sql, (dept,))
        response = ", ".join([row[0] for row in results]) if results else "No employees found"

    elif "manager of" in user_query:
        dept = user_query.split("manager of ")[1].split(" department")[0]
        sql = "SELECT Manager FROM Departments WHERE LOWER(Name) = LOWER(?)"
        results = query_database(sql, (dept,))
        response = results[0][0] if results else "No manager found"

    elif "hired after" in user_query:
        date = user_query.split("hired after ")[1]
        sql = "SELECT Name FROM Employees WHERE Hire_Date > ?"
        results = query_database(sql, (date,))
        response = ", ".join([row[0] for row in results]) if results else "No employees found"

    elif "total salary expense for the" in user_query:
        dept = user_query.split("total salary expense for the ")[1].split(" department")[0]
        sql = "SELECT SUM(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?)"
        results = query_database(sql, (dept,))
        response = f"Total salary expense: {results[0][0]}" if results and results[0][0] else "No salary data found"

    elif "highest paid employee in" in user_query:
        dept = user_query.split("highest paid employee in ")[1].split(" department")[0]
        sql = "SELECT Name, Salary FROM Employees WHERE LOWER(Department) = LOWER(?) ORDER BY Salary DESC LIMIT 1"
        results = query_database(sql, (dept,))
        response = f"Highest paid employee: {results[0][0]} with salary {results[0][1]}" if results else "No data found"

    elif "lowest paid employee in" in user_query:
        dept = user_query.split("lowest paid employee in ")[1].split(" department")[0]
        sql = "SELECT Name, Salary FROM Employees WHERE LOWER(Department) = LOWER(?) ORDER BY Salary ASC LIMIT 1"
        results = query_database(sql, (dept,))
        response = f"Lowest paid employee: {results[0][0]} with salary {results[0][1]}" if results else "No data found"

    elif "average salary in" in user_query:
        dept = user_query.split("average salary in ")[1].split(" department")[0]
        sql = "SELECT AVG(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?)"
        results = query_database(sql, (dept,))
        response = f"Average salary: {round(results[0][0], 2)}" if results and results[0][0] else "No data found"

    else:
        response = "I don't understand that query. Try another question!"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)


