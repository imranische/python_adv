import sys
import datetime
import pytz

original_write = sys.stdout.write

def my_write(string_text):
    if string_text == '\n':
        return
    add_current_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))\
        .strftime('[%Y-%m-%d %H:%M:%S]: ')
    string = add_current_time + string_text + '\n'
    original_write(string)


if __name__ == '__main__':
    print('original output:')
    print('1, 2, 3')
    print('\ntimed_output:')
    original_write = sys.stdout.write
    sys.stdout.write = my_write
    print('1, 2, 3')
    sys.stdout.write = original_write
    print('\noriginal output again:')
    print('1, 2, 3')