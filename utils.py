import time
from functools import wraps
from typing import Callable


def get_exectution_time(func: Callable) -> Callable:
    """
    wrapper to get execution time of a function
    Usage - @get_execution_time above the function definition
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time to run function: [{func.__name__}]: {end-start}")
        return result

    return wrap
