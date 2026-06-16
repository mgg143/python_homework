## Task 1: Introduction to Pandas - Creating and Manipulating DataFrames
'''
1) Create a DataFrame from a dictionary:
Use a dictionary containing the following data:
Name: ['Alice', 'Bob', 'Charlie']
Age: [25, 30, 35]
City: ['New York', 'Los Angeles', 'Chicago']

Convert the dictionary into a DataFrame using Pandas.
Print the DataFrame to verify its creation.
save the DataFrame in a variable called task1_data_frame and run the tests.

2) Add a new column:
Make a copy of the dataFrame you created named task1_with_salary (use the copy() method)
Add a column called Salary with values [70000, 80000, 90000].
Print the new DataFrame and run the tests.

3) Modify an existing column:
Make a copy of task1_with_salary in a variable named task1_older
Increment the Age column by 1 for each entry.
Print the modified DataFrame to verify the changes and run the tests.

4) Save the DataFrame as a CSV file:
Save the task1_older DataFrame to a file named employees.csv using to_csv(), do not include an index in the csv file.
Look at the contents of the CSV file to see how it's formatted.
Run the tests.
'''
import json # We will use this to create the JSON file in Task 2.2

import pandas as pd

#Addressing a downcasting warning when running the tests. This will ensure that 
 #when we fillna with a mean or median, the data type of the column will be 
 #preserved as numeric instead of being downcast to object.
pd.set_option('future.no_silent_downcasting', True) 

# T1.1) Create a DataFrame from a dictionary:
task1_data_dict = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
task1_data_frame = pd.DataFrame(task1_data_dict)

# Print to verify
print("--- Task 1: Original DataFrame ---")
print(task1_data_frame)

# T1.2) Add a new column:
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]

print("\n--- Task 2: Added Salary Column ---")
print(task1_with_salary)

# T1.3) Modify an existing column:
task1_older = task1_with_salary.copy()
task1_older.loc[:, 'Age'] = task1_older['Age'] + 1

print("\n--- Task 3: Incremented Age ---")
print(task1_older)

# T1.4) Save the DataFrame as a CSV file:
task1_older.to_csv('employees.csv', index=False)

# Verify the file content
with open('employees.csv', 'r') as f:
    print(f.read())

## Task 2: Loading Data from CSV and JSON
'''
1) Read data from a CSV file:
Load the CSV file from Task 1 into a new DataFrame saved to a variable task2_employees.
Print it and run the tests to verify the contents.

2) Read data from a JSON file:
Create a JSON file (additional_employees.json). The file adds two new employees. 
Eve, who is 28, lives in Miami, and has a salary of 60000, and Frank, who is 40, lives in Seattle, and has a salary of 95000.
Load this JSON file into a new DataFrame and assign it to the variable json_employees.
Print the DataFrame to verify it loaded correctly and run the tests.

3) Combine DataFrames:
Combine the data from the JSON file into the DataFrame Loaded from the CSV file and save it in the variable more_employees.
Print the combined Dataframe and run the tests.
'''

# T2.1) Read data from a CSV file:
task2_employees = pd.read_csv('employees.csv')

print("\n--- Task 1: Loaded CSV DataFrame ---")
print(task2_employees)

# T2.2) Read data from a JSON file:
# Create the JSON file with additional employees
additional_employees = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open('additional_employees.json', 'w') as f:
    json.dump(additional_employees, f)

json_employees = pd.read_json('additional_employees.json')

print("\n--- Task 2: Loaded JSON DataFrame ---")
print(json_employees)

# T2.3) Combine DataFrames:
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)

print("\n--- Task 3: Combined DataFrame ---")
print(more_employees)


## Task 3: Data Inspection - Using Head, Tail, and Info Methods
'''
1) Use the head() method:
Assign the first three rows of the more_employees DataFrame to the variable first_three
Print the variable and run the tests.
2) Use the tail() method:
Assign the last two rows of the more_employees DataFrame to the variable last_two
Print the variable and run the tests.
3) Get the shape of a DataFrame
Assign the shape of the more_employees DataFrame to the variable employee_shape
Print the variable and run the tests
4) Use the info() method:
Print a concise summary of the DataFrame using the info() method to understand the data types and non-null counts.
'''
# T3.1) Use the head() method:
first_three = more_employees.head(3)

print("\n--- Task 1: First Three Rows ---")
print(first_three)

# T3.2) Use the tail() method:
last_two = more_employees.tail(2)

print("\n--- Task 2: Last Two Rows ---")
print(last_two)

# T3.3) Get the shape of a DataFrame:
employee_shape = more_employees.shape

print("\n--- Task 3: Employee Shape ---")
print(employee_shape)

# T3.4) Use the info() method:
print("\n--- Task 4: Employee Info ---")
more_employees.info()


## Task 4: Data Cleaning
'''
1) Create a DataFrame from dirty_data.csv file and assign it to the variable dirty_data.
Print it and run the tests.
Create a copy of the dirty data in the varialble clean_data (use the copy() method). You will use data cleaning methods to update clean_data.

2) Remove any duplicate rows from the DataFrame
Print it and run the tests.

3) Convert Age to numeric and handle missing values
Print it and run the tests.

4) Convert Salary to numeric and replace known placeholders (unknown, n/a) with NaN
print it and run the tests.

5) Fill missing numeric values (use fillna).  Fill Age with the mean and Salary with the median
Print it and run the tests

6) Convert Hire Date to datetime
Print it and run the tests

7) Strip extra whitespace and standardize Name and Department as uppercase
Print it and run the tests
'''
# T4.1) Create a DataFrame from dirty_data.csv file:
dirty_data = pd.read_csv('dirty_data.csv')

print("\n--- Task 1: Dirty Data ---")
print(dirty_data)

clean_data = dirty_data.copy()

# T4.2) Remove any duplicate rows from the DataFrame
clean_data = clean_data.drop_duplicates()

print("\n--- Task 2: Clean Data (Duplicates Removed) ---")
print(clean_data)

# T4.3) Convert Age to numeric and handle missing values
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')

print("\n--- Task 3: Clean Data (Age Converted) ---")
print(clean_data)

# T4.4) Convert Salary to numeric and replace known placeholders (unknown, n/a) with NaN
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')

print("\n--- Task 4: Clean Data (Salary Converted) ---")
print(clean_data)

# T4.5) Fill missing numeric values (use fillna).  Fill Age with the mean and Salary with the median
clean_data.loc[:, 'Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data.loc[:, 'Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())

#Force the DataFrame to realize these are now numeric columns after filling missing values, which will help ensure the tests recognize them as numeric.
clean_data = clean_data.infer_objects(copy=False)

print("\n--- Task 5: Clean Data (Missing Values Filled) ---")
print(clean_data)

# T4.6) Convert Hire Date to datetime
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], errors='coerce', format='mixed')

print("\n--- Task 6: Clean Data (Hire Date Converted) ---")
print(clean_data)

# T4.7) Strip extra whitespace and standardize Name and Department as uppercase
clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()

print("\n--- Task 7: Clean Data (Name and Department Standardized) ---")
print(clean_data)

