#Name(s) of student(s): Amanda Dorval and Asmaa Zohra Skou 
import time 

import sys
#My OS : MacOS (Sequoia)
#My memory: 24 GB
#My CPU: Apple M4 pro 

# Space for auxilary functions :

def insertion_sort(array, left, right): #We don't need to sort the whole array since it's a hybride sort 
    #so instead of using the whole array, we use left and right to sort a sous-array 
    #Inspired by https://www.geeksforgeeks.org/insertion-sort-algorithm/
    for i in range(left + 1, right + 1):
        key = array[i]
        j = i - 1
        while j >= left and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key

#I just took the pseudocode from the Divide and Conquer chapter, p.24 and I wrote it in python 
def merge(T, d, m, f):
    G = T[d:m+1]
    D = T[m+1:f+1]

    i = j = 0
    k = d

    while i < len(G) and j < len(D):
        if G[i] <= D[j]:
            T[k] = G[i]
            i += 1
        else:
            T[k] = D[j]
            j += 1
        k += 1

    while i < len(G):
        T[k] = G[i]
        i += 1
        k += 1

    while j < len(D):
        T[k] = D[j]
        j += 1
        k += 1

#This hybrid algorithm uses the concept of divide and conquer (merge sort) except when the
#size of the input array is smaller than or equal to a certain threshold, for which the algorithm
#will switch to a simple naive algorithm (insertion sort). 
#Pretty similar to TimSort in python
def hybrid_sort(array,left,right,threshold):
    if left < right:
        if (right - left + 1) <= threshold:
            insertion_sort(array, left, right)
        else:
            m = (left + right) // 2
            hybrid_sort(array, left, m, threshold)
            hybrid_sort(array, m + 1, right, threshold)
            merge(array, left, m, right)


#function to complete:
def solve(array):
    thresholds = range(4, 129, 4)  # testing tresholds to determine the best 
    results = {}

    for threshold in thresholds:
        array_copy = list(array)
        start = time.perf_counter() #Chat GPT gave us this code to time the execution 
        hybrid_sort(array_copy, 0, len(array_copy) - 1, threshold)
        end = time.perf_counter()
        total_time = end - start
        results[threshold] = total_time

    # Chat GPT helps us changing the output in a tab format 
    print("{:<10} {:<15}".format('Threshold', 'Total Time (s)'))
    print("-" * 25)
    for threshold, time_taken in results.items():
        print("{:<10} {:<15.6f}".format(threshold, time_taken))

    best_threshold = min(results, key=results.get)
    print(f"Best threshold is {best_threshold} with time {results[best_threshold]:.6f} seconds")

    # Sort with the best threshold
    hybrid_sort(array, 0, len(array) - 1, best_threshold)
    return array


 

# Do not modify the code below :
def process_numbers(input_file):
    try:
        # Read integers from the input file
        with open(input_file, "r") as f:
            lines = f.readlines() 
            array = list(map(int, lines[0].split()))  # valeur de chaque noeud  

        return solve(array)
    
    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python tri_hybride.py <input_file>")
        return

    input_file = sys.argv[1]

    print(f"Input File: {input_file}")
    res = process_numbers(input_file)
    print(f"Result: {res}")

if __name__ == "__main__":
    main()
