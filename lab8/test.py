from math import inf


def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):
        minValIndex = i
        for j in range(i+1, n):
            if arr[j] < arr[minValIndex]:
                minValIndex = j
        if minValIndex != i:
            arr[i], arr[minValIndex] = arr[minValIndex], arr[i]
    return arr

arr = [2,5,9,7,8,4,6,2,5]
print(selection_sort(arr))
