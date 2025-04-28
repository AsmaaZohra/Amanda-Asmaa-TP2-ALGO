# Nom(s) étudiant(s) / Name(s) of student(s): Amanda Dorval et Asmaa Skou

import sys



# Espace pour fonctions auxillaires :
# Space for auxilary functions :
def rech_en_profondeur(node, result):
    if not node:
        return 0,0  # si nombre de jetons et de noeud est de 0
    
    # analyse des sous-arbres gauches et droites
    jetons_gauches, noeuds_gauches = rech_en_profondeur(node.left, result)
    jetons_droits, noeuds_droits = rech_en_profondeur(node.right, result)

    # nombre total de noeuds dans sous-arbre (noeud courant)
    total_noeuds = noeuds_gauches + noeuds_droits + 1

    # nombre total de jetons dans le sous-arbre (noeud courant)
    total_jetons = jetons_gauches + jetons_droits + node.val

    # calcul du flux de jetons (différence entre jetons actuels et jetons nécéssaires)
    flow = total_jetons - total_noeuds

    # résultat en valeur absolu
    result[0] += abs(flow)

    # retourne le nombre de jetons et de noeuds dans le sous-arbre
    return total_jetons, total_noeuds




# Fonction à compléter / function to complete:
def solve(root) :
    if not root:
        return 0
    
    result = [0] 
    rech_en_profondeur(root, result)
    return result[0]
    

# Ne pas modifier le code ci-dessous :
# Do not modify the code below :

# Ne pas modifier le code ci-dessous :

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def process_numbers(input_file):
    try:
        # Read integers from the input file
        with open(input_file, "r") as f:
            lines = f.readlines() 
            tree_list = list(map(int, lines[0].split()))  # valeur de chaque noeud
            root = build_tree(tree_list)

        return solve(root)
    
    except Exception as e:
        print(f"Error: {e}")

def build_tree(lst):
    if not lst:
        return None
    
    root = TreeNode(lst[0])
    queue = [root]
    i = 1
    
    while i < len(lst):
        node = queue.pop(0)
        
        if i < len(lst):
            node.left = TreeNode(lst[i])
            queue.append(node.left)
            i += 1
        
        if i < len(lst):
            node.right = TreeNode(lst[i])
            queue.append(node.right)
            i += 1
    
    return root

def print_tree(root):
    if not root:
        return
    current_level = [root]
    while current_level:
        next_level = []
        values = []
        for node in current_level:
            if node:
                values.append(str(node.val))
                if node.left != None :
                    next_level.append(node.left)
                if node.right != None :
                    next_level.append(node.right)
        print(" ".join(values))
        current_level = next_level

def main():
    if len(sys.argv) != 2:
        print("Usage: python distribution.py <input_file>")
        return

    input_file = sys.argv[1]

    print(f"Input File: {input_file}")
    res = process_numbers(input_file)
    print(f"Result: {res}")

if __name__ == "__main__":
    main()





