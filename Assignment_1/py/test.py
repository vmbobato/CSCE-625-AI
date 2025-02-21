import random 

def is_sorted(arr):
    for i in range(1, len(arr)):
        if arr[i - 1] > arr[i]:
            return False
    return True

arr = [i for i in range(11)]
j = 0
while True:
    print(f"Try #{j}")
    random.shuffle(arr)
    if is_sorted(arr):
        print(f"Found!  Array : {arr}")
        break
    j += 1