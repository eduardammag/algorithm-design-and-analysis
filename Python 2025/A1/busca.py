# O(n)
def busca_linear(v,x):
    for i in range(len(v)):
        if v[i] == x:
            return i
    return -1

#O(log n)
def busca_binaria_recursiva(v, left, right, x):
    if left > right:
        return -1

    mid = (left + right)//2
    mid_val = v[mid]
    if mid_val == x:
        return mid_val
    if x> mid_val:
        return busca_binaria_recursiva(v, mid+1, right, x)
    else:
        return busca_binaria_recursiva(v, left, mid-1, x)

#O(log n)        
def busca_binaria_iterativa(v,x):
    left = 0
    right = len(v) - 1
    while left <= right:
        mid = (left + right)//2
        mid_val = v[mid]
        if mid_val == x:
            return mid
        elif x < mid_val:
            right = mid - 1
        else:
            left == mid + 1
    return -1            
