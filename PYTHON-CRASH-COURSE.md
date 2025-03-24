# Python Crash Course

This crash course covers Python basics you'll need for building our CRUD application.

## 1. Python Basics

### Variables and Data Types

```python
# Variables (no need to declare type)
name = "John"          # String
age = 30               # Integer
price = 19.99          # Float
is_available = True    # Boolean

# Multiple assignment
x, y, z = 1, 2, 3

# Type conversion
str_age = str(age)     # Convert to string
int_price = int(price) # Convert to integer (truncates decimal)
```

### Strings

```python
# String operations
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name  # Concatenation

# Formatted strings (f-strings)
message = f"Hello, {full_name}. You are {age} years old."

# String methods
print(full_name.upper())   # Convert to uppercase
print(full_name.lower())   # Convert to lowercase
print(len(full_name))      # Length of string
```

### Lists

```python
# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "apple", True, 3.14]

# Accessing elements (0-indexed)
first_fruit = fruits[0]    # "apple"
last_fruit = fruits[-1]    # "cherry"

# Slicing
first_two = fruits[0:2]    # ["apple", "banana"]

# Common list methods
fruits.append("orange")    # Add to end
fruits.insert(1, "mango")  # Insert at index
fruits.remove("banana")    # Remove specific item
popped = fruits.pop()      # Remove and return last item
fruits.sort()              # Sort in place
```

### Dictionaries

```python
# Creating dictionaries
person = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

# Accessing values
print(person["name"])
print(person.get("age"))   # Safer way to access (returns None if key doesn't exist)

# Adding/modifying entries
person["email"] = "john@example.com"  # Add new key-value pair
person["age"] = 31                    # Modify existing value

# Dictionary methods
keys = person.keys()       # Get all keys
values = person.values()   # Get all values
items = person.items()     # Get all key-value pairs as tuples
```

## 2. Control Flow

### Conditional Statements

```python
# If-elif-else
age = 20
if age < 18:
    print("Minor")
elif age >= 18 and age < 65:
    print("Adult")
else:
    print("Senior")

# Ternary operator
status = "Adult" if age >= 18 else "Minor"
```

### Loops

```python
# For loop
for fruit in fruits:
    print(fruit)

# Loop with range
for i in range(5):         # 0 to 4
    print(i)

for i in range(1, 6):      # 1 to 5
    print(i)

# While loop
count = 0
while count < 5:
    print(count)
    count += 1
```

## 3. Functions

```python
# Basic function
def greet(name):
    return f"Hello, {name}!"

# Function with default parameter
def greet_with_title(name, title="Mr."):
    return f"Hello, {title} {name}!"

# Function with arbitrary number of arguments
def sum_all(*numbers):
    return sum(numbers)

# Function with keyword arguments
def build_profile(**user_info):
    return user_info
```

## 4. Error Handling

```python
# Try-except block
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("This runs no matter what")
```

## 5. Working with Files

```python
# Reading a file
with open("file.txt", "r") as file:
    content = file.read()

# Writing to a file
with open("new_file.txt", "w") as file:
    file.write("Hello, world!")

# Appending to a file
with open("file.txt", "a") as file:
    file.write("\nNew line")
```

## 6. Modules and Packages

```python
# Importing a module
import math
print(math.sqrt(16))

# Importing specific functions
from math import sqrt, pi
print(sqrt(16))

# Importing with alias
import math as m
print(m.sqrt(16))
```

## 7. Object-Oriented Programming

```python
# Creating a class
class Person:
    # Constructor
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Method
    def greet(self):
        return f"Hello, my name is {self.name}"

# Creating an instance
john = Person("John", 30)
print(john.greet())

# Inheritance
class Employee(Person):
    def __init__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title

    def introduce(self):
        return f"{self.greet()} and I work as a {self.job_title}"
```
