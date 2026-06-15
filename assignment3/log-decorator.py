# Task 1: Writing and Testing a Decorator
'''
Within the assignment3 folder, create a file called log-decorator.py. It should contain the following.

Declare a decorator called logger_decorator. This should log the name of the called function (func.__name__), the input parameters of that were passed,
and the value the function returns, to a file ./decorator.log. (Logging was described in lesson 1, so review this if you need to do so.) 

Functions may have positional arguments, keyword arguments, both, or neither. So for each invocation of a decorated function, the log would have:

function: <the function name>
positional parameters: <a list of the positional parameters, or "none" if none are passed>
keyword parameters: <a dict of the keyword parameters, or "none" if none are passed>
return: <the return value>

Here's a cookbook on logging:
# one time setup
import logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))
...

# To write a log record:
logger.log(logging.INFO, "this string would be logged")
Declare a function that takes no parameters and returns nothing. Maybe it just prints "Hello, World!". Decorate this function with your decorator.
Declare a function that takes a variable number of positional arguments and returns True. Decorate this function with your decorator.
Declare a function that takes no positional arguments and a variable number of keyword arguments, and that returns logger_decorator. Decorate this 
function with your decorator.


Within the mainline code, call each of these three functions, passing parameters for the functions that take positional or keyword arguments. 
Run the program, and verify that the log file contains the information you want.
'''
import logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        logger.log(logging.INFO, f"function: {func.__name__}")
        if args:
            logger.log(logging.INFO, f"positional parameters: {args}")
        else:
            logger.log(logging.INFO, "positional parameters: none")
        if kwargs:
            logger.log(logging.INFO, f"keyword parameters: {kwargs}")
        else:
            logger.log(logging.INFO, "keyword parameters: none")
        return_value = func(*args, **kwargs)
        logger.log(logging.INFO, f"return: {return_value}")
        return return_value
    return wrapper

@logger_decorator
def hello_world():
    print("Hello, World!")

@logger_decorator
def variable_positional_args(*args):
    return True

@logger_decorator
def variable_keyword_args(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    # Call 1: No parameters
    hello_world()

    # Call 2: Variable positional arguments
    variable_positional_args(1, 2, "three")

    # Call 3: Variable keyword arguments
    variable_keyword_args(status="active", priority="high")