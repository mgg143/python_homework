# ==============================================================================
# SCRIPT: sql_intro_2.py
# PURPOSE: Extract, merge, analyze, and save commercial order summary statistics
#          by blending the power of SQL Databases and Pandas DataFrames.
# ==============================================================================

# ------------------------------------------------------------------------------
# STEP 1: LOADING MODULE DEPENDENCIES (IMPORTS)
# Think of imports like pulling specialized toolboxes out of Python's warehouse.
# ------------------------------------------------------------------------------

# 'os' stands for Operating System. We use it to navigate file folders safely,
# ensuring our code works perfectly whether run on Windows, Mac, or Linux.
import os

# 'sqlite3' is Python's built-in connector to talk to lightweight SQL databases.
import sqlite3

# 'pandas' is the industry-standard data analysis library. We give it the shorter
# nickname 'pd' so we don't have to type out the full word every time we use it.
import pandas as pd

# 'warnings' allows us to control how Python manages system alerts in the terminal.
import warnings

# 🌟 SYSTEM CAPABILITY CONFIGURATION:
# This line tells Python to completely ignore "FutureWarnings". These aren't errors;
# they are just notices that a library's internal code rules will change in a year or two.
# Muting them ensures our terminal output stays completely clean, legible, and professional.
warnings.simplefilter(action="ignore", category=FutureWarning)


# ------------------------------------------------------------------------------
# STEP 2: DEFINING ENVIRONMENT PATHS
# ------------------------------------------------------------------------------
# We map where our database file lives. The '..' symbol means "step backward out 
# of our current folder (assignment9), look for a folder named 'db', and locate 'lesson.db'".
LESSON_DB_PATH = os.path.join("..", "db", "lesson.db")


def main():
    """The master execution core of our analysis program."""
    print(f"Connecting to lesson database asset at: {LESSON_DB_PATH}")

    # --------------------------------------------------------------------------
    # STEP 3: ESTABLISHING SAFE DATABASE CONNECTIONS
    # We wrap database code in a 'try-except' block. If the database file is missing,
    # corrupt, or locked, the program won't crash violently; it will catch the error gracefully.
    # --------------------------------------------------------------------------
    try:
        # Open a communication bridge to the 'lesson.db' database file.
        conn = sqlite3.connect(LESSON_DB_PATH)

        # ----------------------------------------------------------------------
        # STEP 4: WRITING THE SQL RELATIONAL JOIN COMMAND
        # Databases store data across separate, isolated spreadsheets to save space.
        # Here, 'line_items' holds raw order rows, and 'products' holds pricing info.
        # We use an INNER JOIN to merge them together wherever their 'product_id' numbers match!
        # ----------------------------------------------------------------------
        query = """
            SELECT 
                line_items.line_item_id, 
                line_items.quantity, 
                line_items.product_id, 
                products.product_name, 
                products.price 
            FROM line_items
            INNER JOIN products ON line_items.product_id = products.product_id;
        """

        print("\nLoading SQL tracking metrics into a Pandas DataFrame...")
        
        # 🌟 SYSTEM FIX: pd.read_sql_query runs our SQL command and extracts the results.
        # We append '.copy()' at the end to create a 100% independent spreadsheet in memory.
        # This prevents Pandas from worrying about database connection tracking down the line.
        df = pd.read_sql_query(query, conn).copy()

        # Print the first 5 lines of our new dataset container to verify it worked.
        print("\n--- Initial Raw Joined Data Frame Snapshot (First 5 Rows) ---")
        print(df.head(5))

        # ----------------------------------------------------------------------
        # STEP 5: CREATING A DERIVED ANALYSIS COLUMN
        # ----------------------------------------------------------------------
        # 🌟 SYSTEM FIX: We use the explicit '.loc[:, "total"]' syntax here.
        # The colon ':' tells Pandas to apply this rule to EVERY SINGLE ROW in the sheet.
        # We multiply the 'quantity' column by the 'price' column to calculate total order cost.
        df.loc[:, "total"] = df["quantity"] * df["price"]

        print("\n--- Verification Snapshot with Derived 'total' Revenue Column ---")
        print(df.head(5))

        # ----------------------------------------------------------------------
        # STEP 6: AGGREGATING DATA WITH GROUPBY & AGG
        # Right now, the same product might appear on 50 different rows for different orders.
        # We want to compress those duplicate product rows down into a single summary line per item.
        # ----------------------------------------------------------------------
        print("\nAggregating order frequency blocks and financial matrices...")
        
        # .groupby("product_id") tells Python to group all rows with identical product numbers together.
        # .agg({...}) defines our math rules for the compressed columns:
        #   - 'line_item_id': 'count' ➔ Counts how many total individual order entries occurred.
        #   - 'total': 'sum'           ➔ Adds up every dollar spent on this item to get total revenue.
        #   - 'product_name': 'first'  ➔ Grabs the first text name it finds so we can read it easily.
        summary_df = df.groupby("product_id").agg({
            "line_item_id": "count",
            "total": "sum",
            "product_name": "first"
        })

        # ----------------------------------------------------------------------
        # STEP 7: CLEANING AND RE-LABELING HEADERS
        # Our aggregated columns have technical names like 'line_item_id'. We use
        # .rename() to swap them out for more digestible business terms.
        # ----------------------------------------------------------------------
        summary_df = summary_df.rename(columns={
            "line_item_id": "times_ordered",
            "total": "total_revenue"
        })

        # ----------------------------------------------------------------------
        # STEP 8: SORTING RESULTS ALPHABETICALLY
        # We sort our rows by 'product_name' from A to Z (ascending=True) so it reads like a directory.
        # ----------------------------------------------------------------------
        summary_df = summary_df.sort_values(by="product_name", ascending=True)

        print("\n--- Final Aggregated & Sorted Order Summary Snapshot ---")
        print(summary_df.head(5))

        # ----------------------------------------------------------------------
        # STEP 9: WRITING DATA OUT TO A SPREADSHEET FILE
        # .to_csv() exports our final summarized memory table into an external file.
        # 'index=True' ensures that our 'product_id' rows keep their labels in the file.
        # ----------------------------------------------------------------------
        output_csv_path = "order_summary.csv"
        summary_df.to_csv(output_csv_path, index=True)
        print(f"\nSuccess! Order summary spreadsheet compiled cleanly to: {output_csv_path}")

    # --------------------------------------------------------------------------
    # ERROR HANDLING AND CLEANUP GATES
    # --------------------------------------------------------------------------
    except sqlite3.Error as db_error:
        # Runs if the SQL code fails or database parsing has an internal glitch.
        print(f"Database error encountered: {db_error}")
        
    except FileNotFoundError:
        # Runs if Python physically cannot find the 'lesson.db' database file.
        print("File Error: Could not locate the lesson.db file inside the target ../db/ folder.")
        
    finally:
        # The 'finally' block is guaranteed to run no matter what happens, even if the app crashes.
        # We check if 'conn' was created, and if so, safely close the communication pipeline.
        if 'conn' in locals():
            conn.close()
            print("Lesson database communication safely disengaged.")


# This special Python check ensures this script only runs if executed directly.
# If another script imports this file as a secondary tool, it won't trigger by accident.
if __name__ == "__main__":
    main()