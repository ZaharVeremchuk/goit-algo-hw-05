def binary_search(array, value):
    low = 0
    high = len(array) - 1
    iteration_count = 0

    while low <= high:
        
        iteration_count += 1

        mid = (low + high) // 2

        if array[mid] < value:
            low = mid + 1
        
        if array[mid] > value:
            high = mid - 1  

        else:
            return (iteration_count, high)
        
        
arr = [1.2, 1.4, 1.6, 2.0, 3.1, 3.5, 3.7]
print(binary_search(arr, 1.2)) 