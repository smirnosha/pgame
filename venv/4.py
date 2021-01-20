a = int(input())
f = 0
b = 0
if a == 3:
    b = 1
while a >= 2:
    a -= 3
    f += 1
if a == 1 or a == 2:
    print('FALSE')
if a == 0 and f % 3 != 0 and b != 1:
    print('FALSE')
if a == 0 and f % 3 != 0 and b == 1:
    print('TRUE')
if a == 0 and f % 3 == 0:
    print('TRUE')
if a == - 1:
    print('FALSE')

