# Task 3: List Comprehensions Practice
'''
Within the assignment3 folder, create a file called list-comprehensions.py. Add code that reads the contents of ../csv/employees.csv into 
a list of lists using the csv module.

Using a list comprehension, create a list of the employee names, first_name + space + last_name. The list comprehension should iterate 
through the items in the list read from the csv file. Print the resulting list. Skip the item created for the heading of the csv file.

Using a list comprehension, create another list from the previous list of names. This list should include only those names that contain 
the letter "e". Print this list.
'''
import csv

with open("../csv/employees.csv", "r") as f:
    reader = csv.reader(f)
    employees = list(reader)

employee_names = [f"{employee[1]} {employee[2]}" for employee in employees[1:]]

print(employee_names)

names_with_e = [name for name in employee_names if "e" in name]

print(names_with_e)

