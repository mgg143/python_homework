# ==============================================================================
# SCRIPT: advanced_sql.py
# PURPOSE: Assignment 10 - Advanced SQL queries, subqueries, write transactions,
#          and aggregation with conditionals using SQLite and Python.
# ==============================================================================

import os
import sqlite3
import warnings

# Mute harmless internal warnings to keep the terminal clean and professional
warnings.simplefilter(action="ignore", category=FutureWarning)

# Define the relative path to the pre-populated lesson database
# We step backward out of 'assignment10', enter the 'db' folder, and access 'lesson.db'
DB_PATH = os.path.join("..", "db", "lesson.db")


def run_task_1(conn):
    """TASK 1: Complex JOINs with Aggregation

    Problem: Find the total price of each of the first 5 orders.
    Steps:
      - Join the orders, line_items, and products tables.
      - Group by order_id to aggregate items within an order.
      - Calculate the sum of (product price * line_item quantity).
      - Order by order_id and limit the results to the first 5.
    """
    print("\n========================================================")
    print("TASK 1: Total Price of the First 5 Orders")
    print("========================================================")

    try:
        cursor = conn.cursor()

        # Write the SQL query matching the schema rules
        query = """
            SELECT 
                orders.order_id,
                SUM(products.price * line_items.quantity) AS total_order_price
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
            ORDER BY orders.order_id ASC
            LIMIT 5;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        # Display the formatted results
        print(f"{'Order ID':<10} | {'Total Price':<15}")
        print("-" * 28)
        for row in results:
            order_id, total_price = row
            # Format the float to 2 decimal places for currency representation
            print(f"{order_id:<10} | ${total_price:<14.2f}")

    except sqlite3.Error as e:
        print(f"Database error in Task 1: {e}")


def run_task_2(conn):
    """TASK 2: Understanding Subqueries

    Problem: Find the average price of orders for each customer.
    Steps:
      - Subquery: Compute the total price of each order (similar to Task 1),
        returning 'customer_id' aliased as 'customer_id_b' and the order total.
      - Main Statement: LEFT JOIN the 'customers' table with the subquery
        results using ON customer_id = customer_id_b to prevent name collisions.
      - Group by customer name to aggregate their order averages.
    """
    print("\n========================================================")
    print("TASK 2: Average Order Price per Customer (Subqueries)")
    print("========================================================")

    try:
        cursor = conn.cursor()

        # SQL Query utilizing an embedded Subquery joined to the customers table
        query = """
            SELECT 
                customers.customer_name,
                AVG(subquery.total_price) AS average_total_price
            FROM customers
            LEFT JOIN (
                SELECT 
                    orders.customer_id AS customer_id_b,
                    SUM(products.price * line_items.quantity) AS total_price
                FROM orders
                JOIN line_items ON orders.order_id = line_items.order_id
                JOIN products ON line_items.product_id = products.product_id
                GROUP BY orders.order_id
            ) AS subquery ON customers.customer_id = subquery.customer_id_b
            GROUP BY customers.customer_id;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        print(f"{'Customer Name':<25} | {'Average Order Price':<20}")
        print("-" * 48)
        for row in results:
            customer_name, avg_price = row
            # Handle potential None values for customers without any orders
            display_price = (
                f"${avg_price:.2f}" if avg_price is not None else "$0.00"
            )
            print(f"{customer_name:<25} | {display_price:<20}")

    except sqlite3.Error as e:
        print(f"Database error in Task 2: {e}")


