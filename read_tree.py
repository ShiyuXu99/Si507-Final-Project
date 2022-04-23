from build_tree import *
TREE_FILENAME = "tree_data.json"


def read_tree(movies, typeTree):
    constructTree(movies, typeTree)
    try:
        tree_file = open(TREE_FILENAME, 'r')
        tree_data = tree_file.read()
        tree_dict = json.loads(tree_data)
        tree_dict = tree_dict[typeTree]
        tree_file.close()
    except:
        tree_dict = {}
    return tree_dict