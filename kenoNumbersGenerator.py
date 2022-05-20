from cgitb import text
import random

def rand_array (arr) :
    my_set, new_arr = set(arr), []
    for _ in range(len(arr)):
        new_number = random.randint(0, 60)
        while new_number in my_set:
            new_number = random.randint(0, 60)
        new_arr.append(new_number)
    return new_arr

while True:
    numbers = input("In:  ")
    prev_array = list (map(int, numbers.split(",")))
    print (f"Out: {rand_array(prev_array)}")

# Test input: 37, 31, 57, 8, 26, 48, 25, 27, 9, 12, 42, 55, 35, 22, 49, 21, 46, 43, 30, 20
# 10,59,45,29,57,17,15,23,31,56,54,27,36,34,12,30,52,49,28,51