def run_task_3(conn):
    """TASK 3: An Insert Transaction Based on Data

    Problem: Create a new order for 'Perez and Sons' handled by 'Miranda Harris'.
    The customer wants 10 of each of the 5 least expensive products.
    Steps:
      - Perform SELECT queries to retrieve IDs for the customer, employee, and products.
      - Insert the new order record and retrieve the auto-assigned order_id.
      - Insert 5 line_item records within a single transaction.
      - Verify by selecting and printing the line_item IDs, quantities, and product names.
    """
    print("\n========================================================")
    print("TASK 3: Insert Transaction & Order Creation")
    print("========================================================")

    try:
        cursor = conn.cursor()

        # Step 1: Retrieve necessary Foreign Key IDs dynamically
        # A) Get Customer ID for "Perez and Sons"
        cursor.execute(
            "SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons';"
        )
        cust_row = cursor.fetchone()
        if not cust_row:
            print("Error: Customer 'Perez and Sons' not found.")
            return
        customer_id = cust_row[0]

        # B) Get Employee ID for "Miranda Harris"
        cursor.execute(
            "SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris';"
        )
        emp_row = cursor.fetchone()
        if not emp_row:
            print("Error: Employee 'Miranda Harris' not found.")
            return
        employee_id = emp_row[0]

        # C) Get the 5 least expensive product IDs
        cursor.execute(
            "SELECT product_id FROM products ORDER BY price ASC LIMIT 5;"
        )
        product_rows = cursor.fetchall()
        product_ids = [row[0] for row in product_rows]

        if len(product_ids) < 5:
            print("Error: Less than 5 products available in database.")
            return

        # Step 2: Create the Order Record within an explicit transaction
        print("Starting order creation transaction...")

        # Leave primary key (order_id) off the insert; let SQLite autoincrement it
        # RETURNING clause captures the system-assigned order ID immediately
        cursor.execute(
            """
            INSERT INTO orders (customer_id, employee_id, order_date)
            VALUES (?, ?, datetime('now'))
            RETURNING order_id;
        """,
            (customer_id, employee_id),
        )
        new_order_id = cursor.fetchone()[0]
        print(f" -> Created master order record with Order ID: {new_order_id}")

        # Step 3: Insert 5 line item rows referencing the new Order ID, ordering 10 of each product
        print(" -> Adding 5 line item records (10 units per product)...")
        for prod_id in product_ids:
            cursor.execute(
                """
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, 10);
            """,
                (new_order_id, prod_id),
            )

        # The transaction commits successfully here.
        # If any query above failed, Python's exception block would catch it and automatically rollback.
        conn.commit()
        print("Transaction committed successfully to database.")

        # Step 4: Verify results by printing the newly created line items joined with product names
        print("\nVerifying New Order Line Items:")
        verification_query = """
            SELECT 
                line_items.line_item_id,
                line_items.quantity,
                products.product_name
            FROM line_items
            JOIN products ON line_items.product_id = products.product_id
            WHERE line_items.order_id = ?;
        """
        cursor.execute(verification_query, (new_order_id,))
        items = cursor.fetchall()

        print(f"{'Line Item ID':<15} | {'Quantity':<10} | {'Product Name'}")
        print("-" * 55)
        for item in items:
            li_id, qty, p_name = item
            print(f"{li_id:<15} | {qty:<10} | {p_name}")

    except sqlite3.Error as e:
        # If anything goes wrong, this undoes all inserts made inside the try block, protecting database integrity
        conn.rollback()
        print(f"Transaction failed, database rolled back. Error: {e}")


def run_task_4(conn):
    """TASK 4: Aggregation with HAVING

    Problem: Find all employees associated with more than 5 orders.
    Steps:
      - Join the employees and orders tables.
      - Group by employee identifier.
      - Use COUNT to total up orders per employee.
      - Apply a HAVING clause to restrict results to counts strictly greater than 5.
    """
    print("\n========================================================")
    print("TASK 4: Employees with > 5 Orders (HAVING Clause)")
    print("========================================================")

    try:
        cursor = conn.cursor()

        query = """
            SELECT 
                employees.employee_id,
                employees.first_name,
                employees.last_name,
                COUNT(orders.order_id) AS total_orders
            FROM employees
            JOIN orders ON employees.employee_id = orders.employee_id
            GROUP BY employees.employee_id
            HAVING COUNT(orders.order_id) > 5;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        print(f"{'Emp ID':<8} | {'First Name':<15} | {'Last Name':<15} | {'Orders'}")
        print("-" * 60)
        for row in results:
            emp_id, f_name, l_name, order_count = row
            print(f"{emp_id:<8} | {f_name:<15} | {l_name:<15} | {order_count:<6}")

    except sqlite3.Error as e:
        print(f"Database error in Task 4: {e}")


def main():
    """Master controller that starts up the application and routes tasks."""
    print(f"Attempting connection to database file at: {DB_PATH}")

    if not os.path.exists(DB_PATH):
        print(
            f"Error: Database file missing at {DB_PATH}. Ensure the db directory is populated."
        )
        return

    # Open the database connection
    conn = sqlite3.connect(DB_PATH)

    # CRITICAL REQUIREMENT: Turn on Foreign Keys explicitly
    # This prevents orphaned data or bad relational updates within our code connection
    conn.execute("PRAGMA foreign_keys = 1;")

    try:
        # Run all assignment tasks sequentially
        run_task_1(conn)
        run_task_2(conn)
        run_task_3(conn)
        run_task_4(conn)

    finally:
        # Ensure the connection is closed cleanly upon exit, run or crash
        conn.close()
        print("\nDatabase connection disengaged. Program complete.")


# This ensures the script executes only when run directly from the terminal
if __name__ == "__main__":
    main()