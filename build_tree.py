import json
TREE_FILENAME = "tree_data.json"


def getGenre(movies):
    """
    Function that grabs all the genre type for future tree structure
    returns a word list of genres.
    """
    genreList = []
    for item in movies:
        if(isinstance(item.Genre, list)):
            for eachG in item.Genre:
                if(eachG not in genreList):
                    genreList.append(eachG)
        else:
            if(item.Genre not in genreList):
                    genreList.append(item.Genre)           
    return genreList
        
def constructTree(movies, treeType):
    """
    Function will construct the data table into a tree for retrieving information
    parameter1: list of movie objects
    parameter2: list of grenres
    returns a tree of data.
    """
    genreList = getGenre(movies)
    all_tree = {}
    tree = {}
    for genre in genreList:
        for movie in movies:
            if(isinstance(movie.Genre , list)):
                if(genre in movie.Genre):
                    if genre in tree:
                        movieData = tree[genre]
                    else:
                        movieData = {}
                    movieData[movie.MovieName] = {'URL': movie.TicketURL, 'PG':movie.PGRate, 'Description':movie.MovieDescription}
                    tree[genre] = movieData
            if(movie.Genre == genre):
                if genre in tree:
                    movieData = tree[genre]
                else:
                    movieData = {}
                movieData[movie.MovieName] = {'URL': movie.TicketURL, 'PG':movie.PGRate, 'Description':movie.MovieDescription}
                tree[genre] = movieData
    all_tree[treeType] = tree
    save_tree(all_tree)


def save_tree(data_dict):
    ''' saves the current state of the tree to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_tree_data = json.dumps(data_dict)
    fw = open(TREE_FILENAME,"w")
    fw.write(dumped_tree_data)
    fw.close() 