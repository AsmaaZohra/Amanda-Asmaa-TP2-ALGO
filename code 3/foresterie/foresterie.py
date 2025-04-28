 # Name(s) of student(s): Asmaa Zohra Skou et Amanda Dorval

import sys


#function to complete:

# The problem is similar to the house robber problem 
#https://leetcode.com/problems/house-robber/solutions/156523/from-good-to-great-how-to-approach-most-of-dp-problems/ 
# Considering the test file, we only need to give the profits as the answer and not the trees used to get that output 
def solve(cost, forest) :
    profits = []
    for val in forest:
        profits.append(val - cost)

    n = len(profits) 

    if n == 0:
       return 0
    if n == 1:
       return max (0,profits[0]) #do not take in consideration a tree with a negative cost  
     
    tree_n_2 = 0 #best profit up to tree i-2
    tree_n_1 = max(0,profits[0]) #best profit up to tree i-1

    for i in range(1, n):
        current = max(tree_n_1, tree_n_2 + profits[i]) #you can either skip the current tree(profit tree n-1) or cut it (add to tree n-2) 
        #depending on the profit 
        tree_n_2 = tree_n_1
        tree_n_1 = current

    return tree_n_1



# Do not modify the code below :
def process_numbers(input_file):
    try:
        # Read integers from the input file
        with open(input_file, "r") as f:
            lines = f.readlines() 
            cost = int(lines[0].strip())  # cout d'exploitation pour couper un arbre
            forest = list(map(int, lines[1].split()))  # valeur de chaque arbre    

        return solve(cost, forest)
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python foresterie.py <input_file>")
        return

    input_file = sys.argv[1]

    print(f"Input File: {input_file}")
    res = process_numbers(input_file)
    print(f"Result: {res}")

if __name__ == "__main__":
    main() 
