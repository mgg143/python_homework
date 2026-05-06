# Task 5: Extending a Class
'''
1) Within the assignment3 folder, create a file called extend-point-to-vector.py.
2) Create a class called Point. It represents a point in 2d space, with x and y values passed to the __init__() method. It should include 
methods for equality, string representation, and Euclidian distance to another point.
3) Create a class called Vector which is a subclass of Point and uses the same __init__() method. Add a method in the vector class which 
overrides the string representation so Vectors print differently than Points. Override the + operator so that it implements vector addition, 
summing the x and y values and returning a new Vector.
4) Print results which demonstrate all of the classes and methods which have been implemented.
'''
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
class Vector(Point):
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

if __name__ == "__main__":
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(p1)  # Point(1, 2)
    print(p2)  # Point(3, 4)
    print(p1 == p2)  # False
    print(p1.distance_to(p2))  # 2.8284271247461903

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(v1)  # Vector(1, 2)
    print(v2)  # Vector(3, 4)
    v3 = v1 + v2
    print(v3)  # Vector(4, 6)