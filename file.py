import time
TIME_WAIT = 0

def add_one(x):
    x += 1
    return x

def add_two(x):
    x = x + 2

x = 5
print(x)
add_one(x)
print(x)
add_two(x)

print(x)
add_two(x)

print(x)
add_one(x)