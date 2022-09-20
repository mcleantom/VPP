import datetime
import math
from sys import getsizeof


def PrintTime(startTime, message):
    seconds_in_day = 24 * 3600
    later_time = datetime.datetime.now()
    difference = later_time - first_time
    time_diff = 10**6 * (difference.days * seconds_in_day + difference.seconds) + difference.microseconds
    print(message + str(time_diff / 10**6))


myVariable = 3**100000 - 1
hLength = math.ceil(math.log(myVariable) / math.log(16))
dLength = math.ceil(math.log(myVariable) / math.log(10))
print(
    "Length in hex"
    + " "
    + str(hLength)
    + ". Decimal length "
    + str(dLength)
    + " Size of myVariable "
    + str(getsizeof(myVariable))
)
n = myVariable

first_time = datetime.datetime.now()
for i1 in range(0, hLength - 1):
    n = n >> 4
PrintTime(first_time, "Hex truncation time: ")

n = myVariable
first_time = datetime.datetime.now()
for i2 in range(0, dLength - 1):
    x = divmod(n, 10)
    n = x[0]
    r = x[1]
PrintTime(first_time, "divmod time - base 10: ")

n = myVariable
first_time = datetime.datetime.now()
for i2 in range(0, hLength - 1):
    x = divmod(n, 16)
    n = x[0]
    r = x[1]
PrintTime(first_time, "divmod time - base 16: ")
