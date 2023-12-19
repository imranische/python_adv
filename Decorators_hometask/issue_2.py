import sys
from issue_1 import my_write


def timed_output(function):
    def wrapper(*args, **kwargs):
        original_write = sys.stdout.write
        sys.stdout.write = my_write
        function(*args, **kwargs)
        sys.stdout.write = original_write
    return wrapper


@timed_output
def print_greeting(name):
    print(f'Hello, {name}!')


if __name__ == '__main__':
    print_greeting('Nikita')
    print('This is ordinary print')
    print_greeting('Gvido')
    print('This is ordinary print again')
